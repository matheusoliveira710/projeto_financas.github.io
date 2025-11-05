// Sistema Kanban
let projects = [];
let tasks = [];
let currentEditingTask = null;

// Inicialização
function initializeKanban() {
    loadProjects();
    loadTasks();
    setupEventListeners();
    renderTasks();
    updateStats();
    populateProjectSelect();
}

// Carregar dados
function loadProjects() {
    const saved = localStorage.getItem('projects');
    projects = saved ? JSON.parse(saved) : [];

    // Projetos de exemplo se estiver vazio
    if (projects.length === 0) {
        projects = [
            {
                id: 1,
                title: 'Desenvolvimento do Sistema',
                description: 'Projeto principal de desenvolvimento',
                deadline: '2024-12-31',
                priority: 'high',
                progress: 60,
                createdAt: new Date().toISOString()
            },
            {
                id: 2,
                title: 'Documentação',
                description: 'Documentação do sistema e manuais',
                deadline: '2024-11-30',
                priority: 'medium',
                progress: 30,
                createdAt: new Date().toISOString()
            }
        ];
        saveProjects();
    }
}

function loadTasks() {
    const saved = localStorage.getItem('tasks');
    tasks = saved ? JSON.parse(saved) : [
        // Tarefas de exemplo
        {
            id: 1,
            title: 'Configurar ambiente de desenvolvimento',
            description: 'Instalar todas as dependências e configurar o ambiente',
            assignee: 'João Silva',
            priority: 'high',
            effort: 4,
            status: 'done',
            projectId: 1,
            createdAt: new Date().toISOString()
        },
        {
            id: 2,
            title: 'Criar design do sistema',
            description: 'Desenvolver wireframes e protótipos do sistema',
            assignee: 'Maria Santos',
            priority: 'medium',
            effort: 8,
            status: 'inprogress',
            projectId: 1,
            createdAt: new Date().toISOString()
        },
        {
            id: 3,
            title: 'Implementar autenticação',
            description: 'Sistema de login e registro de usuários',
            assignee: 'Pedro Costa',
            priority: 'high',
            effort: 6,
            status: 'todo',
            projectId: 1,
            createdAt: new Date().toISOString()
        },
        {
            id: 4,
            title: 'Escrever documentação técnica',
            description: 'Documentar APIs e funcionalidades do sistema',
            assignee: 'Ana Oliveira',
            priority: 'medium',
            effort: 5,
            status: 'todo',
            projectId: 2,
            createdAt: new Date().toISOString()
        }
    ];
}

// Event Listeners
function setupEventListeners() {
    // Formulário de projeto
    document.getElementById('projectForm').addEventListener('submit', handleProjectSubmit);

    // Formulário de tarefa
    document.getElementById('taskForm').addEventListener('submit', handleTaskSubmit);

    // Fechar modais ao clicar fora
    window.addEventListener('click', function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
                resetForms();
            }
        });
    });
}

// Projetos
function showProjectModal() {
    document.getElementById('projectModal').style.display = 'block';
}

function closeProjectModal() {
    document.getElementById('projectModal').style.display = 'none';
    document.getElementById('projectForm').reset();
}

function handleProjectSubmit(e) {
    e.preventDefault();

    const project = {
        id: Date.now(),
        title: document.getElementById('projectTitle').value,
        description: document.getElementById('projectDescription').value,
        deadline: document.getElementById('projectDeadline').value,
        priority: document.getElementById('projectPriority').value,
        progress: 0,
        createdAt: new Date().toISOString()
    };

    projects.push(project);
    saveProjects();
    closeProjectModal();
    populateProjectSelect();
    showMessage('🎉 Projeto criado com sucesso!', 'success');
}

// Tarefas
function showTaskModal(status = 'todo') {
    document.getElementById('taskModal').style.display = 'block';
    document.getElementById('taskStatus').value = status;
    document.querySelector('#taskModal h3').textContent = '📝 Nova Tarefa';
    document.querySelector('#taskModal button').innerHTML = '<i class="fas fa-plus"></i> Criar Tarefa';
    currentEditingTask = null;
}

function closeTaskModal() {
    document.getElementById('taskModal').style.display = 'none';
    resetForms();
}

function handleTaskSubmit(e) {
    e.preventDefault();

    const taskData = {
        title: document.getElementById('taskTitle').value,
        description: document.getElementById('taskDescription').value,
        assignee: document.getElementById('taskAssignee').value || 'Não atribuído',
        priority: document.getElementById('taskPriority').value,
        effort: parseInt(document.getElementById('taskEffort').value) || 0,
        status: document.getElementById('taskStatus').value,
        projectId: document.getElementById('taskProject').value ?
                   parseInt(document.getElementById('taskProject').value) : null,
        updatedAt: new Date().toISOString()
    };

    if (currentEditingTask) {
        // Editar tarefa existente
        const taskIndex = tasks.findIndex(t => t.id === currentEditingTask);
        if (taskIndex !== -1) {
            tasks[taskIndex] = { ...tasks[taskIndex], ...taskData };
        }
    } else {
        // Criar nova tarefa
        taskData.id = Date.now();
        taskData.createdAt = new Date().toISOString();
        tasks.push(taskData);
    }

    saveTasks();
    closeTaskModal();
    renderTasks();
    updateStats();
    showMessage('✅ Tarefa salva com sucesso!', 'success');
}

function resetForms() {
    document.getElementById('taskForm').reset();
    document.getElementById('projectForm').reset();
    currentEditingTask = null;
}

// Renderização
function renderTasks() {
    const columns = {
        todo: document.getElementById('todoTasks'),
        inprogress: document.getElementById('inProgressTasks'),
        done: document.getElementById('doneTasks')
    };

    // Limpa todas as colunas
    Object.values(columns).forEach(column => {
        column.innerHTML = '';
    });

    // Renderiza tarefas nas respectivas colunas
    tasks.forEach(task => {
        const taskElement = createTaskElement(task);
        columns[task.status].appendChild(taskElement);
    });

    updateTaskCounts();
}

function createTaskElement(task) {
    const taskDiv = document.createElement('div');
    taskDiv.className = `task-card priority-${task.priority}`;
    taskDiv.draggable = true;
    taskDiv.id = `task-${task.id}`;

    const projectInfo = task.projectId ?
        `<div class="task-project">📁 ${getProjectName(task.projectId)}</div>` : '';

    taskDiv.innerHTML = `
        <div class="task-actions">
            <button class="task-action-btn edit" onclick="editTask(${task.id})" title="Editar">
                <i class="fas fa-edit"></i>
            </button>
            <button class="task-action-btn delete" onclick="deleteTask(${task.id})" title="Excluir">
                <i class="fas fa-trash"></i>
            </button>
        </div>
        <div class="task-header">
            <h4 class="task-title">${task.title}</h4>
            <span class="task-priority">${getPriorityLabel(task.priority)}</span>
        </div>
        ${projectInfo}
        <p class="task-description">${task.description || 'Sem descrição'}</p>
        <div class="task-footer">
            <span class="task-assignee">👤 ${task.assignee}</span>
            ${task.effort ? `<span class="task-effort">⏱️ ${task.effort}h</span>` : ''}
        </div>
    `;

    // Eventos de drag
    taskDiv.addEventListener('dragstart', dragStart);
    taskDiv.addEventListener('dragend', dragEnd);
    taskDiv.addEventListener('dblclick', () => showTaskDetail(task.id));

    return taskDiv;
}

// Drag and Drop
function allowDrop(ev) {
    ev.preventDefault();
    ev.currentTarget.classList.add('drag-over');
}

function dragStart(ev) {
    ev.dataTransfer.setData('text/plain', ev.target.id);
    ev.target.classList.add('dragging');
    setTimeout(() => {
        ev.target.style.display = 'none';
    }, 0);
}

function dragEnd(ev) {
    ev.target.classList.remove('dragging');
    ev.target.style.display = 'block';

    // Remove classe drag-over de todas as colunas
    document.querySelectorAll('.tasks-list').forEach(list => {
        list.classList.remove('drag-over');
    });
}

function drop(ev) {
    ev.preventDefault();
    ev.currentTarget.classList.remove('drag-over');

    const taskId = ev.dataTransfer.getData('text/plain').replace('task-', '');
    const newStatus = ev.currentTarget.parentElement.dataset.status;

    // Atualiza status da tarefa
    const taskIndex = tasks.findIndex(task => task.id == taskId);
    if (taskIndex !== -1) {
        tasks[taskIndex].status = newStatus;
        tasks[taskIndex].updatedAt = new Date().toISOString();

        saveTasks();
        renderTasks();
        updateStats();

        showMessage('✅ Tarefa movida!', 'success');
    }
}

// Ações das Tarefas
function editTask(taskId) {
    const task = tasks.find(t => t.id == taskId);
    if (task) {
        document.getElementById('taskTitle').value = task.title;
        document.getElementById('taskDescription').value = task.description || '';
        document.getElementById('taskAssignee').value = task.assignee;
        document.getElementById('taskPriority').value = task.priority;
        document.getElementById('taskEffort').value = task.effort;
        document.getElementById('taskStatus').value = task.status;
        document.getElementById('taskProject').value = task.projectId || '';

        document.getElementById('taskModal').style.display = 'block';
        document.querySelector('#taskModal h3').textContent = '✏️ Editar Tarefa';
        document.querySelector('#taskModal button').innerHTML = '<i class="fas fa-save"></i> Salvar Alterações';

        currentEditingTask = taskId;
    }
}

function deleteTask(taskId) {
    if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
        tasks = tasks.filter(task => task.id != taskId);
        saveTasks();
        renderTasks();
        updateStats();
        showMessage('🗑️ Tarefa excluída!', 'success');
    }
}

function showTaskDetail(taskId) {
    const task = tasks.find(t => t.id == taskId);
    if (task) {
        const modal = document.getElementById('taskDetailModal');
        const content = document.getElementById('taskDetailContent');

        content.innerHTML = `
            <div class="task-detail">
                <div class="task-detail-header">
                    <h3 class="task-detail-title">${task.title}</h3>
                    <span class="task-priority">${getPriorityLabel(task.priority)}</span>
                </div>
                
                <div class="task-detail-meta">
                    <div class="meta-item">
                        <span class="meta-label">Status</span>
                        <span class="meta-value">${getStatusLabel(task.status)}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Responsável</span>
                        <span class="meta-value">${task.assignee}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Prioridade</span>
                        <span class="meta-value">${getPriorityLabel(task.priority)}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Esforço</span>
                        <span class="meta-value">${task.effort ? task.effort + ' horas' : 'Não definido'}</span>
                    </div>
                    ${task.projectId ? `
                    <div class="meta-item">
                        <span class="meta-label">Projeto</span>
                        <span class="meta-value">${getProjectName(task.projectId)}</span>
                    </div>
                    ` : ''}
                </div>
                
                <div class="task-detail-description">
                    <h4>Descrição</h4>
                    <p>${task.description || 'Sem descrição'}</p>
                </div>
                
                <div class="task-detail-actions">
                    <button onclick="editTask(${task.id})" class="btn-primary">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button onclick="deleteTask(${task.id})" class="logout-btn">
                        <i class="fas fa-trash"></i> Excluir
                    </button>
                </div>
            </div>
        `;

        modal.style.display = 'block';
    }
}

function closeTaskDetailModal() {
    document.getElementById('taskDetailModal').style.display = 'none';
}

// Utilitários
function getPriorityLabel(priority) {
    const labels = {
        low: 'Baixa',
        medium: 'Média',
        high: 'Alta'
    };
    return labels[priority] || priority;
}

function getStatusLabel(status) {
    const labels = {
        todo: '📝 A Fazer',
        inprogress: '🚀 Em Progresso',
        done: '✅ Concluído'
    };
    return labels[status] || status;
}

function getProjectName(projectId) {
    const project = projects.find(p => p.id === projectId);
    return project ? project.title : 'Sem projeto';
}

function populateProjectSelect() {
    const select = document.getElementById('taskProject');
    if (select) {
        select.innerHTML = '<option value="">Sem projeto</option>' +
            projects.map(p => `<option value="${p.id}">${p.title}</option>`).join('');
    }
}

// Filtros e Busca
function filterTasks() {
    const searchTerm = document.getElementById('taskSearch').value.toLowerCase();
    const taskCards = document.querySelectorAll('.task-card');

    taskCards.forEach(card => {
        const title = card.querySelector('.task-title').textContent.toLowerCase();
        const description = card.querySelector('.task-description').textContent.toLowerCase();
        const assignee = card.querySelector('.task-assignee').textContent.toLowerCase();

        const matchesSearch = title.includes(searchTerm) ||
                            description.includes(searchTerm) ||
                            assignee.includes(searchTerm);

        card.style.display = matchesSearch ? 'block' : 'none';
    });
}

function filterByPriority(priority) {
    const buttons = document.querySelectorAll('.filter-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    const taskCards = document.querySelectorAll('.task-card');

    taskCards.forEach(card => {
        if (priority === 'all') {
            card.style.display = 'block';
        } else {
            const hasPriority = card.classList.contains(`priority-${priority}`);
            card.style.display = hasPriority ? 'block' : 'none';
        }
    });
}

// Estatísticas
function updateStats() {
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(task => task.status === 'done').length;
    const progress = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

    document.getElementById('totalProjects').textContent = projects.length;
    document.getElementById('totalTasks').textContent = totalTasks;
    document.getElementById('completedTasks').textContent = completedTasks;
    document.getElementById('overallProgress').textContent = progress + '%';
}

function updateTaskCounts() {
    const todoCount = tasks.filter(task => task.status === 'todo').length;
    const inProgressCount = tasks.filter(task => task.status === 'inprogress').length;
    const doneCount = tasks.filter(task => task.status === 'done').length;

    document.getElementById('todoCount').textContent = todoCount;
    document.getElementById('inProgressCount').textContent = inProgressCount;
    document.getElementById('doneCount').textContent = doneCount;
}

// Persistência
function saveProjects() {
    localStorage.setItem('projects', JSON.stringify(projects));
}

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Inicialização da App
function initializeApp() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    document.getElementById('userWelcome').textContent = `Bem-vindo, ${user.name || 'Usuário'}!`;

    initializeKanban();
    startNotificationSystem();
    loadSavedTheme();

    // Adicionar seletor de temas
    addThemeSelector();

    // Adicionar botão de gerenciar usuários (se for admin)
    addUsersButtonToHeader();

    // Inicializar gerenciador de usuários
    userManager.initialize();
}

// Controle de Views expandido
function showView(view) {
    const kanbanSection = document.querySelector('.kanban-board').closest('.main-content');
    const dashboardSection = document.getElementById('dashboardSection');
    const usersSection = document.getElementById('usersSection');
    const viewButtons = document.querySelectorAll('.view-btn');

    // Remover active de todos os botões
    viewButtons.forEach(btn => btn.classList.remove('active'));

    // Esconder todas as seções
    kanbanSection.style.display = 'none';
    dashboardSection.style.display = 'none';
    usersSection.style.display = 'none';

    // Mostrar seção selecionada
    switch(view) {
        case 'kanban':
            kanbanSection.style.display = 'block';
            break;
        case 'dashboard':
            dashboardSection.style.display = 'block';
            chartSystem.initCharts();
            break;
        case 'users':
            usersSection.style.display = 'block';
            userManager.loadUsers();
            break;
    }

    // Adicionar active ao botão clicado
    event.target.classList.add('active');
}

// Utilitários para modais
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Filtro de usuários
function filterUsers() {
    const searchTerm = document.getElementById('userSearch').value.toLowerCase();
    const userCards = document.querySelectorAll('.user-card');

    userCards.forEach(card => {
        const name = card.querySelector('.user-name').textContent.toLowerCase();
        const email = card.querySelector('.user-email').textContent.toLowerCase();

        const matchesSearch = name.includes(searchTerm) || email.includes(searchTerm);
        card.style.display = matchesSearch ? 'flex' : 'none';
    });
}

// Funções globais
window.showProjectModal = showProjectModal;
window.closeProjectModal = closeProjectModal;
window.showTaskModal = showTaskModal;
window.closeTaskModal = closeTaskModal;
window.closeTaskDetailModal = closeTaskDetailModal;
window.allowDrop = allowDrop;
window.drop = drop;
window.dragStart = dragStart;
window.dragEnd = dragEnd;
window.editTask = editTask;
window.deleteTask = deleteTask;
window.showTaskDetail = showTaskDetail;
window.filterTasks = filterTasks;
window.filterByPriority = filterByPriority;

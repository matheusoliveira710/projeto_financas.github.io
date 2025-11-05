// Projects Management
document.getElementById('projectForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const project = {
        title: document.getElementById('projectTitle').value,
        description: document.getElementById('projectDescription').value,
        deadline: document.getElementById('projectDeadline').value,
        priority: document.getElementById('projectPriority').value
    };
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/projects`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(project)
        });
        
        if (response.ok) {
            closeProjectModal();
            loadProjects();
            loadDashboard();
        } else {
            alert('Erro ao criar projeto');
        }
    } catch (error) {
        console.error('Error creating project:', error);
        alert('Erro de conexão');
    }
});

async function loadProjects() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/projects`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const projects = await response.json();
            displayProjects(projects);
        }
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

function displayProjects(projects) {
    const container = document.getElementById('projectsList');
    
    if (projects.length === 0) {
        container.innerHTML = '<p>Nenhum projeto encontrado. Crie seu primeiro projeto!</p>';
        return;
    }
    
    container.innerHTML = projects.map(project => `
        <div class="project-card" onclick="openProject(${project.id})">
            <div class="project-header">
                <h4 class="project-title">${project.title}</h4>
                <span class="project-priority priority-${project.priority}">
                    ${project.priority}
                </span>
            </div>
            <p class="project-description">${project.description}</p>
            <div class="project-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${project.progress || 0}%"></div>
                </div>
            </div>
            <div class="project-footer">
                <span>Vence: ${new Date(project.deadline).toLocaleDateString()}</span>
                <span>${project.progress || 0}%</span>
            </div>
        </div>
    `).join('');
}

function openProject(projectId) {
    // Implement project details view
    alert(`Abrindo projeto ${projectId}`);
}

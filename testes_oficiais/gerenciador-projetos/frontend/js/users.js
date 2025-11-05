// Sistema de Gerenciamento de Usuários
class UserManager {
    constructor() {
        this.users = [];
        this.currentUser = null;
    }

    // Carregar lista de usuários
    async loadUsers() {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE}/users`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.users = data.users;
                this.renderUsers();
            } else {
                throw new Error('Erro ao carregar usuários');
            }
        } catch (error) {
            console.error('❌ Erro ao carregar usuários:', error);
            showMessage('Erro ao carregar lista de usuários', 'error');
        }
    }

    // Renderizar lista de usuários
    renderUsers() {
        const container = document.getElementById('usersList');
        if (!container) return;

        container.innerHTML = this.users.map(user => `
            <div class="user-card ${user.active ? '' : 'inactive'}" data-user-id="${user.id}">
                <div class="user-avatar">
                    ${user.name.split(' ').map(n => n[0]).join('').toUpperCase()}
                </div>
                <div class="user-info">
                    <h4 class="user-name">${user.name}</h4>
                    <p class="user-email">${user.email}</p>
                    <div class="user-meta">
                        <span class="user-role role-${user.role}">${this.getRoleLabel(user.role)}</span>
                        <span class="user-status ${user.active ? 'active' : 'inactive'}">
                            ${user.active ? '✅ Ativo' : '❌ Inativo'}
                        </span>
                    </div>
                </div>
                <div class="user-actions">
                    <button class="btn-icon edit" onclick="userManager.editUser(${user.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    ${user.id !== this.currentUser?.id ? `
                        <button class="btn-icon ${user.active ? 'deactivate' : 'activate'}" 
                                onclick="userManager.toggleUserStatus(${user.id})" 
                                title="${user.active ? 'Desativar' : 'Ativar'}">
                            <i class="fas ${user.active ? 'fa-user-slash' : 'fa-user-check'}"></i>
                        </button>
                    ` : ''}
                </div>
            </div>
        `).join('');
    }

    // Criar novo usuário
    async createUser(userData) {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE}/users`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                showMessage('🎉 Usuário criado com sucesso!', 'success');
                this.loadUsers();
                return true;
            } else {
                throw new Error(data.error || 'Erro ao criar usuário');
            }
        } catch (error) {
            console.error('❌ Erro ao criar usuário:', error);
            showMessage(error.message, 'error');
            return false;
        }
    }

    // Editar usuário
    async editUser(userId) {
        const user = this.users.find(u => u.id === userId);
        if (!user) return;

        // Preencher modal de edição
        document.getElementById('editUserName').value = user.name;
        document.getElementById('editUserEmail').value = user.email;
        document.getElementById('editUserRole').value = user.role;
        document.getElementById('editUserActive').checked = user.active;

        // Mostrar modal
        document.getElementById('editUserModal').style.display = 'block';

        // Salvar ID do usuário sendo editado
        this.editingUserId = userId;
    }

    // Atualizar usuário
    async updateUser(userId, userData) {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE}/users/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                showMessage('✅ Usuário atualizado com sucesso!', 'success');
                this.loadUsers();
                return true;
            } else {
                throw new Error(data.error || 'Erro ao atualizar usuário');
            }
        } catch (error) {
            console.error('❌ Erro ao atualizar usuário:', error);
            showMessage(error.message, 'error');
            return false;
        }
    }

    // Alternar status do usuário
    async toggleUserStatus(userId) {
        const user = this.users.find(u => u.id === userId);
        if (!user) return;

        const newStatus = !user.active;
        const confirmMessage = newStatus ?
            `Ativar o usuário ${user.name}?` :
            `Desativar o usuário ${user.name}?`;

        if (!confirm(confirmMessage)) return;

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE}/users/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ active: newStatus })
            });

            const data = await response.json();

            if (response.ok) {
                showMessage(`✅ Usuário ${newStatus ? 'ativado' : 'desativado'} com sucesso!`, 'success');
                this.loadUsers();
            } else {
                throw new Error(data.error || 'Erro ao alterar status do usuário');
            }
        } catch (error) {
            console.error('❌ Erro ao alterar status do usuário:', error);
            showMessage(error.message, 'error');
        }
    }

    // Utilitários
    getRoleLabel(role) {
        const roles = {
            'admin': '👑 Administrador',
            'user': '👤 Usuário',
            'manager': '📊 Gerente'
        };
        return roles[role] || role;
    }

    // Verificar se usuário atual é admin
    isAdmin() {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        return user.role === 'admin';
    }

    // Inicializar sistema de usuários
    initialize() {
        this.currentUser = JSON.parse(localStorage.getItem('user') || '{}');

        if (this.isAdmin()) {
            this.loadUsers();
            this.setupEventListeners();
        }
    }

    // Configurar event listeners
    setupEventListeners() {
        // Formulário de criação de usuário
        document.getElementById('createUserForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();

            const userData = {
                name: document.getElementById('newUserName').value,
                email: document.getElementById('newUserEmail').value,
                password: document.getElementById('newUserPassword').value,
                role: document.getElementById('newUserRole').value
            };

            const success = await this.createUser(userData);
            if (success) {
                document.getElementById('createUserForm').reset();
                document.getElementById('createUserModal').style.display = 'none';
            }
        });

        // Formulário de edição de usuário
        document.getElementById('editUserForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();

            const userData = {
                name: document.getElementById('editUserName').value,
                email: document.getElementById('editUserEmail').value,
                role: document.getElementById('editUserRole').value,
                active: document.getElementById('editUserActive').checked
            };

            const success = await this.updateUser(this.editingUserId, userData);
            if (success) {
                document.getElementById('editUserModal').style.display = 'none';
                delete this.editingUserId;
            }
        });
    }
}

// Instância global do gerenciador de usuários
const userManager = new UserManager();
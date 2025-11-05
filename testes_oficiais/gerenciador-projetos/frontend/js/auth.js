const API_BASE = 'http://localhost:3000/api';

// Auth state
let currentUser = null;

// Initialize auth system
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Inicializando sistema de autenticação...');
    initializeAuth();
    checkAuthStatus();
});

function initializeAuth() {
    // Tab switching
    const loginTab = document.getElementById('loginTab');
    const registerTab = document.getElementById('registerTab');

    if (loginTab && registerTab) {
        loginTab.addEventListener('click', function() {
            switchAuthTab('login');
        });

        registerTab.addEventListener('click', function() {
            switchAuthTab('register');
        });
    }

    // Form submissions
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    console.log('✅ Sistema de auth configurado');
}

function switchAuthTab(tab) {
    console.log('📁 Mudando para tab:', tab);

    const loginTab = document.getElementById('loginTab');
    const registerTab = document.getElementById('registerTab');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (tab === 'login') {
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    } else {
        registerTab.classList.add('active');
        loginTab.classList.remove('active');
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    }
}

async function handleLogin(e) {
    e.preventDefault();
    console.log('📤 Iniciando login...');

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        showMessage('❌ Preencha todos os campos', 'error');
        return;
    }

    try {
        showLoading('🔐 Entrando...');

        console.log('📨 Enviando request para:', `${API_BASE}/auth/login`);

        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email.trim(),
                password: password
            })
        });

        console.log('📥 Response status:', response.status);

        const data = await response.json();
        console.log('📦 Response data:', data);

        if (response.ok && data.success) {
            showMessage('🎉 Login realizado!', 'success');
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            currentUser = data.user;

            // Aguardar um pouco para mostrar a mensagem de sucesso
            setTimeout(() => {
                showApp();
            }, 1000);

        } else {
            showMessage(data.error || '❌ Erro no login', 'error');
        }

    } catch (error) {
        console.error('💥 Erro:', error);
        showMessage('🌐 Erro de conexão. Verifique o console.', 'error');
    } finally {
        hideLoading();
    }
}

async function handleRegister(e) {
    e.preventDefault();
    console.log('📤 Iniciando registro...');

    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    if (!name || !email || !password) {
        showMessage('❌ Preencha todos os campos', 'error');
        return;
    }

    if (password.length < 6) {
        showMessage('❌ Senha precisa de 6+ caracteres', 'error');
        return;
    }

    try {
        showLoading('👤 Criando conta...');

        console.log('📨 Enviando registro para:', `${API_BASE}/auth/register`);

        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name.trim(),
                email: email.trim(),
                password: password
            })
        });

        console.log('📥 Response status:', response.status);

        const data = await response.json();
        console.log('📦 Response data:', data);

        if (response.ok && data.success) {
            showMessage('🎉 Conta criada! Faça login.', 'success');
            switchAuthTab('login');
            document.getElementById('registerForm').reset();
        } else {
            showMessage(data.error || '❌ Erro no registro', 'error');
        }

    } catch (error) {
        console.error('💥 Erro:', error);
        showMessage('🌐 Erro de conexão. Verifique o console.', 'error');
    } finally {
        hideLoading();
    }
}

function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');

    console.log('🔍 Verificando autenticação...');
    console.log('Token:', token ? '✅ Presente' : '❌ Ausente');
    console.log('User:', user ? '✅ Presente' : '❌ Ausente');

    if (token && user) {
        try {
            const userData = JSON.parse(user);
            console.log('👤 Usuário:', userData.email);
            currentUser = userData;
            showApp();
        } catch (e) {
            console.error('❌ Erro ao ler usuário:', e);
            showAuth();
        }
    } else {
        showAuth();
    }
}

function showAuth() {
    console.log('🔐 Mostrando tela de login');
    const auth = document.getElementById('authScreen');
    const app = document.getElementById('appScreen');

    if (auth) auth.style.display = 'flex';
    if (app) app.style.display = 'none';
}

function showApp() {
    console.log('🏠 Mostrando aplicação');
    const auth = document.getElementById('authScreen');
    const app = document.getElementById('appScreen');

    if (auth) auth.style.display = 'none';
    if (app) app.style.display = 'block';

    // Atualizar nome do usuário
    const userWelcome = document.getElementById('userWelcome');
    if (userWelcome && currentUser) {
        userWelcome.textContent = `Bem-vindo, ${currentUser.name || 'Usuário'}!`;
    }

    // Configurar features de admin
    setupAdminFeatures();

    // Inicializar Kanban
    if (typeof initializeKanban === 'function') {
        initializeKanban();
    }

    // Mostrar view do Kanban por padrão
    showView('kanban');
}

function logout() {
    console.log('🚪 Saindo...');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    currentUser = null;
    showMessage('👋 Até logo!', 'success');
    setTimeout(showAuth, 1000);
}

// Configurar features de admin
function setupAdminFeatures() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user.role === 'admin') {
        // Mostrar botão de usuários no toggle
        const usersViewBtn = document.getElementById('usersViewBtn');
        if (usersViewBtn) {
            usersViewBtn.style.display = 'block';
        }

        // Inicializar gerenciador de usuários
        if (typeof userManager !== 'undefined') {
            userManager.initialize();
        }
    }
}

// Make functions global
window.showApp = showApp;
window.showAuth = showAuth;
window.logout = logout;
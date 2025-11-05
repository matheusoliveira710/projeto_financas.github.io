const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const userRoutes = require('./routes/users');

// Adicione após as outras rotas
app.use('/api/users', authenticateToken, userRoutes);
// Middleware CORS bem configurado
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Servir arquivos estáticos do frontend
app.use(express.static(path.join(__dirname, '../frontend')));

// ========== ROTAS DA API ==========

// Health Check
app.get('/api/health', (req, res) => {
    res.json({
        status: 'OK',
        message: 'API está funcionando perfeitamente!',
        timestamp: new Date().toISOString()
    });
});

// Test Route
app.get('/api/test', (req, res) => {
    res.json({
        success: true,
        message: '✅ Teste bem-sucedido! A API está respondendo.',
        data: {
            server: 'Node.js',
            status: 'online',
            time: new Date().toISOString()
        }
    });
});

// Mock database
let users = [
    {
        id: 1,
        name: "Admin User",
        email: "admin@projectmanager.com",
        password: "$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi", // password
        role: "admin"
    }
];

let projects = [];

// ========== ROTAS DE AUTENTICAÇÃO ==========

// Register
app.post('/api/auth/register', async (req, res) => {
    console.log('📝 Tentativa de registro:', req.body);

    try {
        const { name, email, password } = req.body;

        // Validação
        if (!name || !email || !password) {
            return res.status(400).json({
                success: false,
                error: 'Todos os campos são obrigatórios'
            });
        }

        // Verificar se usuário já existe
        const existingUser = users.find(user => user.email === email);
        if (existingUser) {
            return res.status(400).json({
                success: false,
                error: 'Usuário já existe'
            });
        }

        // Criar novo usuário
        const newUser = {
            id: users.length + 1,
            name,
            email,
            password, // Em produção, usar bcrypt
            role: 'user',
            createdAt: new Date().toISOString()
        };

        users.push(newUser);

        console.log('✅ Novo usuário criado:', newUser.email);

        res.status(201).json({
            success: true,
            message: 'Usuário criado com sucesso!',
            user: {
                id: newUser.id,
                name: newUser.name,
                email: newUser.email,
                role: newUser.role
            }
        });

    } catch (error) {
        console.error('❌ Erro no registro:', error);
        res.status(500).json({
            success: false,
            error: 'Erro interno do servidor'
        });
    }
});

// Login
app.post('/api/auth/login', async (req, res) => {
    console.log('🔐 Tentativa de login:', req.body);

    try {
        const { email, password } = req.body;

        // Validação
        if (!email || !password) {
            return res.status(400).json({
                success: false,
                error: 'Email e senha são obrigatórios'
            });
        }

        // Buscar usuário
        const user = users.find(u => u.email === email);

        // Credenciais de teste
        if (email === 'admin@projectmanager.com' && password === '123456') {
            const userData = {
                id: 1,
                name: "Administrador",
                email: "admin@projectmanager.com",
                role: "admin"
            };

            console.log('✅ Login bem-sucedido para:', userData.email);

            return res.json({
                success: true,
                message: 'Login realizado com sucesso!',
                token: 'demo-token-' + Date.now(),
                user: userData
            });
        }

        // Verificar se usuário existe e senha está correta
        if (!user || user.password !== password) {
            return res.status(401).json({
                success: false,
                error: 'Credenciais inválidas'
            });
        }

        console.log('✅ Login bem-sucedido para:', user.email);

        res.json({
            success: true,
            message: 'Login realizado com sucesso!',
            token: 'demo-token-' + user.id,
            user: {
                id: user.id,
                name: user.name,
                email: user.email,
                role: user.role
            }
        });

    } catch (error) {
        console.error('❌ Erro no login:', error);
        res.status(500).json({
            success: false,
            error: 'Erro interno do servidor'
        });
    }
});

// ========== ROTAS DE PROJETOS ==========

// Middleware de autenticação simples
const authenticate = (req, res, next) => {
    const token = req.headers.authorization;

    if (!token) {
        return res.status(401).json({
            success: false,
            error: 'Token de autenticação necessário'
        });
    }

    // Token de demonstração - em produção validar JWT
    next();
};

// Get all projects
app.get('/api/projects', authenticate, (req, res) => {
    res.json({
        success: true,
        projects: projects
    });
});

// Create project
app.post('/api/projects', authenticate, (req, res) => {
    const { title, description, deadline, priority } = req.body;

    const newProject = {
        id: projects.length + 1,
        title,
        description,
        deadline,
        priority,
        progress: 0,
        createdAt: new Date().toISOString()
    };

    projects.push(newProject);

    res.status(201).json({
        success: true,
        project: newProject
    });
});

// Dashboard data
app.get('/api/dashboard', authenticate, (req, res) => {
    const dashboardData = {
        activeProjects: projects.length,
        pendingTasks: 12,
        overallProgress: 65,
        recentProjects: projects.slice(-3),
        stats: {
            total: projects.length,
            completed: projects.filter(p => p.progress === 100).length,
            inProgress: projects.filter(p => p.progress > 0 && p.progress < 100).length,
            notStarted: projects.filter(p => p.progress === 0).length
        }
    };

    res.json({
        success: true,
        ...dashboardData
    });
});

// ========== ROTA PADRÃO ==========

// Servir o frontend para todas as outras rotas
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// ========== INICIAR SERVIDOR ==========

app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('🚀 SERVIDOR INICIADO COM SUCESSO!');
    console.log('='.repeat(50));
    console.log(`📡 Porta: ${PORT}`);
    console.log(`🌐 Frontend: http://localhost:${PORT}`);
    console.log(`🔗 API: http://localhost:${PORT}/api`);
    console.log(`🩺 Health: http://localhost:${PORT}/api/health`);
    console.log(`🧪 Test: http://localhost:${PORT}/api/test`);
    console.log('='.repeat(50));
    console.log('👤 Credenciais de teste:');
    console.log('   Email: admin@projectmanager.com');
    console.log('   Senha: 123456');
    console.log('='.repeat(50));
});
const express = require('express');
const bcrypt = require('bcryptjs');
const router = express.Router();

// Mock database - em produção usar PostgreSQL/MongoDB
let users = [
    {
        id: 1,
        name: "Administrador",
        email: "admin@projectmanager.com",
        password: "$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi", // password
        role: "admin",
        createdAt: new Date().toISOString(),
        active: true
    }
];

// Get all users (apenas admin)
router.get('/', authenticateAdmin, (req, res) => {
    res.json({
        success: true,
        users: users.map(user => ({
            id: user.id,
            name: user.name,
            email: user.email,
            role: user.role,
            createdAt: user.createdAt,
            active: user.active
        }))
    });
});

// Create new user
router.post('/', authenticateAdmin, async (req, res) => {
    try {
        const { name, email, password, role = 'user' } = req.body;

        // Validação
        if (!name || !email || !password) {
            return res.status(400).json({
                success: false,
                error: 'Nome, email e senha são obrigatórios'
            });
        }

        if (password.length < 6) {
            return res.status(400).json({
                success: false,
                error: 'A senha deve ter pelo menos 6 caracteres'
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

        // Hash da senha
        const hashedPassword = await bcrypt.hash(password, 10);

        // Criar novo usuário
        const newUser = {
            id: users.length + 1,
            name,
            email,
            password: hashedPassword,
            role,
            createdAt: new Date().toISOString(),
            active: true
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
                role: newUser.role,
                createdAt: newUser.createdAt
            }
        });

    } catch (error) {
        console.error('❌ Erro ao criar usuário:', error);
        res.status(500).json({
            success: false,
            error: 'Erro interno do servidor'
        });
    }
});

// Update user
router.put('/:id', authenticateAdmin, async (req, res) => {
    try {
        const userId = parseInt(req.params.id);
        const { name, email, role, active, password } = req.body;

        const userIndex = users.findIndex(user => user.id === userId);
        if (userIndex === -1) {
            return res.status(404).json({
                success: false,
                error: 'Usuário não encontrado'
            });
        }

        // Atualizar dados do usuário
        if (name) users[userIndex].name = name;
        if (email) users[userIndex].email = email;
        if (role) users[userIndex].role = role;
        if (typeof active === 'boolean') users[userIndex].active = active;

        // Se forneceu nova senha, fazer hash
        if (password) {
            users[userIndex].password = await bcrypt.hash(password, 10);
        }

        users[userIndex].updatedAt = new Date().toISOString();

        res.json({
            success: true,
            message: 'Usuário atualizado com sucesso!',
            user: {
                id: users[userIndex].id,
                name: users[userIndex].name,
                email: users[userIndex].email,
                role: users[userIndex].role,
                active: users[userIndex].active,
                createdAt: users[userIndex].createdAt,
                updatedAt: users[userIndex].updatedAt
            }
        });

    } catch (error) {
        console.error('❌ Erro ao atualizar usuário:', error);
        res.status(500).json({
            success: false,
            error: 'Erro interno do servidor'
        });
    }
});

// Delete user (soft delete)
router.delete('/:id', authenticateAdmin, (req, res) => {
    const userId = parseInt(req.params.id);
    const userIndex = users.findIndex(user => user.id === userId);

    if (userIndex === -1) {
        return res.status(404).json({
            success: false,
            error: 'Usuário não encontrado'
        });
    }

    // Soft delete - marcar como inativo
    users[userIndex].active = false;
    users[userIndex].updatedAt = new Date().toISOString();

    res.json({
        success: true,
        message: 'Usuário desativado com sucesso!'
    });
});

// Middleware para verificar se é admin
function authenticateAdmin(req, res, next) {
    if (req.user.role !== 'admin') {
        return res.status(403).json({
            success: false,
            error: 'Acesso negado. Apenas administradores podem realizar esta ação.'
        });
    }
    next();
}

module.exports = router;
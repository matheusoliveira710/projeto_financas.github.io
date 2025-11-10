const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// --- Configuração Essencial (Middleware) ---
app.use(cors());
app.use(express.json());

// --- 1. Conexão ÚNICA com o MongoDB ---
// O seu log de erro confirma que o banco é 'finance_db'
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/finance_db';

mongoose.connect(MONGODB_URI)
  .then(() => console.log(`✅ Conexão ÚNICA com MongoDB estabelecida em: ${MONGODB_URI}`))
  .catch(err => console.error('❌ Erro ao conectar ao MongoDB:', err));

// --- 2. Definição dos Modelos (Schemas) ---

// NOVO: Schema do Usuário (Sem alterações)
const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: [true, 'Email é obrigatório'],
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: [true, 'Senha é obrigatória']
  }
});
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});
userSchema.methods.comparePassword = function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};
const User = mongoose.model('User', userSchema);

// ****** AQUI ESTÁ A CORREÇÃO ******
const categorySchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  name: { type: String, required: true },
  type: { type: String, enum: ['income', 'expense'], required: true },
  // 1. Removemos o 'unique: true' daqui
  id: { type: Number, required: true }
});

// 2. Adicionamos um "índice composto"
// Isso garante que a combinação de 'user' e 'id' seja única.
// Agora, usuários diferentes PODEM ter categorias com o mesmo 'id'.
categorySchema.index({ user: 1, id: 1 }, { unique: true });
// ****** FIM DA CORREÇÃO ******

const Category = mongoose.model('Category', categorySchema);

// ATUALIZADO: Transação (Sem alterações)
const transactionSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  description: { type: String, required: true },
  amount: { type: Number, required: true },
  type: { type: String, enum: ['income', 'expense'], required: true },
  date: { type: Date, default: Date.now },
  category: { type: String, required: true }
});
const Transaction = mongoose.model('Transaction', transactionSchema);

// --- 3. Middleware de Autenticação (Sem alterações) ---
const protect = async (req, res, next) => {
  let token;
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    try {
      token = req.headers.authorization.split(' ')[1];
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      req.user = await User.findById(decoded.id).select('-password');
      next();
    } catch (error) {
      console.error(error);
      res.status(401).json({ error: 'Não autorizado, token falhou' });
    }
  }
  if (!token) {
    res.status(401).json({ error: 'Não autorizado, sem token' });
  }
};

// --- 4. Rotas da API (Sem alterações) ---

// --- ROTAS DE AUTENTICAÇÃO ---
app.post('/api/auth/register', async (req, res) => {
  const { email, password } = req.body;
  try {
    if (!email || !password) {
      return res.status(400).json({ error: 'Email e senha são obrigatórios' });
    }
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ error: 'Email já cadastrado' });
    }
    const user = await User.create({ email, password });
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '30d' });
    res.status(201).json({
      _id: user._id,
      email: user.email,
      token: token
    });
  } catch (error) {
    res.status(400).json({ error: 'Erro ao registrar usuário: ' + error.message });
  }
});

app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  try {
    const user = await User.findOne({ email });
    if (user && (await user.comparePassword(password))) {
      const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '30d' });
      res.json({
        _id: user._id,
        email: user.email,
        token: token
      });
    } else {
      res.status(401).json({ error: 'Email ou senha inválidos' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Erro no login: ' + error.message });
  }
});

// --- ROTAS DE DADOS (PROTEGIDAS) ---
app.get('/api/health', (req, res) => {
  res.json({
    status: 'OK',
    database: mongoose.connection.readyState === 1 ? 'Conectado' : 'Desconectado'
  });
});

app.get('/api/categories', protect, async (req, res) => {
  try {
    const categories = await Category.find({ user: req.user.id });
    if (categories.length === 0) {
      return res.status(404).json({
        error: 'Nenhuma categoria encontrada para este usuário.',
        action: 'Visite /api/setup/seed-categories (logado) para popular o banco.'
      });
    }
    res.json(categories);
  } catch (error) {
    res.status(500).json({ error: 'Erro ao buscar categorias: ' + error.message });
  }
});

app.get('/api/transactions', protect, async (req, res) => {
  try {
    const transactions = await Transaction.find({ user: req.user.id }).sort({ date: -1 });
    res.json(transactions);
  } catch (error) {
    res.status(500).json({ error: 'Erro ao buscar transações: ' + error.message });
  }
});

app.post('/api/transactions', protect, async (req, res) => {
  try {
    const { description, amount, type, category, date } = req.body;
    const numericAmount = parseFloat(amount);
    if (isNaN(numericAmount)) {
      return res.status(400).json({ error: 'O valor (amount) deve ser um número válido.' });
    }
    if (!description || !type || !category || !date) {
        return res.status(400).json({ error: 'Todos os campos são obrigatórios.' });
    }
    const transaction = new Transaction({
      description: description,
      amount: numericAmount,
      type: type,
      category: category,
      date: date,
      user: req.user.id
    });
    await transaction.save();
    res.status(201).json(transaction);
  } catch (error) {
    console.error('Erro ao salvar transação:', error);
    res.status(400).json({ error: 'Erro ao criar transação: ' + error.message });
  }
});

// ROTA ESPECIAL PARA POPULAR O BANCO (Seed)
app.get('/api/setup/seed-categories', protect, async (req, res) => {
  try {
    // 1. Apaga APENAS as categorias deste usuário
    await Category.deleteMany({ user: req.user.id });
    console.log(`[Seed] Categorias antigas removidas para o usuário: ${req.user.email}`);

    const mockCategories = [
      { id: 1, name: 'Alimentação', type: 'expense' },
      { id: 2, name: 'Transporte', type: 'expense' },
      { id: 3, name: 'Moradia', type: 'expense' },
      { id: 4, name: 'Saúde', type: 'expense' },
      { id: 5, name: 'Educação', type: 'expense' },
      { id: 6, name: 'Lazer', type: 'expense' },
      { id: 7, name: 'Aluguel', type: 'income' },
      { id: 8, name: 'Salário', type: 'income' },
      { id: 9, name: 'Freelance', type: 'income' },
      { id: 10, name: 'Investimentos', type: 'income' },
      { id: 11, name: 'Presente', type: 'income' },
      { id: 12, name: 'Reembolsos', type: 'income'},
      { id: 13, name: 'Bônus', type: 'income'}
    ];

    // 2. Adiciona o ID do usuário
    const categoriesWithUser = mockCategories.map(cat => ({
      ...cat,
      user: req.user.id
    }));

    // 3. Insere as novas
    await Category.insertMany(categoriesWithUser);
    console.log(`[Seed] Novas categorias inseridas para o usuário: ${req.user.email}`);

    res.status(201).json({
      message: 'Banco de dados de Categorias populado com sucesso para o seu usuário!',
      data: categoriesWithUser
    });
  } catch (error) {
    console.error('[Seed] Erro na rota de seed:', error.message);
    res.status(500).json({ error: 'Erro ao popular categorias: ' + error.message });
  }
});

// --- 5. Iniciar o Servidor ---
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Servidor backend rodando em http://0.0.0.0:${PORT}`);
  console.log(`(Conectando ao MongoDB...)`);
  console.log(`---`);
  console.log(`Rotas de Autenticação prontas:`);
  console.log(`  POST /api/auth/register`);
  console.log(`  POST /api/auth/login`);
});
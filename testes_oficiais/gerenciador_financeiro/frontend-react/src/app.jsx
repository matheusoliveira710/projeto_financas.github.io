import React, { useState, useEffect } from 'react';

// URL da API (deve ser o mesmo do seu backend)
const API_URL = 'http://localhost:5000/api';

/**
 * Componente Principal - Gerencia o estado da aplicação
 */
function App() {
  // Estado para o token e informações do usuário
  const [authToken, setAuthToken] = useState(localStorage.getItem('authToken'));
  const [userInfo, setUserInfo] = useState(() => {
    const savedUser = localStorage.getItem('userInfo');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  // Estado para controlar a "página" atual
  const [page, setPage] = useState('loading'); // loading | login | register | finance | admin

  // Efeito para "rotear" o usuário quando o app carrega ou o login muda
  useEffect(() => {
    if (!authToken || !userInfo) {
      setPage('login');
    } else if (userInfo.role === 'admin') {
      setPage('admin');
    } else {
      setPage('finance');
    }
  }, [authToken, userInfo]);

  // Função para lidar com o sucesso do Login/Cadastro
  const handleAuthSuccess = (data) => {
    localStorage.setItem('authToken', data.token);
    localStorage.setItem('userInfo', JSON.stringify(data));
    setAuthToken(data.token);
    setUserInfo(data);
    // O useEffect acima cuidará de definir a página correta (admin ou finance)
  };

  // Função de Logout
  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userInfo');
    setAuthToken(null);
    setUserInfo(null);
    // O useEffect acima cuidará de definir a página para 'login'
  };

  // Função para renderizar a página correta
  const renderPage = () => {
    switch (page) {
      case 'loading':
        return <div className="loading-spinner">Carregando...</div>;
      case 'login':
        return <AuthPage mode="login" onAuthSuccess={handleAuthSuccess} setPage={setPage} />;
      case 'register':
        return <AuthPage mode="register" onAuthSuccess={handleAuthSuccess} setPage={setPage} />;
      case 'admin':
        return <AdminPage authToken={authToken} userInfo={userInfo} onLogout={handleLogout} />;
      case 'finance':
        return <FinancePage authToken={authToken} userInfo={userInfo} onLogout={handleLogout} />;
      default:
        return <AuthPage mode="login" onAuthSuccess={handleAuthSuccess} setPage={setPage} />;
    }
  };

  return (
    <div className="app-container">
      <GlobalStyles />
      {renderPage()}
    </div>
  );
}

// ========================================================================
// NOVO COMPONENTE: PAINEL DE ADMINISTRAÇÃO
// ========================================================================
function AdminPage({ authToken, userInfo, onLogout }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // V V V V V V V CORREÇÃO AQUI V V V V V V V
  // Se o usuário acabou de deslogar, userInfo será null.
  // Retornamos null para não tentar renderizar a página e causar o erro.
  if (!userInfo) {
    return null;
  }
  // ^ ^ ^ ^ ^ ^ ^ FIM DA CORREÇÃO ^ ^ ^ ^ ^ ^ ^

  // Função para buscar a lista de usuários
  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/admin/users`, {
        headers: { 'Authorization': `Bearer ${authToken}` },
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar usuários');
      }
      setUsers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Buscar usuários quando o componente for montado
  useEffect(() => {
    fetchUsers();
  }, [authToken]);

  // Função para deletar um usuário
  const handleDeleteUser = async (userId, userEmail) => {
    // Usamos 'confirm' aqui, mas um modal seria melhor em produção
    if (!window.confirm(`Tem certeza que quer deletar o usuário ${userEmail}? Esta ação é irreversível e deletará todas as finanças dele.`)) {
      return;
    }

    // Proteção de UI (o backend também protege, mas é bom ter nos dois)
    if (userId === userInfo._id) {
      setError('Você não pode deletar a si mesmo.');
      return;
    }

    try {
      setError(null);
      const response = await fetch(`${API_URL}/admin/users/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${authToken}` },
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao deletar usuário');
      }
      // Sucesso! Atualizar a lista de usuários
      fetchUsers();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="admin-page">
      <header className="header">
        <h1>Painel de Admin</h1>
        <p>Gerenciamento de Usuários (Logado como: {userInfo.email})</p>
        <button onClick={onLogout} className="logout-btn">Sair</button>
      </header>

      {loading && <div className="loading-spinner">Carregando usuários...</div>}
      {error && <div className="error-message">{error}</div>}

      <div className="user-list">
        <h2>Usuários Cadastrados ({users.length})</h2>
        {users.map(user => (
          <div key={user._id} className="user-card">
            <div className="user-info">
              <strong className="user-email">{user.email}</strong>
              <span className={`role-badge role-${user.role}`}>{user.role}</span>
              <small className="user-id">ID: {user._id}</small>
            </div>
            <button
              onClick={() => handleDeleteUser(user._id, user.email)}
              disabled={user._id === userInfo._id} // Desabilita o botão para o próprio admin
              className="delete-btn"
            >
              Deletar
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}


// ========================================================================
// COMPONENTE: PÁGINA DE FINANÇAS (O seu app antigo, agora protegido)
// ========================================================================
function FinancePage({ authToken, userInfo, onLogout }) {
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [needsSeed, setNeedsSeed] = useState(false);

  const [formData, setFormData] = useState({
    description: '',
    amount: '',
    type: 'expense',
    category: '',
    date: new Date().toISOString().split('T')[0],
  });

  // Função para carregar dados (Transações e Categorias)
  const loadData = async () => {
    setLoading(true);
    setError('');
    setNeedsSeed(false);
    try {
      // 1. Tentar carregar Categorias
      const categoriesResponse = await fetch(`${API_URL}/categories`, {
        headers: { 'Authorization': `Bearer ${authToken}` },
      });
      if (categoriesResponse.status === 404) {
         setNeedsSeed(true); // Usuário novo, precisa popular o banco
         setCategories([]); // Garante que está vazio
      } else if (categoriesResponse.ok) {
        const categoriesData = await categoriesResponse.json();
        setCategories(categoriesData);
      } else {
        const errData = await categoriesResponse.json();
        throw new Error(errData.error || 'Erro ao carregar categorias');
      }

      // 2. Tentar carregar Transações
      const transactionsResponse = await fetch(`${API_URL}/transactions`, {
        headers: { 'Authorization': `Bearer ${authToken}` },
      });
      if (transactionsResponse.ok) {
        const transactionsData = await transactionsResponse.json();
        setTransactions(transactionsData);
      } else {
         const errData = await transactionsResponse.json();
         throw new Error(errData.error || 'Erro ao carregar transações');
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Carregar dados quando o componente montar
  useEffect(() => {
    loadData();
  }, [authToken]);

  // Função para popular o banco (Seed)
  const handleSeedCategories = async () => {
    setError('');
    try {
      const response = await fetch(`${API_URL}/setup/seed-categories`, {
        method: 'GET', // Usamos GET como definido no backend
        headers: { 'Authorization': `Bearer ${authToken}` },
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Erro ao criar categorias');
      }
      // Sucesso! Recarregar os dados
      loadData();
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  // Lidar com inputs do formulário
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
      ...(name === 'type' && { category: '' }) // Reseta categoria se o tipo mudar
    }));
  };

  // Enviar formulário de transação
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.description || !formData.amount || !formData.category || !formData.date) {
      setError('Por favor, preencha todos os campos');
      return;
    }
    try {
      setError('');
      const response = await fetch(`${API_URL}/transactions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`,
        },
        body: JSON.stringify(formData),
      });

      const newTransaction = await response.json();
      if (!response.ok) {
        throw new Error(newTransaction.error || 'Erro ao salvar transação');
      }

      // Sucesso: Adicionar na lista e resetar form
      setTransactions(prev => [newTransaction, ...prev]);
      setFormData({
        description: '',
        amount: '',
        type: 'expense',
        category: '',
        date: new Date().toISOString().split('T')[0],
      });
    } catch (err) {
      setError(err.message);
    }
  };

  // Calcular totais
  const totals = transactions.reduce((acc, transaction) => {
    const amount = parseFloat(transaction.amount) || 0;
    if (transaction.type === 'income') {
      acc.income += amount;
    } else {
      acc.expenses += amount;
    }
    return acc;
  }, { income: 0, expenses: 0 });
  const balance = totals.income - totals.expenses;

  // Filtrar categorias pelo tipo (Receita/Despesa)
  const getFilteredCategories = () => {
    return categories.filter(cat => cat.type === formData.type);
  };

  // Renderização
  if (loading) {
    return <div className="loading-spinner">Carregando dados financeiros...</div>;
  }

  // Card especial para novos usuários
  if (needsSeed) {
    return (
      <div className="app">
        <header className="header">
          <h1>Bem-vindo, {userInfo.email}!</h1>
          <button onClick={onLogout} className="logout-btn">Sair</button>
        </header>
        <div className="seed-container card">
          <h2>Vamos começar?</h2>
          <p>Parece que você é um novo usuário. Clique no botão abaixo para criar as categorias padrão (Salário, Alimentação, Moradia, etc.) e começar a usar o app.</p>
          <button onClick={handleSeedCategories} className="btn-primary seed-btn">
            Criar Categorias Padrão
          </button>
          {error && <div className="error-message">{error}</div>}
        </div>
      </div>
    );
  }

  // Página principal de finanças
  return (
    <div className="app">
      <header className="header">
        <h1>Meu Painel Financeiro</h1>
        <p>Logado como: {userInfo.email}</p>
        <button onClick={onLogout} className="logout-btn">Sair</button>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="dashboard">
        <div className="card">
          <h3>Saldo Total</h3>
          <div className={`balance ${balance >= 0 ? 'positive' : 'negative'}`}>
            R$ {balance.toFixed(2)}
          </div>
        </div>
        <div className="card">
          <h3>Receitas</h3>
          <div className="balance positive">R$ {totals.income.toFixed(2)}</div>
        </div>
        <div className="card">
          <h3>Despesas</h3>
          <div className="balance negative">R$ {totals.expenses.toFixed(2)}</div>
        </div>
      </div>

      <div className="transaction-form card">
        <h3>Adicionar Transação</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Descrição</label>
            <input type="text" name="description" value={formData.description} onChange={handleInputChange} required />
          </div>
          <div className="form-group">
            <label>Valor (R$)</label>
            <input type="number" name="amount" value={formData.amount} onChange={handleInputChange} step="0.01" required />
          </div>
          <div className="form-group">
            <label>Tipo</label>
            <select name="type" value={formData.type} onChange={handleInputChange}>
              <option value="expense">Despesa</option>
              <option value="income">Receita</option>
            </select>
          </div>
          <div className="form-group">
            <label>Categoria</label>
            <select name="category" value={formData.category} onChange={handleInputChange} required>
              <option value="">Selecione</option>
              {getFilteredCategories().map(cat => (
                <option key={cat._id || cat.id} value={cat.name}>{cat.name}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Data</label>
            <input type="date" name="date" value={formData.date} onChange={handleInputChange} required />
          </div>
          <button type="submit" className="btn-primary">Adicionar</button>
        </form>
      </div>

      <div className="transactions-list card">
        <h3>Últimas Transações</h3>
        {transactions.length === 0 ? (
          <p>Nenhuma transação encontrada.</p>
        ) : (
          transactions.map(t => (
            <div key={t._id || t.id} className="transaction-item">
              <div className="transaction-info">
                <span className="transaction-description">{t.description}</span>
                <span className="transaction-category">{t.category} • {new Date(t.date).toLocaleDateString('pt-BR')}</span>
              </div>
              <div className={`transaction-amount ${t.type === 'income' ? 'positive' : 'negative'}`}>
                {t.type === 'income' ? '+' : '-'} R$ {parseFloat(t.amount).toFixed(2)}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}


// ========================================================================
// COMPONENTE: PÁGINA DE AUTENTICAÇÃO (Login / Cadastro)
// ========================================================================
function AuthPage({ mode, onAuthSuccess, setPage }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const isLogin = mode === 'login';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!isLogin && password !== confirmPassword) {
      setError('As senhas não conferem!');
      setLoading(false);
      return;
    }

    const endpoint = isLogin ? '/auth/login' : '/auth/register';

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Algo deu errado');
      }

      // Sucesso! Chama a função do componente App
      onAuthSuccess(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <form className="auth-form card" onSubmit={handleSubmit}>
        <h1>{isLogin ? 'Login' : 'Cadastro'}</h1>
        <p>{isLogin ? 'Entre na sua conta' : 'Crie uma nova conta'}</p>

        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Senha</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {!isLogin && (
          <div className="form-group">
            <label>Confirmar Senha</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
        )}

        {error && <div className="error-message">{error}</div>}

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Carregando...' : (isLogin ? 'Entrar' : 'Cadastrar')}
        </button>

        <div className="auth-switch">
          {isLogin ? (
            <p>Não tem uma conta? <span onClick={() => setPage('register')}>Cadastre-se</span></p>
          ) : (
            <p>Já tem uma conta? <span onClick={() => setPage('login')}>Faça login</span></p>
          )}
        </div>
      </form>
    </div>
  );
}


// ========================================================================
// ESTILOS GLOBAIS (CSS-in-JS)
// ========================================================================
function GlobalStyles() {
  return (
    <style>{`
      /* --- Reset Básico e Variáveis --- */
      :root {
        --cor-primaria: #4f46e5;
        --cor-primaria-hover: #4338ca;
        --cor-sucesso: #10b981;
        --cor-erro: #ef4444;
        --cor-fundo: #f3f4f6;
        --cor-fundo-card: #ffffff;
        --cor-texto: #1f2937;
        --cor-texto-claro: #6b7280;
        --cor-borda: #e5e7eb;
      }
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        background-color: var(--cor-fundo);
        color: var(--cor-texto);
        line-height: 1.6;
      }
      input, button, select {
        font-family: inherit;
        font-size: 1rem;
        border-radius: 8px;
        border: 1px solid var(--cor-borda);
        padding: 0.75rem 1rem;
      }
      .card {
        background-color: var(--cor-fundo-card);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
      }
      .btn-primary {
        background-color: var(--cor-primaria);
        color: white;
        border: none;
        cursor: pointer;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: background-color 0.2s;
      }
      .btn-primary:hover, .btn-primary:focus {
        background-color: var(--cor-primaria-hover);
      }
      .btn-primary:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
      .form-group {
        margin-bottom: 1rem;
      }
      .form-group label {
        display: block;
        font-weight: 500;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
      }
      .form-group input, .form-group select {
        width: 100%;
      }
      .error-message {
        color: var(--cor-erro);
        background-color: #fee2e2;
        border: 1px solid var(--cor-erro);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
      }
      .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        font-size: 1.5rem;
        font-weight: 600;
      }
      .header {
        background-color: var(--cor-fundo-card);
        padding: 1.5rem 2rem;
        border-bottom: 1px solid var(--cor-borda);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
      }
      .header h1 { font-size: 1.75rem; }
      .header p { color: var(--cor-texto-claro); }
      .logout-btn {
        background: #f1f5f9;
        color: var(--cor-texto);
        border: 1px solid var(--cor-borda);
        padding: 0.5rem 1rem;
        font-weight: 500;
        cursor: pointer;
      }
      .logout-btn:hover { background: #e2e8f0; }

      /* --- Estilos da Página de Autenticação --- */
      .auth-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 2rem;
      }
      .auth-form {
        width: 100%;
        max-width: 400px;
        text-align: center;
      }
      .auth-form h1 { margin-bottom: 0.5rem; }
      .auth-form p { margin-bottom: 1.5rem; color: var(--cor-texto-claro); }
      .auth-form .btn-primary { width: 100%; }
      .auth-switch {
        margin-top: 1.5rem;
        color: var(--cor-texto-claro);
      }
      .auth-switch span {
        color: var(--cor-primaria);
        font-weight: 600;
        cursor: pointer;
      }

      /* --- Estilos da Página de Finanças --- */
      .app { max-width: 1000px; margin: 0 auto; padding: 0 1rem; }
      .dashboard {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
      }
      .balance { font-size: 1.75rem; font-weight: 700; }
      .positive { color: var(--cor-sucesso); }
      .negative { color: var(--cor-erro); }
      .transaction-form form {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
      }
      .transaction-form .form-group:nth-of-type(1) { grid-column: 1 / -1; }
      .transaction-form button { grid-column: 1 / -1; }
      .transaction-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid var(--cor-borda);
      }
      .transaction-item:last-child { border-bottom: none; }
      .transaction-info { display: flex; flex-direction: column; }
      .transaction-description { font-weight: 600; }
      .transaction-category { font-size: 0.875rem; color: var(--cor-texto-claro); }
      .transaction-amount { font-weight: 600; }
      .seed-container { text-align: center; }
      .seed-btn { font-size: 1.1rem; padding: 1rem 2rem; }

      /* --- NOVOS Estilos da Página de Admin --- */
      .admin-page { max-width: 900px; margin: 0 auto; padding: 0 1rem; }
      .user-list {
        background-color: var(--cor-fundo-card);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.07);
      }
      .user-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid var(--cor-borda);
      }
      .user-card:last-child { border-bottom: none; }
      .user-info { display: flex; flex-direction: column; gap: 0.25rem; }
      .user-email { font-weight: 600; }
      .user-id { font-size: 0.75rem; color: #9ca3af; }
      .role-badge {
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.15rem 0.5rem;
        border-radius: 1rem;
        text-transform: uppercase;
        width: fit-content;
      }
      .role-admin { background-color: #fef08a; color: #a16207; }
      .role-user { background-color: #e0e7ff; color: var(--cor-primaria); }
      .delete-btn {
        background-color: #fee2e2;
        color: var(--cor-erro);
        border: 1px solid var(--cor-erro);
        font-weight: 500;
        cursor: pointer;
      }
      .delete-btn:hover { background-color: #fecaca; }
      .delete-btn:disabled {
        background-color: var(--cor-borda);
        color: var(--cor-texto-claro);
        border-color: #d1d5db;
        cursor: not-allowed;
      }

      /* Media Queries para Responsividade */
      @media (max-width: 768px) {
        .header { flex-direction: column; gap: 0.5rem; text-align: center; }
        .transaction-form form { grid-template-columns: 1fr; }
        .transaction-form .form-group:nth-of-type(1) { grid-column: 1; }
        .transaction-form button { grid-column: 1; }
      }
    `}</style>
  );
}

export default App;
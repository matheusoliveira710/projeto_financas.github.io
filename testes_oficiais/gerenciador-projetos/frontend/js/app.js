const API_BASE = 'http://localhost:3000/api';

// DOM Elements
let currentUser = null;

// Initialize App
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
    initializeCharts();
});

// Auth Functions
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
        currentUser = JSON.parse(user);
        showApp();
    } else {
        showAuth();
    }
}

function showAuth() {
    document.getElementById('authScreen').style.display = 'flex';
    document.getElementById('appScreen').style.display = 'none';
}

function showApp() {
    document.getElementById('authScreen').style.display = 'none';
    document.getElementById('appScreen').style.display = 'block';
    document.getElementById('userName').textContent = currentUser.name;
    loadDashboard();
}

// Navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Add active class to clicked nav item
    event.target.classList.add('active');
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

// Modal Functions
function showProjectModal() {
    document.getElementById('projectModal').style.display = 'block';
}

function closeProjectModal() {
    document.getElementById('projectModal').style.display = 'none';
    document.getElementById('projectForm').reset();
}

// Dashboard Functions
async function loadDashboard() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/dashboard`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            updateDashboard(data);
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function updateDashboard(data) {
    document.getElementById('activeProjectsCount').textContent = data.activeProjects;
    document.getElementById('pendingTasksCount').textContent = data.pendingTasks;
    document.getElementById('overallProgress').textContent = `${data.overallProgress}%`;
    
    updateRecentProjects(data.recentProjects);
    updateCharts(data.chartData);
}

function updateRecentProjects(projects) {
    const container = document.getElementById('recentProjectsList');
    container.innerHTML = projects.map(project => `
        <div class="project-card">
            <div class="project-header">
                <h4 class="project-title">${project.title}</h4>
                <span class="project-priority priority-${project.priority}">
                    ${project.priority}
                </span>
            </div>
            <p class="project-description">${project.description}</p>
            <div class="project-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${project.progress}%"></div>
                </div>
            </div>
            <div class="project-footer">
                <span>Vence: ${new Date(project.deadline).toLocaleDateString()}</span>
                <span>${project.progress}%</span>
            </div>
        </div>
    `).join('');
}

function initializeCharts() {
    // Progress Chart
    const progressCtx = document.getElementById('progressChart').getContext('2d');
    window.progressChart = new Chart(progressCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Progresso',
                data: [],
                borderColor: '#4361ee',
                tension: 0.1
            }]
        }
    });
    
    // Tasks Chart
    const tasksCtx = document.getElementById('tasksChart').getContext('2d');
    window.tasksChart = new Chart(tasksCtx, {
        type: 'doughnut',
        data: {
            labels: ['Concluídas', 'Pendentes', 'Atrasadas'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: ['#4cc9f0', '#4361ee', '#f72585']
            }]
        }
    });
}

function updateCharts(chartData) {
    if (window.progressChart && chartData.progress) {
        window.progressChart.data.labels = chartData.progress.labels;
        window.progressChart.data.datasets[0].data = chartData.progress.data;
        window.progressChart.update();
    }
    
    if (window.tasksChart && chartData.tasks) {
        window.tasksChart.data.datasets[0].data = chartData.tasks;
        window.tasksChart.update();
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('projectModal');
    if (event.target === modal) {
        closeProjectModal();
    }
}

// Enhanced Dashboard Functions
function initializeDashboardCharts() {
    // Progress Chart
    const progressCtx = document.getElementById('progressChart');
    if (progressCtx) {
        window.progressChart = new Chart(progressCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                datasets: [{
                    label: 'Progresso dos Projetos',
                    data: [30, 45, 60, 75, 65, 80],
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    // Tasks Chart
    const tasksCtx = document.getElementById('tasksChart');
    if (tasksCtx) {
        window.tasksChart = new Chart(tasksCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Concluídas', 'Em Progresso', 'Pendentes', 'Atrasadas'],
                datasets: [{
                    data: [45, 30, 15, 10],
                    backgroundColor: [
                        '#4cc9f0',
                        '#4361ee',
                        '#ffb703',
                        '#f72585'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Initialize progress rings
    initializeProgressRings();
}

function initializeProgressRings() {
    const rings = document.querySelectorAll('.progress-ring');
    rings.forEach(ring => {
        const progress = ring.querySelector('.ring-progress');
        const text = ring.querySelector('.ring-text');
        const radius = progress.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;

        progress.style.strokeDasharray = circumference;
        progress.style.strokeDashoffset = circumference;

        const progressValue = parseInt(text.textContent);
        const offset = circumference - (progressValue / 100) * circumference;
        progress.style.strokeDashoffset = offset;
    });
}

// Update the existing loadDashboard function
async function loadDashboard() {
    try {
        showLoading();
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE}/dashboard`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            updateDashboard(data);
            initializeDashboardCharts();
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        // Load sample data for demo
        loadSampleDashboardData();
    } finally {
        hideLoading();
    }
}

function loadSampleDashboardData() {
    const sampleData = {
        activeProjects: 8,
        pendingTasks: 15,
        overallProgress: 72,
        recentProjects: [
            {
                id: 1,
                title: "Website Redesign",
                description: "Redesign completo do website corporativo",
                priority: "high",
                deadline: "2024-02-15",
                progress: 75,
                team: ['JD', 'AS', 'MR']
            },
            {
                id: 2,
                title: "Mobile App Development",
                description: "Desenvolvimento do aplicativo móvel",
                priority: "medium",
                deadline: "2024-03-01",
                progress: 45,
                team: ['TP', 'KL']
            },
            {
                id: 3,
                title: "Database Migration",
                description: "Migração para novo sistema de banco de dados",
                priority: "high",
                deadline: "2024-01-30",
                progress: 90,
                team: ['WS', 'RG', 'MN', 'OP']
            }
        ],
        chartData: {
            progress: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                data: [30, 45, 60, 75, 65, 80]
            },
            tasks: [45, 30, 15, 10]
        }
    };

    updateDashboard(sampleData);
    initializeDashboardCharts();
}

// Add loading states
function showLoading() {
    // Implement loading indicators
    const sections = document.querySelectorAll('.section.active .stats-grid, .section.active .projects-grid');
    sections.forEach(section => {
        section.innerHTML = '<div class="loading"></div>';
    });
}

function hideLoading() {
    // Remove loading indicators
    const loaders = document.querySelectorAll('.loading');
    loaders.forEach(loader => loader.remove());
}

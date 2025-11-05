const express = require('express');
const router = express.Router();

// Mock database - replace with real database
const projects = [];

// Get all projects
router.get('/', (req, res) => {
    res.json(projects);
});

// Create new project
router.post('/', (req, res) => {
    try {
        const { title, description, deadline, priority } = req.body;

        const project = {
            id: projects.length + 1,
            title,
            description,
            deadline,
            priority,
            progress: 0,
            createdAt: new Date().toISOString(),
            userId: req.user.id
        };

        projects.push(project);

        res.status(201).json(project);
    } catch (error) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Get project by ID
router.get('/:id', (req, res) => {
    const project = projects.find(p => p.id === parseInt(req.params.id));

    if (!project) {
        return res.status(404).json({ error: 'Project not found' });
    }

    res.json(project);
});

// Update project
router.put('/:id', (req, res) => {
    const projectIndex = projects.findIndex(p => p.id === parseInt(req.params.id));

    if (projectIndex === -1) {
        return res.status(404).json({ error: 'Project not found' });
    }

    projects[projectIndex] = { ...projects[projectIndex], ...req.body };

    res.json(projects[projectIndex]);
});

// Delete project
router.delete('/:id', (req, res) => {
    const projectIndex = projects.findIndex(p => p.id === parseInt(req.params.id));

    if (projectIndex === -1) {
        return res.status(404).json({ error: 'Project not found' });
    }

    projects.splice(projectIndex, 1);

    res.json({ message: 'Project deleted successfully' });
});

module.exports = router;
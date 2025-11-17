/**
 * Agent-Cleo v2.0 - Frontend Application
 * Professional UX with Studio55IQ Integration
 */

// Global state
const state = {
    agents: [],
    selectedAgent: null,
    chatSessionId: null,
    currentSection: 'dashboard',
    currentVisualization: null
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Agent-Cleo v2.0 initializing...');
    await loadAgents();
    await updateDashboard();
});

// ============================================================================
// NAVIGATION
// ============================================================================

function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });

    // Show selected section
    document.getElementById(`section-${sectionName}`).classList.add('active');

    // Update sidebar icons
    document.querySelectorAll('.sidebar-icon').forEach(icon => {
        icon.classList.remove('active');
    });
    event.target.closest('.sidebar-icon').classList.add('active');

    state.currentSection = sectionName;

    // Load section-specific data
    if (sectionName === 'agents') {
        loadAgentsGrid();
    } else if (sectionName === 'chat') {
        loadChatAgentList();
    }
}

// ============================================================================
// AGENT MANAGEMENT
// ============================================================================

async function initializeAgents() {
    try {
        const btn = event.target;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Initializing...';
        btn.disabled = true;

        const response = await fetch('/api/agents/initialize', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showNotification('success', `Initialized ${data.created + data.updated} agents`);
            await loadAgents();
            await updateDashboard();
        } else {
            showNotification('error', 'Failed to initialize agents');
        }

        btn.innerHTML = originalText;
        btn.disabled = false;

    } catch (error) {
        console.error('Error initializing agents:', error);
        showNotification('error', 'Failed to initialize agents');
    }
}

async function loadAgents() {
    try {
        const response = await fetch('/api/agents');
        state.agents = await response.json();

        // Update agent count
        document.getElementById('agent-count').textContent = `${state.agents.length} agents`;

        // Update system status
        const activeAgents = state.agents.filter(a => a.status === 'working').length;
        const statusEl = document.getElementById('system-status');
        statusEl.className = 'agent-status ' + (activeAgents > 0 ? 'status-working' : 'status-idle');

        return state.agents;

    } catch (error) {
        console.error('Error loading agents:', error);
        return [];
    }
}

async function loadAgentsGrid() {
    const container = document.getElementById('agents-grid');
    if (!state.agents.length) {
        container.innerHTML = `
            <div class="col-span-full text-center text-gray-400 py-8">
                <i class="fas fa-robot text-4xl mb-2"></i>
                <p>No agents found. Click "Initialize Agents" to discover agents.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = state.agents.map(agent => `
        <div class="card p-6 agent-card" onclick="selectAgent(${agent.id})">
            <div class="flex items-start justify-between mb-3">
                <div class="flex items-center space-x-2">
                    <span class="agent-status status-${agent.status}"></span>
                    <h3 class="font-bold text-lg">${agent.name}</h3>
                </div>
                <span class="tier-badge tier-${agent.tier}">${agent.tier}</span>
            </div>
            <p class="text-sm text-gray-600 mb-4">${agent.description || 'No description'}</p>
            ${agent.capabilities && agent.capabilities.length > 0 ? `
                <div class="flex flex-wrap gap-2 mb-3">
                    ${agent.capabilities.slice(0, 3).map(cap => `
                        <span class="text-xs px-2 py-1 rounded-full bg-gray-100">${cap}</span>
                    `).join('')}
                    ${agent.capabilities.length > 3 ? `<span class="text-xs text-gray-500">+${agent.capabilities.length - 3} more</span>` : ''}
                </div>
            ` : ''}
            <div class="text-xs text-gray-500 mt-4 pt-4 border-t">
                ${agent.last_active ? `Last active: ${formatDate(agent.last_active)}` : 'Never active'}
            </div>
        </div>
    `).join('');
}

function filterAgents() {
    const tierFilter = document.getElementById('filter-tier').value;
    const statusFilter = document.getElementById('filter-status').value;

    const filtered = state.agents.filter(agent => {
        if (tierFilter && agent.tier !== tierFilter) return false;
        if (statusFilter && agent.status !== statusFilter) return false;
        return true;
    });

    // Update grid with filtered agents
    const container = document.getElementById('agents-grid');
    container.innerHTML = filtered.map(agent => {
        // Same card HTML as in loadAgentsGrid
        return `<div class="card p-6 agent-card" onclick="selectAgent(${agent.id})">...</div>`;
    }).join('');
}

function selectAgent(agentId) {
    state.selectedAgent = state.agents.find(a => a.id === agentId);
    console.log('Selected agent:', state.selectedAgent);
    // Could show agent details modal or switch to chat view
}

// ============================================================================
// DASHBOARD
// ============================================================================

async function updateDashboard() {
    // Update stats
    document.getElementById('stat-total-agents').textContent = state.agents.length;

    const activeAgents = state.agents.filter(a => a.status === 'working').length;
    document.getElementById('stat-active-agents').textContent = activeAgents;

    // Load activities count
    try {
        const response = await fetch('/api/activities?limit=10');
        const activities = await response.json();
        document.getElementById('stat-activities').textContent = activities.length;
    } catch (error) {
        console.error('Error loading activities:', error);
    }

    // Display agent overview by tier
    const dashboard = document.getElementById('dashboard-agents');
    if (!state.agents.length) return;

    const tierGroups = {
        master: [],
        personal: [],
        team: [],
        worker: [],
        expert: []
    };

    state.agents.forEach(agent => {
        if (tierGroups[agent.tier]) {
            tierGroups[agent.tier].push(agent);
        }
    });

    dashboard.innerHTML = Object.entries(tierGroups)
        .filter(([tier, agents]) => agents.length > 0)
        .map(([tier, agents]) => `
            <div class="card p-4">
                <span class="tier-badge tier-${tier} mb-3 inline-block">${tier}</span>
                <div class="text-2xl font-bold">${agents.length}</div>
                <div class="text-sm text-gray-500">${agents.filter(a => a.status === 'working').length} active</div>
            </div>
        `).join('');
}

// ============================================================================
// CHAT
// ============================================================================

function loadChatAgentList() {
    const container = document.getElementById('chat-agent-list');

    if (!state.agents.length) {
        container.innerHTML = '<p class="text-gray-400 text-sm">No agents available</p>';
        return;
    }

    container.innerHTML = state.agents.map(agent => `
        <div class="flex items-center space-x-3 p-3 rounded-lg cursor-pointer hover:bg-gray-50"
             onclick="selectChatAgent(${agent.id})">
            <span class="agent-status status-${agent.status}"></span>
            <div class="flex-grow">
                <div class="font-medium text-sm">${agent.name}</div>
                <div class="text-xs text-gray-500">${agent.tier}</div>
            </div>
        </div>
    `).join('');
}

function selectChatAgent(agentId) {
    state.selectedAgent = state.agents.find(a => a.id === agentId);
    state.chatSessionId = null; // Start new session

    document.getElementById('chat-agent-name').textContent = state.selectedAgent.name;
    document.getElementById('chat-agent-tier').textContent = state.selectedAgent.tier;

    // Clear messages
    document.getElementById('chat-messages').innerHTML = `
        <div class="text-center text-gray-400 py-8">
            <p>Chat with ${state.selectedAgent.name}</p>
        </div>
    `;
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message || !state.selectedAgent) return;

    // Add user message to UI
    addChatMessage('user', message);
    input.value = '';

    // Show typing indicator
    const typingId = addChatMessage('agent', '<i class="fas fa-ellipsis-h fa-pulse"></i>');

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                agent_id: state.selectedAgent.id,
                message: message,
                session_id: state.chatSessionId,
                use_rag: document.getElementById('chat-use-rag').checked
            })
        });

        const data = await response.json();
        state.chatSessionId = data.session_id;

        // Remove typing indicator
        document.getElementById(typingId).remove();

        // Add agent response
        addChatMessage('agent', data.message);

    } catch (error) {
        console.error('Error sending message:', error);
        document.getElementById(typingId).remove();
        addChatMessage('agent', 'Sorry, I encountered an error. Please try again.');
    }
}

function addChatMessage(role, content) {
    const container = document.getElementById('chat-messages');
    const messageId = `msg-${Date.now()}`;

    // Clear empty state if present
    if (container.querySelector('.text-gray-400')) {
        container.innerHTML = '';
    }

    const messageDiv = document.createElement('div');
    messageDiv.id = messageId;
    messageDiv.className = `chat-message message-${role}`;
    messageDiv.innerHTML = `
        <div class="message-bubble">
            ${content}
        </div>
        <div class="text-xs text-gray-400 mt-1">${new Date().toLocaleTimeString()}</div>
    `;

    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;

    return messageId;
}

// ============================================================================
// VISUALIZATIONS
// ============================================================================

async function showVisualization(type) {
    state.currentVisualization = type;
    const container = document.getElementById('visualization-container');

    container.innerHTML = '<div class="flex items-center justify-center h-full"><div class="spinner"></div></div>';

    try {
        if (type === 'network') {
            await renderNetworkGraph(container);
        } else if (type === 'hierarchy') {
            await renderOrgChart(container);
        } else if (type === 'kanban') {
            await renderKanban(container);
        } else if (type === 'grid') {
            await renderGrid(container);
        }
    } catch (error) {
        console.error('Error rendering visualization:', error);
        container.innerHTML = '<div class="text-center text-red-500">Failed to load visualization</div>';
    }
}

async function renderNetworkGraph(container) {
    const response = await fetch('/api/agents/visualization/graph');
    const data = await response.json();

    container.innerHTML = '<svg id="network-svg"></svg>';

    const width = container.clientWidth;
    const height = container.clientHeight;

    const svg = d3.select('#network-svg')
        .attr('width', width)
        .attr('height', height);

    // D3 force simulation
    const simulation = d3.forceSimulation(data.nodes)
        .force('link', d3.forceLink(data.edges).id(d => d.id))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2));

    // Draw edges
    const links = svg.append('g')
        .selectAll('line')
        .data(data.edges)
        .enter().append('line')
        .attr('stroke', '#999')
        .attr('stroke-width', 2);

    // Draw nodes
    const nodes = svg.append('g')
        .selectAll('circle')
        .data(data.nodes)
        .enter().append('circle')
        .attr('r', 20)
        .attr('fill', d => getTierColor(d.tier))
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    // Add labels
    const labels = svg.append('g')
        .selectAll('text')
        .data(data.nodes)
        .enter().append('text')
        .text(d => d.name)
        .attr('font-size', 12)
        .attr('dx', 25)
        .attr('dy', 5);

    simulation.on('tick', () => {
        links
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        nodes
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);

        labels
            .attr('x', d => d.x)
            .attr('y', d => d.y);
    });

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

async function renderOrgChart(container) {
    const response = await fetch('/api/agents/visualization/hierarchy');
    const data = await response.json();

    container.innerHTML = `
        <div class="h-full overflow-auto">
            <div class="flex justify-center">
                ${renderOrgNode(data[0])}
            </div>
        </div>
    `;
}

function renderOrgNode(node) {
    return `
        <div class="flex flex-col items-center">
            <div class="card p-4 m-2 text-center" style="min-width: 150px;">
                <div class="agent-status status-${node.status} mx-auto mb-2"></div>
                <div class="font-bold text-sm">${node.name}</div>
                <span class="tier-badge tier-${node.tier} text-xs mt-2">${node.tier}</span>
            </div>
            ${node.children && node.children.length > 0 ? `
                <div class="flex">
                    ${node.children.map(child => renderOrgNode(child)).join('')}
                </div>
            ` : ''}
        </div>
    `;
}

async function renderKanban(container) {
    const response = await fetch('/api/agents/visualization/kanban');
    const data = await response.json();

    const columns = [
        { key: 'idle', title: 'Idle', color: 'gray' },
        { key: 'working', title: 'Working', color: 'green' },
        { key: 'waiting', title: 'Waiting', color: 'yellow' },
        { key: 'error', title: 'Error', color: 'red' }
    ];

    container.innerHTML = `
        <div class="grid grid-cols-4 gap-4 h-full">
            ${columns.map(col => `
                <div class="card p-4">
                    <h3 class="font-bold mb-4 text-${col.color}-600">${col.title} (${data[col.key].length})</h3>
                    <div class="space-y-2">
                        ${data[col.key].map(agent => `
                            <div class="bg-white p-3 rounded border">
                                <div class="font-medium text-sm">${agent.name}</div>
                                <span class="tier-badge tier-${agent.tier} text-xs mt-1">${agent.tier}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

async function renderGrid(container) {
    await loadAgentsGrid(); // Reuse the grid rendering
    const gridHTML = document.getElementById('agents-grid').innerHTML;
    container.innerHTML = `<div class="grid grid-cols-4 gap-4 h-full overflow-auto">${gridHTML}</div>`;
}

// ============================================================================
// UTILITIES
// ============================================================================

function getTierColor(tier) {
    const colors = {
        master: '#8B5CF6',
        personal: '#06B6D4',
        team: '#10B981',
        worker: '#F59E0B',
        expert: '#EF4444'
    };
    return colors[tier] || '#6B7280';
}

function formatDate(dateString) {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleString();
}

function showNotification(type, message) {
    // Simple notification (could be enhanced with a toast library)
    const color = type === 'success' ? 'green' : 'red';
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 bg-${color}-500 text-white px-6 py-3 rounded-lg shadow-lg z-50`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// ============================================================================
// DOCUMENT UPLOAD
// ============================================================================

async function uploadDocuments() {
    const fileInput = document.getElementById('file-upload');
    const files = fileInput.files;

    if (files.length === 0) return;

    const formData = new FormData();
    for (let file of files) {
        formData.append('files', file);
    }

    try {
        const response = await fetch('/api/documents/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        showNotification('success', `Uploaded ${files.length} document(s)`);
    } catch (error) {
        console.error('Upload error:', error);
        showNotification('error', 'Failed to upload documents');
    }
}

// ============================================================================
// THEME SYSTEM (Vibeship-inspired)
// ============================================================================

class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'purple';
        this.currentMode = localStorage.getItem('mode') || 'light';
        this.init();
    }

    init() {
        // Apply saved theme
        this.applyTheme(this.currentTheme, this.currentMode);

        // Setup event listeners
        this.setupListeners();

        // Highlight current selections
        this.updateUI();
    }

    setupListeners() {
        // Toggle button
        const toggleBtn = document.getElementById('theme-toggle-btn');
        const panel = document.getElementById('theme-panel');

        toggleBtn.addEventListener('click', () => {
            const isVisible = panel.style.display !== 'none';
            panel.style.display = isVisible ? 'none' : 'block';
        });

        // Close panel when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.theme-switcher')) {
                panel.style.display = 'none';
            }
        });

        // Theme options
        document.querySelectorAll('.theme-option').forEach(button => {
            button.addEventListener('click', () => {
                const theme = button.dataset.theme;
                this.setTheme(theme);
            });

            // Hover effect
            button.addEventListener('mouseenter', () => {
                button.style.transform = 'scale(1.05)';
            });
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'scale(1)';
            });
        });

        // Mode options
        document.querySelectorAll('.mode-option').forEach(button => {
            button.addEventListener('click', () => {
                const mode = button.dataset.mode;
                this.setMode(mode);
            });
        });
    }

    setTheme(theme) {
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        this.applyTheme(theme, this.currentMode);
        this.updateUI();
    }

    setMode(mode) {
        this.currentMode = mode;
        localStorage.setItem('mode', mode);
        this.applyTheme(this.currentTheme, mode);
        this.updateUI();
    }

    applyTheme(theme, mode) {
        const root = document.documentElement;
        const themeString = `${theme}-${mode}`;

        // Set data-theme attribute
        root.setAttribute('data-theme', themeString);

        // Also apply dark class if in dark mode (for backward compatibility)
        if (mode === 'dark') {
            root.classList.add('dark');
        } else {
            root.classList.remove('dark');
        }

        console.log(`Applied theme: ${themeString}`);
    }

    updateUI() {
        // Highlight active theme
        document.querySelectorAll('.theme-option').forEach(button => {
            const isActive = button.dataset.theme === this.currentTheme;
            button.style.borderColor = isActive ? 'hsl(var(--primary))' : 'hsl(var(--border))';
            button.style.borderWidth = isActive ? '3px' : '2px';
        });

        // Highlight active mode
        document.querySelectorAll('.mode-option').forEach(button => {
            const isActive = button.dataset.mode === this.currentMode;
            button.style.background = isActive ? 'hsl(var(--accent))' : 'hsl(var(--card))';
            button.style.color = isActive ? 'hsl(var(--accent-foreground))' : 'hsl(var(--foreground))';
            button.style.borderColor = isActive ? 'hsl(var(--accent))' : 'hsl(var(--border))';
        });
    }
}

// Initialize theme manager when DOM is ready
let themeManager;
document.addEventListener('DOMContentLoaded', () => {
    themeManager = new ThemeManager();
});

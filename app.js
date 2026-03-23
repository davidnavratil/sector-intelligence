// ==================== APP.JS ====================
// Navigation, Charts, Interactivity

// Chart.js defaults
Chart.defaults.color = '#64748b';
Chart.defaults.borderColor = '#e2e8f0';
Chart.defaults.font.family = 'Inter';
Chart.defaults.font.size = 11;
Chart.defaults.plugins.legend.labels.boxWidth = 12;
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.scale.grid = { color: 'rgba(226, 232, 240, 0.5)' };

const chartInstances = {};

// ==================== NAVIGATION ====================
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    const page = document.getElementById('page-' + pageId);
    if (page) {
        page.classList.add('active');
        page.classList.remove('fade-in');
        void page.offsetWidth; // force reflow
        page.classList.add('fade-in');
    }

    const navItems = document.querySelectorAll('.nav-item');
    const pageIndex = { dashboard: 0, data: 1, foresight: 2, supply: 3, news: 4, banking: 5, documents: 6 };
    if (navItems[pageIndex[pageId]]) {
        navItems[pageIndex[pageId]].classList.add('active');
    }

    const titles = {
        dashboard: ['Executive Dashboard', 'Automotive sektor — Česká republika, EU, Svět'],
        data: ['Data Explorer', 'Interaktivní průzkum dat automotive sektoru'],
        foresight: ['Foresighting & Scénáře', 'Trendy, predikce a scénářové plánování'],
        supply: ['Supply Chain', 'Hodnotový řetězec, rizika a příležitosti'],
        news: ['News & Alerts', 'Automatizovaný monitoring trendů a událostí'],
        banking: ['Banking Implications', 'Dopad na portfolio a obchodní příležitosti ČS'],
        documents: ['Reporty ke stažení', 'Zdrojové sektorové reporty pro automobilový průmysl'],
    };
    document.getElementById('page-title').textContent = titles[pageId]?.[0] || '';
    document.getElementById('page-subtitle').textContent = titles[pageId]?.[1] || '';

    // Initialize charts for the page
    setTimeout(() => initPageCharts(pageId), 100);
}

// ==================== DASHBOARD INIT ====================
function initDashboard() {
    // Metrics table
    const tbody = document.getElementById('metrics-table');
    tbody.innerHTML = METRICS.map(m => `
        <tr class="border-b border-cs-border/30 hover:bg-gray-50 transition-colors">
            <td class="py-3 pl-4 font-medium">${m.name}</td>
            <td class="text-center font-semibold text-gray-900">${m.value}</td>
            <td class="text-center ${m.yoy.startsWith('+') ? 'text-green-600' : m.yoy.startsWith('-') ? 'text-red-600' : 'text-yellow-600'}">${m.yoy}</td>
            <td class="text-center"><span class="traffic-light tl-${m.status}"></span></td>
            <td class="text-center text-lg">${m.trend}</td>
            <td class="text-center"><span class="traffic-light tl-${m.outlook}"></span></td>
        </tr>
    `).join('');

    // KPI cards
    const kpiContainer = document.getElementById('kpi-cards');
    kpiContainer.innerHTML = KPI_CARDS.map(k => `
        <div class="metric-card ${k.color}">
            <div class="text-xs text-cs-muted mb-1">${k.title}</div>
            <div class="text-2xl font-bold text-gray-900">${k.value}</div>
            <div class="text-xs text-cs-muted mt-1">${k.subtitle}</div>
            <div class="text-sm ${k.change.startsWith('+') ? 'text-green-600' : k.change.startsWith('-') ? 'text-red-600' : 'text-yellow-600'} mt-2 font-semibold">${k.change} YoY</div>
        </div>
    `).join('');
}

// ==================== CHART CREATION ====================
function createChart(canvasId, type, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    if (chartInstances[canvasId]) {
        chartInstances[canvasId].destroy();
    }

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: type !== 'doughnut' && type !== 'pie',
                position: 'top',
            },
            tooltip: {
                backgroundColor: '#ffffff',
                borderColor: '#e2e8f0',
                borderWidth: 1,
                titleColor: '#1e293b',
                bodyColor: '#64748b',
                padding: 12,
                cornerRadius: 8,
            },
        },
        scales: type === 'doughnut' || type === 'pie' || type === 'radar' ? undefined : {
            x: { grid: { display: false } },
            y: { beginAtZero: type === 'bar' },
        },
    };

    const mergedOptions = deepMerge(defaultOptions, options);

    chartInstances[canvasId] = new Chart(canvas, {
        type: type,
        data: data,
        options: mergedOptions,
    });
}

function deepMerge(target, source) {
    const result = { ...target };
    for (const key of Object.keys(source)) {
        if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
            result[key] = deepMerge(target[key] || {}, source[key]);
        } else {
            result[key] = source[key];
        }
    }
    return result;
}

// ==================== PAGE CHART INITIALIZATION ====================
const chartsInitialized = {};

function initPageCharts(pageId) {
    if (chartsInitialized[pageId]) return;

    switch (pageId) {
        case 'dashboard':
            // Dashboard has no charts, just tables
            break;

        case 'data':
            initDataCharts('production');
            break;

        case 'foresight':
            initForesightCharts();
            break;

        case 'supply':
            initSupplyCharts();
            break;

        case 'news':
            initNewsPage();
            break;

        case 'banking':
            initBankingCharts();
            break;
    }

    chartsInitialized[pageId] = true;
}

// ==================== DATA EXPLORER ====================
function switchDataTab(tab) {
    document.querySelectorAll('.data-section').forEach(s => s.style.display = 'none');
    document.querySelectorAll('#page-data .tab-btn').forEach(b => b.classList.remove('active'));

    const section = document.getElementById('data-' + tab);
    if (section) section.style.display = 'block';

    event.target.classList.add('active');
    initDataCharts(tab);
}

function initDataCharts(tab) {
    switch (tab) {
        case 'production':
            createChart('chart-production-index', 'line', CHART_DATA.productionIndex);
            createChart('chart-production-vehicles', 'bar', CHART_DATA.productionVehicles, {
                scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } }
            });
            createChart('chart-production-oem', 'doughnut', CHART_DATA.productionOEM, {
                plugins: { legend: { display: true, position: 'bottom' } },
                cutout: '60%',
            });
            createChart('chart-production-subsectors', 'bar', CHART_DATA.productionSubsectors, {
                scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } }
            });
            break;

        case 'registrations':
            createChart('chart-reg-total', 'line', CHART_DATA.registrationsTotal);
            createChart('chart-reg-brands', 'bar', CHART_DATA.registrationsBrands, {
                indexAxis: 'y',
                plugins: { legend: { display: false } },
            });
            createChart('chart-reg-eu', 'bar', CHART_DATA.registrationsEU, {
                indexAxis: 'y',
                plugins: { legend: { display: false } },
            });
            createChart('chart-reg-global', 'line', CHART_DATA.registrationsGlobal);
            break;

        case 'ev':
            createChart('chart-ev-share', 'line', CHART_DATA.evShare);
            createChart('chart-ev-global', 'bar', CHART_DATA.evGlobal, {
                scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } }
            });
            createChart('chart-ev-battery', 'line', CHART_DATA.evBattery);
            createChart('chart-ev-charging', 'bar', CHART_DATA.evCharging, {
                scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } }
            });
            break;

        case 'trade':
            createChart('chart-trade-balance', 'line', CHART_DATA.tradeBalance);
            createChart('chart-trade-destinations', 'doughnut', CHART_DATA.tradeDestinations, {
                plugins: { legend: { display: true, position: 'right' } },
                cutout: '55%',
            });
            break;

        case 'employment':
            createChart('chart-emp-total', 'line', CHART_DATA.employmentTotal);
            createChart('chart-emp-wages', 'line', CHART_DATA.employmentWages);
            break;

        case 'prices':
            createChart('chart-prices-comparison', 'bar', CHART_DATA.pricesComparison, {
                indexAxis: 'y',
            });
            createChart('chart-prices-tco', 'bar', CHART_DATA.pricesTCO, {
                indexAxis: 'y',
            });
            break;
    }
}

// ==================== FORESIGHTING ====================
function initForesightCharts() {
    // Trend Radar
    const radar = document.getElementById('trend-radar');
    TRENDS.forEach(t => {
        const dot = document.createElement('div');
        dot.className = 'trend-dot';
        const bg = t.type === 'threat' ? 'rgba(244,67,54,0.3)' :
                   t.type === 'opportunity' ? 'rgba(76,175,80,0.3)' : 'rgba(255,193,7,0.3)';
        const border = t.type === 'threat' ? '#f44336' :
                       t.type === 'opportunity' ? '#4caf50' : '#ffc107';
        dot.style.background = bg;
        dot.style.border = `2px solid ${border}`;
        // Position: impact = right (higher = more right), horizon = top (higher = more top)
        dot.style.left = `${10 + t.impact * 0.8}%`;
        dot.style.top = `${5 + (100 - t.horizon) * 0.85}%`;
        dot.innerHTML = t.emoji;
        dot.title = t.name;
        dot.addEventListener('mouseenter', (e) => showTrendTooltip(e, t));
        dot.addEventListener('mouseleave', hideTrendTooltip);
        radar.appendChild(dot);
    });

    // Forecast charts
    createChart('chart-forecast-production', 'line', CHART_DATA.forecastProduction, {
        plugins: {
            legend: { display: true, position: 'bottom' },
        },
    });
    createChart('chart-forecast-ev', 'line', CHART_DATA.forecastEV, {
        plugins: {
            legend: { display: true, position: 'bottom' },
        },
    });
}

let tooltipEl = null;
function showTrendTooltip(e, trend) {
    if (!tooltipEl) {
        tooltipEl = document.createElement('div');
        tooltipEl.className = 'tooltip';
        document.body.appendChild(tooltipEl);
    }
    const typeLabel = trend.type === 'threat' ? '🔴 Hrozba' :
                      trend.type === 'opportunity' ? '🟢 Příležitost' : '🟡 Neutrální';
    tooltipEl.innerHTML = `
        <div class="font-semibold text-gray-800 mb-1">${trend.emoji} ${trend.name}</div>
        <div class="text-gray-500">${typeLabel}</div>
        <div class="text-gray-500 mt-1">Dopad: ${trend.impact}/100</div>
        <div class="text-gray-500">Horizont: ${trend.horizon < 33 ? 'Krátkodobý' : trend.horizon < 66 ? 'Střednědobý' : 'Dlouhodobý'}</div>
    `;
    const rect = e.target.getBoundingClientRect();
    tooltipEl.style.left = rect.right + 10 + 'px';
    tooltipEl.style.top = rect.top + 'px';
    tooltipEl.classList.add('show');
}

function hideTrendTooltip() {
    if (tooltipEl) tooltipEl.classList.remove('show');
}

function showScenario(index) {
    const s = SCENARIOS[index];
    document.querySelectorAll('.scenario-quadrant').forEach((q, i) => {
        q.classList.toggle('active-scenario', i === index);
    });

    document.getElementById('scenario-detail-title').textContent = `Scénář: ${s.title} — Detail`;
    document.getElementById('scenario-detail-title').style.color = s.color;

    document.getElementById('scenario-impact-cz').innerHTML = s.impactCZ.map(i =>
        `<li class="flex items-center gap-2"><span class="tl-${i.status} traffic-light" style="width:10px;height:10px"></span> ${i.text}</li>`
    ).join('');

    document.getElementById('scenario-impact-sc').innerHTML = s.impactSC.map(i =>
        `<li class="flex items-center gap-2"><span class="tl-${i.status} traffic-light" style="width:10px;height:10px"></span> ${i.text}</li>`
    ).join('');

    document.getElementById('scenario-signposts').innerHTML = s.signposts.map(sp =>
        `<li>${sp}</li>`
    ).join('');
}

// ==================== SUPPLY CHAIN ====================
function initSupplyCharts() {
    // Supplier health chart
    createChart('chart-supplier-health', 'bar', CHART_DATA.supplierHealth, {
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } },
    });

    // Risk heatmap
    initRiskHeatmap();
}

function initRiskHeatmap() {
    const container = document.getElementById('risk-heatmap');
    const rows = RISK_HEATMAP.rows;

    rows.forEach((rowLabel, rowIdx) => {
        // Row label
        const label = document.createElement('div');
        label.className = 'text-xs text-cs-muted text-right pr-2 flex items-center justify-end';
        label.textContent = rowLabel;
        label.style.height = '60px';
        container.appendChild(label);

        // 5 columns
        for (let col = 0; col < 5; col++) {
            const cell = document.createElement('div');
            const risk = RISK_HEATMAP.risks.find(r => r[0] === rowIdx && r[1] === col);
            if (risk) {
                cell.className = 'risk-cell';
                cell.style.backgroundColor = risk[3] + '33';
                cell.style.border = `1px solid ${risk[3]}`;
                cell.style.color = risk[3];
                cell.textContent = risk[2];
            } else {
                cell.className = 'risk-cell';
                cell.style.backgroundColor = '#f8fafc';
                cell.style.border = '1px solid #e2e8f022';
            }
            container.appendChild(cell);
        }
    });
}

function showTierDetail(tier) {
    // Placeholder for tier detail modal
    const details = {
        raw: 'Suroviny: Kritická závislost na zahraničních zdrojích. 90 %+ lithia pochází z Chile a Austrálie, 70 % kobaltu z DRC, 80 % vzácných zemin z Číny.',
        t2: 'Tier 2 komponenty: ČR má silnou pozici v odlitcích a výliscích. Slabší v bateriových článcích a semiconductorech.',
        t1: 'Tier 1 systémy: Bosch, Continental, Magna a další mají závody v ČR. Přechod z ICE na EV systémy probíhá.',
        oem: 'OEM v ČR: 3 výrobci s celkovou kapacitou ~1.5M vozidel/rok. Škoda Auto dominuje s 62 % podílem.',
    };
    alert(details[tier] || 'Detail není k dispozici');
}

// ==================== NEWS ====================
function initNewsPage() {
    renderNews('all');
    createChart('chart-sentiment', 'line', CHART_DATA.sentiment, {
        plugins: { legend: { display: false } },
        scales: {
            y: { min: 30, max: 80, display: false },
            x: { display: true, grid: { display: false } },
        },
    });
}

function renderNews(filter) {
    const feed = document.getElementById('news-feed');
    const filtered = filter === 'all' ? NEWS : NEWS.filter(n => n.type === filter);

    feed.innerHTML = filtered.map(n => {
        const impactBadge = n.impact === 'high'
            ? '<span class="bg-red-100 text-red-700 px-2 py-0.5 rounded text-xs font-bold">Vysoký dopad</span>'
            : n.impact === 'medium'
            ? '<span class="bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded text-xs font-bold">Střední dopad</span>'
            : '<span class="bg-green-100 text-green-700 px-2 py-0.5 rounded text-xs font-bold">Nízký dopad</span>';

        const typeLabel = {
            regulatory: '⚖️ Regulatorní',
            market: '📊 Tržní',
            technology: '⚡ Technologie',
            geopolitical: '🌍 Geopolitika',
        }[n.type];

        return `
            <div class="news-item ${n.type}">
                <div class="flex items-center gap-3 mb-2">
                    <span class="text-xs text-cs-muted">${typeLabel}</span>
                    ${impactBadge}
                    <span class="text-xs text-cs-muted ml-auto">${n.date}</span>
                </div>
                <h4 class="text-sm font-semibold text-gray-900 mb-1">${n.title}</h4>
                <p class="text-xs text-cs-muted">${n.summary}</p>
                <div class="text-xs text-cs-accent mt-2">Zdroj: ${n.source}</div>
            </div>
        `;
    }).join('');
}

function filterNews(type) {
    document.querySelectorAll('#page-news .tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    renderNews(type);
}

// ==================== BANKING ====================
function initBankingCharts() {
    createChart('chart-banking-portfolio', 'bar', CHART_DATA.bankingPortfolio, {
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } },
    });
    createChart('chart-banking-scenarios', 'bar', CHART_DATA.bankingScenarios, {
        plugins: { legend: { display: false } },
        scales: {
            y: {
                beginAtZero: true,
                title: { display: true, text: 'NPL ratio (%)' },
            },
        },
    });
}

// ==================== INIT ====================
document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
    // Data explorer charts will init when user switches to that page
    chartsInitialized['dashboard'] = true;
});

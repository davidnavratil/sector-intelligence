// ==================== SECTOR DATA ====================
// Data extracted from automotive sector reports (ČR, EU, World)

const METRICS = [
    { name: 'Průmyslová produkce NACE 29', value: '98.3', yoy: '+0.8 %', status: 'yellow', trend: '→', outlook: 'yellow' },
    { name: 'Registrace nových vozidel ČR', value: '228 tis.', yoy: '+5.2 %', status: 'green', trend: '↑', outlook: 'green' },
    { name: 'Podíl EV na registracích ČR', value: '6.2 %', yoy: '+2.1 pp', status: 'yellow', trend: '↑', outlook: 'yellow' },
    { name: 'Zaměstnanost NACE 29', value: '178 tis.', yoy: '-2.1 %', status: 'yellow', trend: '↓', outlook: 'red' },
    { name: 'Export motorových vozidel', value: '645 mld. CZK', yoy: '+4.2 %', status: 'green', trend: '↑', outlook: 'green' },
    { name: 'Ziskovost dodavatelů (29.3)', value: '-1.2 %', yoy: '-3.1 pp', status: 'red', trend: '↓', outlook: 'red' },
    { name: 'Investice do EV přechodu', value: '12 mld. CZK', yoy: '+2 %', status: 'yellow', trend: '→', outlook: 'yellow' },
    { name: 'Cenová konkurenceschopnost vs EU', value: 'Index 87', yoy: '-1.2', status: 'green', trend: '→', outlook: 'yellow' },
];

const KPI_CARDS = [
    { title: 'Výroba vozidel ČR', value: '1.42M', subtitle: 'kusů (2024)', change: '+3.1 %', color: 'green' },
    { title: 'Podíl na HDP', value: '9.2 %', subtitle: 'přímý + nepřímý', change: '-0.3 pp', color: 'yellow' },
    { title: 'Podíl na exportu ČR', value: '23.5 %', subtitle: 'SITC 78', change: '+0.8 pp', color: 'green' },
    { title: 'Průměrná mzda NACE 29', value: '52 400 CZK', subtitle: '130 % průměru ČR', change: '+6.8 %', color: 'green' },
];

// ==================== CHART DATA ====================

const CHART_DATA = {
    // Production Index
    productionIndex: {
        labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'Index produkce NACE 29',
            data: [108.2, 114.5, 112.8, 109.1, 78.3, 89.5, 93.2, 96.8, 98.3],
            borderColor: '#4fc3f7',
            backgroundColor: 'rgba(79, 195, 247, 0.1)',
            fill: true,
            tension: 0.4,
        }]
    },

    // Vehicle production
    productionVehicles: {
        labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'Osobní vozidla',
            data: [1344, 1413, 1345, 1427, 1159, 1111, 1220, 1360, 1420],
            backgroundColor: '#4fc3f7',
            borderRadius: 4,
        }, {
            label: 'Užitková vozidla',
            data: [15, 17, 14, 13, 6, 8, 9, 12, 14],
            backgroundColor: '#ff9800',
            borderRadius: 4,
        }]
    },

    // OEM share
    productionOEM: {
        labels: ['Škoda Auto', 'Hyundai', 'TPCA/Toyota'],
        datasets: [{
            data: [62, 24, 14],
            backgroundColor: ['#4fc3f7', '#4caf50', '#ff9800'],
            borderWidth: 0,
        }]
    },

    // NACE subsectors
    productionSubsectors: {
        labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'NACE 29.1 — Motorová vozidla',
            data: [780, 810, 620, 680, 720, 790, 812],
            backgroundColor: '#4fc3f7',
            borderRadius: 4,
        }, {
            label: 'NACE 29.2 — Karoserie',
            data: [42, 44, 32, 36, 40, 43, 45],
            backgroundColor: '#ffc107',
            borderRadius: 4,
        }, {
            label: 'NACE 29.3 — Díly a příslušenství',
            data: [310, 315, 245, 260, 278, 290, 298],
            backgroundColor: '#f44336',
            borderRadius: 4,
        }]
    },

    // Registrations total
    registrationsTotal: {
        labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'Nové registrace (tis.)',
            data: [259, 271, 261, 249, 203, 206, 196, 217, 228],
            borderColor: '#4fc3f7',
            backgroundColor: 'rgba(79, 195, 247, 0.15)',
            fill: true,
            tension: 0.4,
        }]
    },

    // Top brands
    registrationsBrands: {
        labels: ['Škoda', 'VW', 'Hyundai', 'Toyota', 'Kia', 'BMW', 'Dacia', 'Ford', 'Mercedes', 'Peugeot'],
        datasets: [{
            label: 'Registrace 2024 (tis.)',
            data: [68, 22, 18, 16, 14, 10, 9, 8, 7, 6],
            backgroundColor: ['#4fc3f7', '#2196f3', '#4caf50', '#ff9800', '#e91e63', '#9c27b0', '#00bcd4', '#795548', '#607d8b', '#ff5722'],
            borderRadius: 4,
        }]
    },

    // EU registrations
    registrationsEU: {
        labels: ['Německo', 'Francie', 'Itálie', 'Španělsko', 'Polsko', 'Belgie', 'Nizozemí', 'Rakousko', 'Česko', 'Švédsko'],
        datasets: [{
            label: 'Registrace 2024 (tis.)',
            data: [2840, 1780, 1560, 1020, 510, 480, 390, 310, 228, 280],
            backgroundColor: '#4fc3f7',
            borderRadius: 4,
        }]
    },

    // Global vehicle sales
    registrationsGlobal: {
        labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'Čína',
            data: [27.8, 25.8, 25.3, 26.3, 26.9, 30.1, 31.4],
            borderColor: '#f44336',
            tension: 0.4,
        }, {
            label: 'Evropa',
            data: [18.1, 17.9, 14.5, 15.2, 15.8, 16.3, 16.8],
            borderColor: '#4fc3f7',
            tension: 0.4,
        }, {
            label: 'USA',
            data: [17.2, 17.0, 14.5, 15.0, 13.7, 15.5, 15.9],
            borderColor: '#4caf50',
            tension: 0.4,
        }, {
            label: 'Zbytek světa',
            data: [29.5, 28.7, 24.2, 25.3, 25.8, 27.5, 28.2],
            borderColor: '#ff9800',
            tension: 0.4,
            borderDash: [5, 5],
        }]
    },

    // EV share
    evShare: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'ČR',
            data: [0.6, 1.0, 1.8, 2.8, 4.1, 6.2],
            borderColor: '#4fc3f7',
            backgroundColor: 'rgba(79, 195, 247, 0.1)',
            fill: true,
            tension: 0.4,
        }, {
            label: 'EU průměr',
            data: [3.0, 5.4, 9.1, 12.1, 15.7, 21.0],
            borderColor: '#ffc107',
            tension: 0.4,
            borderDash: [5, 5],
        }, {
            label: 'Norsko',
            data: [42.4, 54.3, 64.5, 79.3, 82.4, 88.9],
            borderColor: '#4caf50',
            tension: 0.4,
            borderDash: [2, 2],
        }]
    },

    // Global EV sales
    evGlobal: {
        labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'BEV',
            data: [1.3, 1.6, 2.1, 4.6, 7.3, 9.5, 12.1],
            backgroundColor: '#4fc3f7',
            borderRadius: 4,
        }, {
            label: 'PHEV',
            data: [0.7, 0.8, 1.0, 1.9, 2.9, 3.2, 3.8],
            backgroundColor: '#ff9800',
            borderRadius: 4,
        }]
    },

    // Battery prices
    evBattery: {
        labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025E'],
        datasets: [{
            label: '$/kWh',
            data: [273, 226, 185, 161, 140, 132, 151, 139, 128, 120],
            borderColor: '#4caf50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            fill: true,
            tension: 0.4,
        }]
    },

    // Charging infrastructure
    evCharging: {
        labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'AC body',
            data: [450, 680, 1050, 1580, 2300, 3100],
            backgroundColor: '#4fc3f7',
            borderRadius: 4,
        }, {
            label: 'DC body (rychlonabíjení)',
            data: [120, 180, 310, 520, 780, 1100],
            backgroundColor: '#ff9800',
            borderRadius: 4,
        }]
    },

    // Trade balance
    tradeBalance: {
        labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'Export',
            data: [580, 610, 498, 520, 560, 618, 645],
            borderColor: '#4caf50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            fill: true,
            tension: 0.4,
        }, {
            label: 'Import',
            data: [320, 335, 278, 295, 330, 355, 370],
            borderColor: '#f44336',
            backgroundColor: 'rgba(244, 67, 54, 0.1)',
            fill: true,
            tension: 0.4,
        }]
    },

    // Export destinations
    tradeDestinations: {
        labels: ['Německo', 'UK', 'Francie', 'Itálie', 'Polsko', 'Španělsko', 'Rakousko', 'Ostatní'],
        datasets: [{
            data: [32, 12, 9, 8, 7, 5, 4, 23],
            backgroundColor: ['#4fc3f7', '#2196f3', '#1565c0', '#4caf50', '#ff9800', '#f44336', '#9c27b0', '#607d8b'],
            borderWidth: 0,
        }]
    },

    // Employment
    employmentTotal: {
        labels: ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'Zaměstnanost NACE 29 (tis.)',
            data: [175, 179, 182, 185, 172, 170, 176, 182, 178],
            borderColor: '#4fc3f7',
            backgroundColor: 'rgba(79, 195, 247, 0.1)',
            fill: true,
            tension: 0.4,
        }]
    },

    // Wages
    employmentWages: {
        labels: ['2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'NACE 29 — Automotive',
            data: [38200, 40100, 40800, 42500, 45800, 49200, 52400],
            borderColor: '#4fc3f7',
            tension: 0.4,
        }, {
            label: 'Průmysl celkem',
            data: [32800, 34500, 35200, 36800, 39500, 41800, 43600],
            borderColor: '#ff9800',
            tension: 0.4,
            borderDash: [5, 5],
        }, {
            label: 'ČR průměr',
            data: [31868, 33429, 34835, 36404, 39306, 41265, 43100],
            borderColor: '#888',
            tension: 0.4,
            borderDash: [2, 2],
        }]
    },

    // Prices comparison
    pricesComparison: {
        labels: [
            ['Škoda Octavia', 'vs. Enyaq 60'],
            ['VW Golf', 'vs. ID.3'],
            ['Hyundai Tucson', 'vs. Ioniq 5'],
            ['Toyota Corolla', 'vs. bZ4X'],
            ['BMW 3', 'vs. i4'],
            ['Kia Sportage', 'vs. EV6'],
            ['Peugeot 308', 'vs. e-308'],
            ['Renault Mégane', 'vs. Mégane E-Tech'],
        ],
        datasets: [{
            label: 'Spalovací (ICE)',
            data: [750, 680, 820, 650, 1150, 850, 620, 580],
            backgroundColor: '#ff9800',
            borderRadius: 4,
        }, {
            label: 'Elektrický (BEV)',
            data: [1050, 920, 1150, 1080, 1380, 1120, 890, 850],
            backgroundColor: '#4fc3f7',
            borderRadius: 4,
        }]
    },

    // TCO
    pricesTCO: {
        labels: [['Škoda Octavia', 'vs. Enyaq'], ['VW Golf', 'vs. ID.3'], ['Hyundai Tucson', 'vs. Ioniq 5'], ['BMW 3', 'vs. i4']],
        datasets: [{
            label: 'TCO - Spalovací (5 let)',
            data: [1180, 1050, 1290, 1750],
            backgroundColor: '#ff9800',
            borderRadius: 4,
        }, {
            label: 'TCO - Elektrický (5 let)',
            data: [1210, 1020, 1310, 1580],
            backgroundColor: '#4fc3f7',
            borderRadius: 4,
        }]
    },

    // Forecast production
    forecastProduction: {
        labels: ['2020', '2021', '2022', '2023', '2024', '2025E', '2026E', '2027E', '2028E'],
        datasets: [{
            label: 'Skutečnost',
            data: [1165, 1119, 1229, 1372, 1434, null, null, null, null],
            borderColor: '#4fc3f7',
            tension: 0.4,
            pointRadius: 4,
        }, {
            label: 'Predikce (baseline)',
            data: [null, null, null, null, 1434, 1460, 1480, 1450, 1420],
            borderColor: '#4caf50',
            borderDash: [5, 5],
            tension: 0.4,
            pointRadius: 4,
        }, {
            label: 'Horní CI 80 %',
            data: [null, null, null, null, 1434, 1510, 1560, 1550, 1540],
            borderColor: 'rgba(76, 175, 80, 0.3)',
            backgroundColor: 'rgba(76, 175, 80, 0.05)',
            fill: '+1',
            tension: 0.4,
            pointRadius: 0,
        }, {
            label: 'Dolní CI 80 %',
            data: [null, null, null, null, 1434, 1410, 1400, 1350, 1300],
            borderColor: 'rgba(76, 175, 80, 0.3)',
            tension: 0.4,
            pointRadius: 0,
        }]
    },

    // Forecast EV share
    forecastEV: {
        labels: ['2020', '2021', '2022', '2023', '2024', '2025E', '2026E', '2027E', '2028E', '2029E', '2030E'],
        datasets: [{
            label: 'Skutečnost',
            data: [1.0, 1.8, 2.8, 4.1, 6.2, null, null, null, null, null, null],
            borderColor: '#4fc3f7',
            tension: 0.4,
            pointRadius: 4,
        }, {
            label: 'Baseline scénář',
            data: [null, null, null, null, 6.2, 8.5, 11.8, 16.2, 21.5, 27.8, 35.0],
            borderColor: '#ffc107',
            borderDash: [5, 5],
            tension: 0.4,
        }, {
            label: 'Optimistický',
            data: [null, null, null, null, 6.2, 10.2, 15.5, 23.0, 32.0, 42.0, 55.0],
            borderColor: '#4caf50',
            borderDash: [2, 2],
            tension: 0.4,
        }, {
            label: 'Pesimistický',
            data: [null, null, null, null, 6.2, 7.2, 8.8, 11.0, 14.0, 17.5, 22.0],
            borderColor: '#f44336',
            borderDash: [2, 2],
            tension: 0.4,
        }]
    },

    // Supplier health
    supplierHealth: {
        labels: ['29.1 Vozidla', '29.2 Karoserie', '29.3 Díly'],
        datasets: [{
            label: 'EBITDA marže (%)',
            data: [8.2, 3.1, -1.2],
            backgroundColor: ['#4caf50', '#ffc107', '#f44336'],
            borderRadius: 4,
        }]
    },

    // Sentiment
    sentiment: {
        labels: ['Srp', 'Zář', 'Říj', 'Lis', 'Pro', 'Led', 'Úno', 'Bře'],
        datasets: [{
            label: 'Sentiment',
            data: [58, 55, 48, 45, 50, 53, 49, 52],
            borderColor: '#ffc107',
            backgroundColor: 'rgba(255, 193, 7, 0.1)',
            fill: true,
            tension: 0.4,
        }]
    },

    // Banking portfolio
    bankingPortfolio: {
        labels: [['NACE 29.1', 'OEM výrobci'], ['NACE 29.3', 'Dodavatelé'], ['Leasing', 'flotily'], ['Dealeři', 'retail'], ['Ostatní', 'automotive']],
        datasets: [{
            label: 'Expozice (mld. CZK)',
            data: [12.5, 14.2, 8.4, 4.8, 2.9],
            backgroundColor: ['#4fc3f7', '#f44336', '#4caf50', '#ffc107', '#9c27b0'],
            borderRadius: 4,
        }]
    },

    // Banking scenarios
    bankingScenarios: {
        labels: ['Baseline', 'Řízená revoluce', 'Zelený sprint', 'Status quo+', 'Tržní evoluce'],
        datasets: [{
            label: 'NPL ratio (%)',
            data: [3.8, 6.2, 4.5, 3.2, 5.8],
            backgroundColor: ['#4fc3f7', '#f44336', '#ffc107', '#4caf50', '#ff9800'],
            borderRadius: 4,
        }]
    },
};

// ==================== TREND RADAR DATA ====================
const TRENDS = [
    { name: 'CO2 limity 2025', type: 'threat', impact: 85, horizon: 25, emoji: '⚖️' },
    { name: 'Čínské EV v EU', type: 'threat', impact: 75, horizon: 35, emoji: '🇨🇳' },
    { name: 'Cena baterií', type: 'opportunity', impact: 90, horizon: 55, emoji: '🔋' },
    { name: 'Solid-state baterie', type: 'opportunity', impact: 80, horizon: 80, emoji: '⚡' },
    { name: 'Autonomní řízení', type: 'neutral', impact: 60, horizon: 85, emoji: '🤖' },
    { name: 'Nearshoring', type: 'opportunity', impact: 70, horizon: 45, emoji: '🏭' },
    { name: 'Recese Německo', type: 'threat', impact: 65, horizon: 20, emoji: '📉' },
    { name: 'SW-defined vehicles', type: 'opportunity', impact: 55, horizon: 60, emoji: '💻' },
    { name: 'Skill gap', type: 'threat', impact: 50, horizon: 40, emoji: '👷' },
    { name: 'Cirkulární ekonomika', type: 'opportunity', impact: 45, horizon: 65, emoji: '♻️' },
    { name: 'Vodíkové články', type: 'neutral', impact: 35, horizon: 75, emoji: '💧' },
    { name: 'EU cla na Čínu', type: 'neutral', impact: 70, horizon: 30, emoji: '🛃' },
    { name: 'Gigacasting', type: 'opportunity', impact: 40, horizon: 50, emoji: '🔩' },
    { name: 'Zákaz ICE 2035', type: 'threat', impact: 95, horizon: 70, emoji: '🚫' },
];

// ==================== NEWS DATA ====================
const NEWS = [
    {
        type: 'regulatory',
        title: 'EU potvrdila CO2 limity pro 2030: 49.5 g/km pro osobní vozy',
        summary: 'Evropská komise zamítla návrh na odložení přísnějších CO2 limitů. OEM budou muset dosáhnout ~50 % podílu EV na prodejích.',
        date: '19. března 2026',
        impact: 'high',
        source: 'European Commission',
    },
    {
        type: 'market',
        title: 'Volkswagen oznámil restrukturalizaci dodavatelského řetězce',
        summary: 'VW sníží počet Tier 1 dodavatelů o 20 % do roku 2028. České firmy mezi potenciálně dotčenými.',
        date: '18. března 2026',
        impact: 'high',
        source: 'Reuters',
    },
    {
        type: 'technology',
        title: 'CATL představil baterii s hustotou 500 Wh/kg',
        summary: 'Nová generace LFP baterií slibuje 30 % nárůst dojezdu. Masová výroba plánována na 2028.',
        date: '15. března 2026',
        impact: 'medium',
        source: 'BloombergNEF',
    },
    {
        type: 'geopolitical',
        title: 'EU schválila dodatečná cla 38 % na čínské elektromobily',
        summary: 'Definitivní rozhodnutí po antidumpingovém šetření. Čína hrozí odvetou na EU zemědělské produkty.',
        date: '12. března 2026',
        impact: 'high',
        source: 'EU Trade Commission',
    },
    {
        type: 'market',
        title: 'Škoda Auto: rekordní objednávky Enyaq facelift',
        summary: 'Objednávky nového Enyaq překročily 50 000 ks v prvním měsíci. Mladoboleslavský závod navyšuje kapacitu.',
        date: '10. března 2026',
        impact: 'medium',
        source: 'Škoda Auto',
    },
    {
        type: 'regulatory',
        title: 'Euro 7 norma: finální parametry zveřejněny',
        summary: 'Nové emisní limity pro znečišťující látky (NOx, PM) budou platit od 2027. Dopady na ICE výrobu.',
        date: '8. března 2026',
        impact: 'medium',
        source: 'EUR-Lex',
    },
    {
        type: 'market',
        title: 'Magna International uzavírá závod v Liberci',
        summary: '800 zaměstnanců bude propuštěno. Důvodem je přesun výroby interiérových dílů do Rumunska.',
        date: '5. března 2026',
        impact: 'medium',
        source: 'Hospodářské noviny',
    },
    {
        type: 'technology',
        title: 'BYD spouští výrobu v Maďarsku — první čínská auto továrna v EU',
        summary: 'Kapacita 150 000 vozidel ročně. Dopad na konkurenceschopnost evropských OEM.',
        date: '3. března 2026',
        impact: 'high',
        source: 'Financial Times',
    },
    {
        type: 'geopolitical',
        title: 'USA zvyšují cla na čínské EV na 100 %',
        summary: 'Přesměrování čínského exportu do Evropy je pravděpodobným důsledkem.',
        date: '28. února 2026',
        impact: 'medium',
        source: 'White House',
    },
    {
        type: 'market',
        title: 'Registrace nových vozidel v ČR: únor +8.3 % YoY',
        summary: 'Pozitivní trend pokračuje 5. měsíc. EV podíl dosáhl rekordních 7.1 % v únoru.',
        date: '25. února 2026',
        impact: 'low',
        source: 'SDA',
    },
];

// ==================== RISK HEATMAP DATA ====================
const RISK_HEATMAP = {
    rows: ['Kritický', 'Vysoký', 'Střední', 'Nízký', 'Minimální'],
    risks: [
        // [row (0=Kritický), col (0-4), name, color]
        [0, 3, 'Zákaz ICE 2035', '#f44336'],
        [0, 2, 'CO2 pokuty OEM', '#f44336'],
        [1, 4, 'Čínská dominance\nvzácné zeminy', '#ff5722'],
        [1, 3, 'Semiconductor\nshortage', '#ff9800'],
        [1, 2, 'Bankrot Tier 1\ndodavatele', '#ff9800'],
        [2, 3, 'Přesun výroby\nOEM z ČR', '#ffc107'],
        [2, 2, 'Skill gap\nEV specialisté', '#ffc107'],
        [2, 1, 'Energetické\nnáklady ČR', '#ffc107'],
        [3, 4, 'Kyber útok\nna supply chain', '#4caf50'],
        [3, 1, 'Logistická\ndisruption', '#4caf50'],
        [4, 2, 'Přírodní\nkatastrofa', '#2196f3'],
        [4, 0, 'Patent\nspory', '#2196f3'],
    ]
};

// ==================== SCENARIO DETAILS ====================
const SCENARIOS = [
    {
        title: 'Řízená revoluce',
        color: '#ffc107',
        impactCZ: [
            { text: 'Produkce: -5 až -15 %', status: 'yellow' },
            { text: 'Zaměstnanost: -10 až -20 %', status: 'red' },
            { text: 'Export: stabilní (přechod na EV modely)', status: 'yellow' },
        ],
        impactSC: [
            { text: 'ICE dodavatelé: vysoké ztráty', status: 'red' },
            { text: 'EV komponenty: růst poptávky', status: 'green' },
            { text: 'Tier 2/3: tlak na konsolidaci', status: 'yellow' },
        ],
        signposts: [
            '📌 Cena baterií >100 $/kWh v 2026',
            '📌 EU neodloží CO2 limity 2030',
            '📌 EV share ČR <10 % v 2026',
            '📌 Další OEM ohlásí uzavření ICE linek',
        ],
    },
    {
        title: 'Zelený sprint',
        color: '#4caf50',
        impactCZ: [
            { text: 'Produkce: +5 až +15 % (nové EV modely)', status: 'green' },
            { text: 'Zaměstnanost: -5 % (automatizace kompenzuje)', status: 'yellow' },
            { text: 'Export: silný růst EV exportu', status: 'green' },
        ],
        impactSC: [
            { text: 'ICE dodavatelé: nucená rychlá konverze', status: 'red' },
            { text: 'EV komponenty: boom poptávky', status: 'green' },
            { text: 'Nové segmenty: baterie, SW, ADAS', status: 'green' },
        ],
        signposts: [
            '📌 Cena baterií <80 $/kWh v 2027',
            '📌 TCO parita EV vs ICE dosažena',
            '📌 EV share EU >30 % v 2026',
            '📌 Gigafactory v ČR oznámena',
        ],
    },
    {
        title: 'Status quo+',
        color: '#888',
        impactCZ: [
            { text: 'Produkce: stabilní (mix ICE + EV)', status: 'green' },
            { text: 'Zaměstnanost: stabilní', status: 'green' },
            { text: 'Export: mírný růst', status: 'green' },
        ],
        impactSC: [
            { text: 'ICE dodavatelé: přežívají déle', status: 'yellow' },
            { text: 'EV komponenty: pomalý růst', status: 'yellow' },
            { text: 'Hybridní mix: ICE + PHEV + BEV', status: 'yellow' },
        ],
        signposts: [
            '📌 EU odloží/zmírní CO2 limity',
            '📌 Cena baterií stagnuje >110 $/kWh',
            '📌 Spotřebitelé preferují ICE/hybrid',
            '📌 Politický obrat v EU klimatické politice',
        ],
    },
    {
        title: 'Tržní evoluce',
        color: '#4fc3f7',
        impactCZ: [
            { text: 'Produkce: volatilní (cenová válka)', status: 'yellow' },
            { text: 'Zaměstnanost: -10 % (efektivita)', status: 'yellow' },
            { text: 'Export: ohrožen čínskou konkurencí', status: 'red' },
        ],
        impactSC: [
            { text: 'ICE dodavatelé: postupný útlum', status: 'yellow' },
            { text: 'Cenová konkurence z Číny: extrémní', status: 'red' },
            { text: 'Konsolidace: M&A vlna', status: 'yellow' },
        ],
        signposts: [
            '📌 Čínské značky >15 % EU trhu',
            '📌 Cla na čínské EV neúčinná',
            '📌 Bankrot/akvizice evropského OEM',
            '📌 Masová cenová válka EV pod €20 000',
        ],
    },
];

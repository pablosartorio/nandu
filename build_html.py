import json

# Read problems
with open("problemas_nandu.json", "r", encoding="utf-8") as f:
    problems_json = f.read()

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Misión Ñandú: Camino al Nacional</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-error: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #cbd5e1;
            --font-main: 'Outfit', sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-main);
            background: radial-gradient(circle at top right, #1e1b4b, var(--bg-primary));
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
        }

        /* Top Bar */
        header {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .user-stats {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .stat-badge {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 700;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .xp-bar-container {
            width: 150px;
            height: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            overflow: hidden;
            margin-left: 10px;
        }

        .xp-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            width: 0%;
            transition: width 0.5s ease-out;
        }

        .title-logo {
            font-size: 1.8rem;
            font-weight: 900;
            background: linear-gradient(to right, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            color: transparent;
            text-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        }

        /* Main Container */
        main {
            flex: 1;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        /* Screens */
        .screen {
            display: none;
            animation: fadeIn 0.4s ease-out forwards;
        }
        .screen.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Home Dashboard */
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 2rem;
        }

        .modules-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }

        .module-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .module-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .module-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border-color: var(--accent-secondary);
        }

        .module-card:hover::before { opacity: 1; }

        .module-progress {
            height: 4px;
            background: rgba(255,255,255,0.1);
            border-radius: 2px;
            margin-top: 0.8rem;
            overflow: hidden;
        }
        .module-progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            width: 0%;
            transition: width 0.5s ease-out;
        }
        .module-progress-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }

        .module-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .module-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        /* Sidebar Mascot */
        .mascot-container {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(139, 92, 246, 0.3);
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.1);
        }

        .mascot-svg {
            width: 150px;
            height: 150px;
            margin: 0 auto 1rem;
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        .competencia-btn {
            background: linear-gradient(135deg, #f59e0b, #ef4444);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 30px;
            font-size: 1.2rem;
            font-weight: 900;
            width: 100%;
            cursor: pointer;
            margin-top: 1rem;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
            transition: transform 0.2s;
        }
        .competencia-btn:hover {
            transform: scale(1.05);
        }

        /* Gameplay Area */
        .play-area {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(30, 41, 59, 0.9);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .problem-statement {
            font-size: 1.5rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            font-weight: 500;
        }

        .answer-section {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .answer-input {
            flex: 1;
            background: rgba(15, 23, 42, 0.8);
            border: 2px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 1rem;
            font-size: 1.2rem;
            border-radius: 10px;
            outline: none;
            font-family: var(--font-main);
            transition: border-color 0.3s;
        }

        .answer-input:focus {
            border-color: var(--accent-primary);
        }

        .btn {
            padding: 1rem 2rem;
            border-radius: 10px;
            font-weight: 700;
            font-size: 1.1rem;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
            font-family: var(--font-main);
        }

        .btn-primary {
            background: var(--accent-primary);
            color: white;
        }
        .btn-primary:hover {
            background: #2563eb;
            transform: translateY(-2px);
        }

        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: white;
        }
        .btn-secondary:hover {
            background: rgba(255,255,255,0.2);
        }

        .feedback {
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1.5rem;
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .feedback.success {
            display: block;
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid var(--accent-success);
        }

        .feedback.error {
            display: block;
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid var(--accent-error);
        }

        /* Geometria SVG Canvas */
        #svg-workspace {
            width: 100%;
            height: 300px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            margin-bottom: 1.5rem;
            display: none;
            cursor: crosshair;
            border: 1px dashed rgba(255,255,255,0.2);
        }

        .interactive-polygon {
            fill: rgba(59, 130, 246, 0.3);
            stroke: var(--accent-primary);
            stroke-width: 3;
            transition: fill 0.3s;
        }
        .interactive-polygon:hover {
            fill: rgba(59, 130, 246, 0.5);
        }
        .interactive-vertex {
            fill: white;
            r: 6;
            cursor: pointer;
            transition: r 0.2s, fill 0.2s;
        }
        .interactive-vertex:hover {
            r: 8;
            fill: var(--accent-warning);
        }

        @media (max-width: 768px) {
            .dashboard { grid-template-columns: 1fr; }
            .user-stats { gap: 1rem; }
            .title-logo { font-size: 1.2rem; }
            .xp-bar-container { width: 100px; }
        }

        /* Competencia Mode Tracker */
        .stage-tracker {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            position: relative;
        }
        .stage-tracker::before {
            content: '';
            position: absolute;
            top: 50%; left: 0; right: 0;
            height: 2px;
            background: rgba(255,255,255,0.2);
            z-index: 0;
        }
        .stage-node {
            width: 30px; height: 30px;
            border-radius: 50%;
            background: var(--bg-secondary);
            border: 2px solid rgba(255,255,255,0.5);
            z-index: 1;
            display: flex; align-items: center; justify-content: center;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .stage-node.active { border-color: var(--accent-primary); background: var(--accent-primary); box-shadow: 0 0 15px var(--accent-primary); }
        .stage-node.passed { border-color: var(--accent-success); background: var(--accent-success); }
    </style>
</head>
<body>

    <header>
        <div class="title-logo" style="cursor: pointer" onclick="showScreen('home')">Misión Ñandú</div>
        <div class="user-stats">
            <div class="stat-badge">
                🏆 <span id="level-display">Nivel 1</span>
                <div class="xp-bar-container"><div class="xp-bar-fill" id="xp-bar"></div></div>
            </div>
            <div class="stat-badge">
                🏅 <span id="achievements-display">0</span>
            </div>
        </div>
    </header>

    <main>
        <!-- Home Dashboard Screen -->
        <div id="home" class="screen active">
            <div class="dashboard">
                <div class="modules-grid">
                    <div class="module-card" onclick="startModule('patrones')">
                        <div class="module-icon">🕵️‍♂️</div>
                        <div class="module-title">Detective de Patrones</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Descubre secuencias numéricas ocultas.</div>
                        <div class="module-progress"><div class="module-progress-bar" id="prog-patrones"></div></div>
                        <div class="module-progress-label" id="prog-patrones-label">0 resueltos</div>
                    </div>
                    <div class="module-card" onclick="startModule('logica')">
                        <div class="module-icon">🧪</div>
                        <div class="module-title">Laboratorio de Estrategias</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Lógica y razonamiento deductivo.</div>
                        <div class="module-progress"><div class="module-progress-bar" id="prog-logica"></div></div>
                        <div class="module-progress-label" id="prog-logica-label">0 resueltos</div>
                    </div>
                    <div class="module-card" onclick="startModule('geometria')">
                        <div class="module-icon">🥷</div>
                        <div class="module-title">Geometría Ninja</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Domina perímetros y áreas con precisión.</div>
                        <div class="module-progress"><div class="module-progress-bar" id="prog-geometria"></div></div>
                        <div class="module-progress-label" id="prog-geometria-label">0 resueltos</div>
                    </div>
                    <div class="module-card" onclick="startModule('conteo')">
                        <div class="module-icon">🛣️</div>
                        <div class="module-title">Cuenta Caminos</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Combinatoria y conteo de posibilidades.</div>
                        <div class="module-progress"><div class="module-progress-bar" id="prog-conteo"></div></div>
                        <div class="module-progress-label" id="prog-conteo-label">0 resueltos</div>
                    </div>
                    <div class="module-card" onclick="startModule('divisibilidad')">
                        <div class="module-icon">🏴‍☠️</div>
                        <div class="module-title">Cofre de Divisibilidad</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Secretos de múltiplos y divisores.</div>
                        <div class="module-progress"><div class="module-progress-bar" id="prog-divisibilidad"></div></div>
                        <div class="module-progress-label" id="prog-divisibilidad-label">0 resueltos</div>
                    </div>
                    <div class="module-card" onclick="startModule('error')">
                        <div class="module-icon">🔍</div>
                        <div class="module-title">Encuentra el Error</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Analiza resoluciones falsas.</div>
                        <div class="module-progress"><div class="module-progress-bar" id="prog-error"></div></div>
                        <div class="module-progress-label" id="prog-error-label">0 resueltos</div>
                    </div>
                    <div class="module-card" onclick="startModule('olimpico')">
                        <div class="module-icon">👑</div>
                        <div class="module-title">Problema Olímpico</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">El desafío final de campeones.</div>
                        <div class="module-progress"><div class="module-progress-bar" id="prog-olimpico"></div></div>
                        <div class="module-progress-label" id="prog-olimpico-label">0 resueltos</div>
                    </div>
                </div>
                
                <div>
                    <div class="mascot-container">
                        <div id="mascot-svg-wrapper">
                            <!-- SVG Mascot injected here based on level -->
                        </div>
                        <h3 style="margin-bottom: 0.5rem;" id="mascot-name">Huevo Matemático</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;" id="mascot-desc">Resuelve problemas para evolucionar tu Ñandú.</p>
                        
                        <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1)">
                            <h3>Modo Competencia</h3>
                            <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1rem;">Simula las 5 etapas oficiales.</p>
                            <button class="competencia-btn" onclick="startCompetencia()">¡Inscribirse!</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Problem Playing Screen -->
        <div id="play" class="screen">
            <div class="play-area">
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <button class="btn btn-secondary" style="padding: 0.5rem 1rem" onclick="showScreen('home')">← Volver</button>
                    <div id="mode-indicator" style="color: var(--accent-warning); font-weight: bold; align-self: center;">Entrenamiento</div>
                </div>
                
                <div id="competencia-tracker" class="stage-tracker" style="display: none;">
                    <div class="stage-node" id="stage-0" title="Escolar">1</div>
                    <div class="stage-node" id="stage-1" title="Interescolar">2</div>
                    <div class="stage-node" id="stage-2" title="Zonal">3</div>
                    <div class="stage-node" id="stage-3" title="Regional">4</div>
                    <div class="stage-node" id="stage-4" title="Nacional">5</div>
                </div>

                <div id="problem-category" style="text-transform: uppercase; letter-spacing: 2px; color: var(--accent-secondary); font-size: 0.9rem; font-weight: 700; margin-bottom: 1rem;">CATEGORIA</div>
                
                <!-- Interactive SVG Canvas for Geometry -->
                <svg id="svg-workspace"></svg>

                <div class="problem-statement" id="problem-statement">
                    Cargando problema...
                </div>

                <div class="answer-section">
                    <input type="text" id="answer-input" class="answer-input" placeholder="Tu respuesta final..." onkeypress="if(event.key === 'Enter') checkAnswer()">
                    <button class="btn btn-primary" onclick="checkAnswer()">Responder</button>
                    <button class="btn btn-secondary" onclick="showHint()" id="hint-btn">💡 Pista</button>
                </div>

                <div id="feedback" class="feedback">
                    <h3 id="feedback-title" style="margin-bottom: 0.5rem;"></h3>
                    <p id="feedback-desc"></p>
                    <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                        <button class="btn btn-primary" id="next-problem-btn" onclick="nextProblem()">Siguiente Problema →</button>
                    </div>
                </div>
            </div>
        </div>
        
    </main>

    <script>
        // Data
        const problemBank = PLACEHOLDER_JSON;

        // State
        let state = {
            xp: 0,
            level: 1,
            achievements: [],
            progress: {},
            competencia: {
                active: false,
                stageIndex: 0, // 0: Escolar, 1: Interescolar, 2: Zonal, 3: Regional, 4: Nacional
                problemCount: 0,
                correctCount: 0
            }
        };

        const stages = ["Escolar", "Interescolar", "Zonal", "Regional", "Nacional"];

        let currentProblem = null;
        let currentModule = null;
        let recentIds = []; // ids mostrados recientemente, para no repetir los últimos N

        // Initialization
        function init() {
            loadState();
            updateStatsUI();
            updateMascot();
            updateProgressUI();
        }

        // Local Storage
        function loadState() {
            const saved = localStorage.getItem('nandu_state');
            if (!saved) return;
            let parsed;
            try {
                parsed = JSON.parse(saved);
            } catch (e) {
                // Estado corrupto: arrancamos limpio en lugar de romper la app.
                console.warn('Estado guardado inválido, se reinicia.', e);
                return;
            }
            // Merge sobre los valores por defecto: un estado guardado por una versión
            // anterior (sin, p.ej., 'competencia') no debe dejar claves sin definir.
            const defaultCompetencia = state.competencia;
            state = Object.assign({}, state, parsed);
            state.competencia = Object.assign({}, defaultCompetencia, parsed.competencia || {});
            if (!state.progress || typeof state.progress !== 'object') state.progress = {};
            if (!Array.isArray(state.achievements)) state.achievements = [];
            if (typeof state.xp !== 'number') state.xp = 0;
            if (typeof state.level !== 'number') state.level = 1;
        }

        function saveState() {
            localStorage.setItem('nandu_state', JSON.stringify(state));
        }

        // UI Routing
        function showScreen(id) {
            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            
            if (id === 'home') {
                updateStatsUI();
                updateMascot();
                updateProgressUI();
            }
        }

        // Mascot Evolution
        function getMascotData() {
            if (state.level < 4) {
                return {
                    name: "Huevo Matemático",
                    desc: "Recién descubriendo los números.",
                    svg: `<svg viewBox="0 0 100 100"><circle cx="50" cy="60" r="30" fill="#fef3c7"/><path d="M30 50 Q 50 30 70 50 Q 50 70 30 50" stroke="#f59e0b" stroke-width="2" fill="none" stroke-dasharray="4"/></svg>`
                };
            } else if (state.level < 8) {
                return {
                    name: "Ñanducito",
                    desc: "Dando sus primeros pasos lógicos.",
                    svg: `<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="20" fill="#d97706"/><circle cx="43" cy="45" r="3" fill="#fff"/><circle cx="57" cy="45" r="3" fill="#fff"/><circle cx="43" cy="45" r="1" fill="#000"/><circle cx="57" cy="45" r="1" fill="#000"/><path d="M45 55 Q 50 60 55 55" stroke="#fff" stroke-width="2" fill="none"/><line x1="50" y1="70" x2="50" y2="90" stroke="#d97706" stroke-width="4"/><line x1="50" y1="90" x2="40" y2="95" stroke="#d97706" stroke-width="3"/><line x1="50" y1="90" x2="60" y2="95" stroke="#d97706" stroke-width="3"/></svg>`
                };
            } else if (state.level < 13) {
                return {
                    name: "Ñandú Corredor",
                    desc: "Veloz para calcular y razonar.",
                    svg: `<svg viewBox="0 0 100 100"><ellipse cx="50" cy="60" rx="30" ry="20" fill="#b45309"/><circle cx="70" cy="30" r="15" fill="#b45309"/><path d="M 60 40 Q 50 50 50 60" stroke="#b45309" stroke-width="10" fill="none"/><circle cx="75" cy="25" r="2" fill="#fff"/><polygon points="85,30 95,35 85,40" fill="#f59e0b"/><line x1="40" y1="80" x2="40" y2="95" stroke="#b45309" stroke-width="5"/><line x1="60" y1="80" x2="60" y2="95" stroke="#b45309" stroke-width="5"/></svg>`
                };
            } else {
                return {
                    name: "Ñandú Ninja Olímpico",
                    desc: "Maestro supremo de las estrategias.",
                    svg: `<svg viewBox="0 0 100 100"><ellipse cx="50" cy="60" rx="30" ry="20" fill="#1e293b"/><circle cx="70" cy="30" r="15" fill="#1e293b"/><path d="M 60 40 Q 50 50 50 60" stroke="#1e293b" stroke-width="10" fill="none"/><rect x="60" y="20" width="20" height="5" fill="#ef4444"/><polygon points="85,30 95,35 85,40" fill="#f59e0b"/><line x1="40" y1="80" x2="40" y2="95" stroke="#1e293b" stroke-width="5"/><line x1="60" y1="80" x2="60" y2="95" stroke="#1e293b" stroke-width="5"/><path d="M 20 60 L 10 50 L 30 50 Z" fill="#ef4444"/></svg>`
                };
            }
        }

        function updateMascot() {
            const data = getMascotData();
            document.getElementById('mascot-svg-wrapper').innerHTML = `<div class="mascot-svg">${data.svg}</div>`;
            document.getElementById('mascot-name').innerText = data.name;
            document.getElementById('mascot-desc').innerText = data.desc;
        }

        function updateStatsUI() {
            document.getElementById('level-display').innerText = `Nivel ${state.level}`;
            const xpForNext = state.level * 100;
            const percentage = (state.xp / xpForNext) * 100;
            document.getElementById('xp-bar').style.width = `${percentage}%`;
            document.getElementById('achievements-display').innerText = state.achievements.length;
        }

        function updateProgressUI() {
            const cats = ['patrones', 'logica', 'geometria', 'conteo', 'divisibilidad', 'error', 'olimpico'];
            const progress = state.progress || {};
            cats.forEach(cat => {
                const count = progress[cat] || 0;
                const pct = Math.min(count / 20, 1) * 100;
                const barEl = document.getElementById(`prog-${cat}`);
                const labelEl = document.getElementById(`prog-${cat}-label`);
                if (barEl) barEl.style.width = `${pct}%`;
                if (labelEl) labelEl.innerText = `${count} resueltos`;
            });
        }

        function gainXP(amount) {
            state.xp += amount;
            let xpForNext = state.level * 100;
            while (state.xp >= xpForNext) {
                state.xp -= xpForNext;
                state.level++;
                xpForNext = state.level * 100;
                alert(`¡Felicidades! Has alcanzado el Nivel ${state.level} 🏆`);
            }
            saveState();
            updateStatsUI();
        }

        // Gameplay
        function startModule(category) {
            state.competencia.active = false;
            document.getElementById('competencia-tracker').style.display = 'none';
            document.getElementById('mode-indicator').innerText = `Entrenamiento: ${category.toUpperCase()}`;
            currentModule = category;
            loadNextProblem();
            showScreen('play');
        }

        function startCompetencia() {
            state.competencia = {
                active: true,
                stageIndex: 0,
                problemCount: 0,
                correctCount: 0
            };
            document.getElementById('competencia-tracker').style.display = 'flex';
            updateCompetenciaUI();
            currentModule = 'olimpico'; // Mezcla de problemas
            loadNextProblem();
            showScreen('play');
        }

        function updateCompetenciaUI() {
            const st = state.competencia;
            document.getElementById('mode-indicator').innerText = `🏆 Competencia Oficial: Instancia ${stages[st.stageIndex]} (${st.problemCount}/3)`;
            for(let i=0; i<5; i++) {
                const node = document.getElementById(`stage-${i}`);
                node.className = 'stage-node';
                if(i < st.stageIndex) node.classList.add('passed');
                if(i === st.stageIndex) node.classList.add('active');
            }
        }

        function loadNextProblem() {
            document.getElementById('feedback').style.display = 'none';
            document.getElementById('answer-input').value = '';
            document.getElementById('answer-input').disabled = false;
            document.getElementById('svg-workspace').style.display = 'none';
            document.getElementById('svg-workspace').innerHTML = '';

            let available;
            if (state.competencia.active) {
                // La competencia es de respuesta numérica: excluimos 'Encuentra el Error' (respuesta de texto).
                const diff = Math.min(Math.floor(state.competencia.stageIndex / 2) + 1, 3);
                available = problemBank.filter(p => p.dificultad === diff && p.categoria !== 'error');
                if (available.length === 0) available = problemBank.filter(p => p.categoria !== 'error');
            } else {
                available = problemBank.filter(p => p.categoria === currentModule);
                if (available.length === 0) available = problemBank;
            }

            // Evita repetir los últimos N problemas (N se adapta al tamaño del bucket).
            const windowSize = Math.min(5, Math.max(0, available.length - 1));
            let candidates = available.filter(p => !recentIds.includes(p.id));
            if (candidates.length === 0) candidates = available;
            const randomIndex = Math.floor(Math.random() * candidates.length);
            currentProblem = candidates[randomIndex];
            recentIds.push(currentProblem.id);
            while (recentIds.length > windowSize) recentIds.shift();

            document.getElementById('problem-category').innerText = `MÓDULO: ${currentProblem.categoria}`;
            document.getElementById('problem-statement').innerText = currentProblem.enunciado;

            // Easter egg interactive SVG for Geometry
            if (currentProblem.categoria === 'geometria') {
                setupInteractiveGeometry();
            }
        }

        // Dibuja la figura concreta del problema usando currentProblem.figura.
        // Solo rotula los datos DADOS en el enunciado, nunca la respuesta.
        function setupInteractiveGeometry() {
            const svg = document.getElementById('svg-workspace');
            const fig = currentProblem.figura;
            if (!fig) { svg.style.display = 'none'; svg.innerHTML = ''; return; }
            svg.style.display = 'block';

            const width = svg.clientWidth || 800;
            const height = 300;
            const cx = width / 2, cy = height / 2;

            const STROKE = '#3b82f6';            // --accent-primary
            const FILL = 'rgba(59,130,246,0.25)';
            const GIVEN = '#f59e0b';             // --accent-warning (datos del enunciado)
            const MUTED = '#cbd5e1';             // --text-muted

            const txt = (x, y, t, color, size, anchor) =>
                `<text x="${x}" y="${y}" fill="${color || '#f8fafc'}" font-size="${size || 16}" ` +
                `font-family="system-ui, sans-serif" font-weight="600" text-anchor="${anchor || 'middle'}">${t}</text>`;
            const vertex = (x, y) =>
                `<circle cx="${x}" cy="${y}" class="interactive-vertex" onclick="flashVertex(this)"/>`;

            // Grilla de fondo
            let grid = '';
            for (let i = 0; i < width; i += 20) grid += `<line x1="${i}" y1="0" x2="${i}" y2="${height}" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>`;
            for (let i = 0; i < height; i += 20) grid += `<line x1="0" y1="${i}" x2="${width}" y2="${i}" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>`;

            let shape = '';

            if (fig.tipo === 'rect_dos_cuadrados') {
                // Dos cuadrados iguales unidos -> rectángulo 2:1. Dato dado: el lado.
                const s = 90, w = s * 2, h = s;
                const x0 = cx - w / 2, y0 = cy - h / 2 + 10;
                shape += `<rect x="${x0}" y="${y0}" width="${w}" height="${h}" fill="${FILL}" stroke="${STROKE}" stroke-width="3"/>`;
                shape += `<line x1="${cx}" y1="${y0}" x2="${cx}" y2="${y0 + h}" stroke="${STROKE}" stroke-width="2" stroke-dasharray="7"/>`;
                // Acotación del lado (dato)
                shape += `<line x1="${x0 - 14}" y1="${y0}" x2="${x0 - 14}" y2="${y0 + h}" stroke="${GIVEN}" stroke-width="1.5"/>`;
                shape += txt(x0 - 22, cy + 15, `${fig.lado} cm`, GIVEN, 15, 'end');
                shape += txt(x0 + s / 2, y0 - 12, `${fig.lado} cm`, GIVEN, 14, 'middle');
                shape += txt(cx, y0 + h + 32, 'Dos cuadrados iguales unidos', MUTED, 13, 'middle');
                [[x0, y0], [cx, y0], [x0 + w, y0], [x0, y0 + h], [cx, y0 + h], [x0 + w, y0 + h]].forEach(p => shape += vertex(p[0], p[1]));

            } else if (fig.tipo === 'triangulo') {
                // Triángulo con base y área dadas; la altura es la incógnita (NO se rotula).
                const bw = 200, th = 150;
                const ax = cx - 30, ay = cy - th / 2;          // vértice superior (no centrado, genérico)
                const blx = cx - bw / 2, brx = cx + bw / 2, by = cy + th / 2;
                shape += `<polygon points="${ax},${ay} ${brx},${by} ${blx},${by}" fill="${FILL}" stroke="${STROKE}" stroke-width="3"/>`;
                // Altura punteada con marca de ángulo recto (sin rotular su valor)
                shape += `<line x1="${ax}" y1="${ay}" x2="${ax}" y2="${by}" stroke="${MUTED}" stroke-width="1.5" stroke-dasharray="5"/>`;
                shape += `<path d="M ${ax} ${by - 12} L ${ax + 12} ${by - 12} L ${ax + 12} ${by}" fill="none" stroke="${MUTED}" stroke-width="1.5"/>`;
                shape += txt(ax + 20, cy, 'altura = ?', MUTED, 13, 'start');
                // Datos dados
                shape += `<line x1="${blx}" y1="${by + 14}" x2="${brx}" y2="${by + 14}" stroke="${GIVEN}" stroke-width="1.5"/>`;
                shape += txt(cx, by + 32, `base = ${fig.base} cm`, GIVEN, 15, 'middle');
                shape += txt(cx - 5, by - 28, `Área = ${fig.area} cm²`, GIVEN, 15, 'middle');
                [[ax, ay], [brx, by], [blx, by]].forEach(p => shape += vertex(p[0], p[1]));

            } else if (fig.tipo === 'cuadrado_4') {
                // Cuadrado grande dividido en 4 cuadraditos iguales. Dato: perímetro del cuadradito.
                const S = 170, x0 = cx - S / 2, y0 = cy - S / 2 + 6, m = S / 2;
                shape += `<rect x="${x0}" y="${y0}" width="${S}" height="${S}" fill="${FILL}" stroke="${STROKE}" stroke-width="3"/>`;
                shape += `<line x1="${x0 + m}" y1="${y0}" x2="${x0 + m}" y2="${y0 + S}" stroke="${STROKE}" stroke-width="2" stroke-dasharray="7"/>`;
                shape += `<line x1="${x0}" y1="${y0 + m}" x2="${x0 + S}" y2="${y0 + m}" stroke="${STROKE}" stroke-width="2" stroke-dasharray="7"/>`;
                // Resalta un cuadradito y rotula su perímetro (dato)
                shape += `<rect x="${x0}" y="${y0}" width="${m}" height="${m}" fill="rgba(245,158,11,0.18)" stroke="${GIVEN}" stroke-width="2"/>`;
                shape += txt(x0 + m / 2, y0 + m / 2 + 5, `P = ${fig.perimetro_pequeno} cm`, GIVEN, 13, 'middle');
                shape += txt(cx, y0 + S + 30, 'Cuatro cuadraditos iguales', MUTED, 13, 'middle');
                [[x0, y0], [x0 + S, y0], [x0, y0 + S], [x0 + S, y0 + S]].forEach(p => shape += vertex(p[0], p[1]));

            } else {
                svg.style.display = 'none'; svg.innerHTML = ''; return;
            }

            svg.innerHTML = grid + shape;
        }

        window.flashVertex = function(el) {
            el.setAttribute('fill', '#f59e0b');
            el.setAttribute('r', '10');
            setTimeout(() => {
                el.setAttribute('fill', 'white');
                el.setAttribute('r', '6');
            }, 300);
        }

        function showHint() {
            if(currentProblem.pista) {
                alert("Pista del Entrenador: " + currentProblem.pista);
            } else {
                alert("¡Tú puedes! Lee con cuidado y haz un dibujo.");
            }
        }

        window.checkAnswer = function() {
            const input = document.getElementById('answer-input').value.trim().toLowerCase();
            if (!input) return;

            const correct = String(currentProblem.respuesta).trim().toLowerCase();
            const normalize = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '');
            const isMatch = normalize(input) === normalize(correct);

            document.getElementById('answer-input').disabled = true;
            const feedback = document.getElementById('feedback');
            
            if (isMatch) {
                feedback.className = 'feedback success';
                document.getElementById('feedback-title').innerText = '¡Excelente Resolución! ✨';
                gainXP(20 * currentProblem.dificultad);
                if (!state.progress) state.progress = {};
                state.progress[currentProblem.categoria] = (state.progress[currentProblem.categoria] || 0) + 1;
                updateProgressUI();

                if (state.competencia.active) {
                    state.competencia.correctCount++;
                }
            } else {
                feedback.className = 'feedback error';
                document.getElementById('feedback-title').innerText = 'Hay un detalle para revisar... 🤔';
            }

            document.getElementById('feedback-desc').innerHTML = `
                <strong>Respuesta correcta:</strong> ${currentProblem.respuesta}<br><br>
                <strong>Estrategia Olímpica:</strong><br> ${currentProblem.explicacion}
            `;
            feedback.style.display = 'block';

            if (state.competencia.active) {
                state.competencia.problemCount++;
                if (state.competencia.problemCount >= 3) {
                    document.getElementById('next-problem-btn').innerText = "Ver Resultado de la Etapa";
                } else {
                    document.getElementById('next-problem-btn').innerText = "Siguiente Problema →";
                    updateCompetenciaUI();
                }
            }
        }

        window.nextProblem = function() {
            if (state.competencia.active && state.competencia.problemCount >= 3) {
                // Etapa finalizada
                if (state.competencia.correctCount >= 2) {
                    // Aprueba
                    alert(`¡Felicitaciones! Aprobaste el certamen ${stages[state.competencia.stageIndex]} con ${state.competencia.correctCount}/3 correctas.`);
                    gainXP(100 * (state.competencia.stageIndex + 1));
                    state.competencia.stageIndex++;
                    state.competencia.problemCount = 0;
                    state.competencia.correctCount = 0;

                    if (state.competencia.stageIndex >= 5) {
                        alert("¡INCREÍBLE! ¡Eres CAMPEÓN NACIONAL! Has completado el juego.");
                        if(!state.achievements.includes("CampeonNacional")) {
                            state.achievements.push("CampeonNacional");
                        }
                        showScreen('home');
                    } else {
                        updateCompetenciaUI();
                        loadNextProblem();
                    }
                } else {
                    // Desaprueba
                    alert(`No alcanzaste los 2 puntos necesarios en el certamen ${stages[state.competencia.stageIndex]}. ¡Sigue entrenando!`);
                    showScreen('home');
                }
            } else {
                loadNextProblem();
            }
        }

        // Boot
        init();

    </script>
</body>
</html>
"""

html_template = html_template.replace("PLACEHOLDER_JSON", problems_json)

with open("mision_nandu.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated mision_nandu.html successfully.")

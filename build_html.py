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

        .module-card.dimmed { opacity: 0.5; }

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

        .comp-timer-label {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            justify-content: center;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.8rem;
            cursor: pointer;
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
            margin-bottom: 1rem;
            flex-wrap: wrap;
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

        /* Opción múltiple (Encuentra el Error) */
        #options-container {
            display: none;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin-bottom: 1rem;
        }
        .btn-option {
            background: rgba(255,255,255,0.08);
            border: 2px solid rgba(255,255,255,0.2);
            color: white;
            flex: 1 1 45%;
            text-align: left;
            font-size: 1rem;
        }
        .btn-option:hover:not(:disabled) {
            border-color: var(--accent-primary);
            transform: translateY(-2px);
        }
        .btn-option:disabled { cursor: default; }
        .btn-option.ok {
            border-color: var(--accent-success);
            background: rgba(16, 185, 129, 0.25);
        }
        .btn-option.mal {
            border-color: var(--accent-error);
            background: rgba(239, 68, 68, 0.25);
            opacity: 0.85;
        }

        /* Pista inline */
        .hint-box {
            display: none;
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid var(--accent-warning);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            line-height: 1.5;
        }
        .hint-cost {
            display: block;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.4rem;
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

        /* Segundo intento pendiente */
        .feedback.retry {
            display: block;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid var(--accent-warning);
        }

        /* Respuesta registrada en competencia (sin revelar corrección) */
        .feedback.neutral {
            display: block;
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid var(--accent-primary);
        }

        /* Timer de competencia */
        #timer-display {
            display: none;
            text-align: center;
            font-weight: 900;
            font-size: 1.3rem;
            letter-spacing: 2px;
            background: rgba(255,255,255,0.06);
            border-radius: 10px;
            padding: 0.4rem 1rem;
            margin-bottom: 1rem;
        }
        #timer-display.warning {
            color: var(--accent-error);
            animation: pulseTimer 1s infinite;
        }
        @keyframes pulseTimer { 50% { opacity: 0.55; } }

        /* Resumen de etapa */
        .summary-item {
            border: 1px solid rgba(255,255,255,0.15);
            border-left-width: 5px;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .summary-item.ok { border-left-color: var(--accent-success); }
        .summary-item.mal { border-left-color: var(--accent-error); }
        .summary-enunciado {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin: 0.4rem 0;
        }
        .summary-expl {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.5rem;
            border-top: 1px dashed rgba(255,255,255,0.15);
            padding-top: 0.5rem;
        }

        /* Modal propio (reemplaza a los alert() del navegador) */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(2, 6, 23, 0.75);
            backdrop-filter: blur(4px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 200;
            padding: 1rem;
        }
        .modal-overlay.visible { display: flex; }
        .modal-card {
            background: var(--bg-secondary);
            border: 1px solid rgba(139, 92, 246, 0.4);
            border-radius: 20px;
            padding: 2rem;
            max-width: 640px;
            width: 100%;
            max-height: 85vh;
            overflow-y: auto;
            box-shadow: 0 25px 60px rgba(0,0,0,0.6);
            animation: fadeIn 0.25s ease-out;
        }
        .modal-card h2 { margin-bottom: 1rem; }
        .modal-body { color: var(--text-muted); line-height: 1.5; }
        .modal-actions {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
            justify-content: flex-end;
            flex-wrap: wrap;
        }

        /* Toasts (avisos no bloqueantes) */
        #toast-container {
            position: fixed;
            bottom: 1.5rem;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            z-index: 300;
            align-items: center;
        }
        .toast {
            background: var(--bg-secondary);
            border: 1px solid var(--accent-secondary);
            padding: 0.8rem 1.4rem;
            border-radius: 30px;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.35s ease;
            max-width: 90vw;
        }
        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }

        /* Panel del Entrenador */
        .panel-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }
        .panel-table th, .panel-table td {
            padding: 0.7rem 0.5rem;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .panel-table th {
            color: var(--text-muted);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
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
            .btn-option { flex: 1 1 100%; }
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
        <div class="title-logo" style="cursor: pointer" onclick="volverAlInicio()">Misión Ñandú</div>
        <div class="user-stats">
            <div class="stat-badge">
                🏆 <span id="level-display">Nivel 1</span>
                <div class="xp-bar-container"><div class="xp-bar-fill" id="xp-bar"></div></div>
            </div>
            <div class="stat-badge" title="Días seguidos entrenando">
                🔥 <span id="streak-display">0</span>
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
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Descubrí secuencias numéricas ocultas.</div>
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
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Dominá perímetros y áreas con precisión.</div>
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
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Analizá resoluciones falsas.</div>
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
                    <div class="module-card" id="revancha-card" onclick="startRevancha()">
                        <div class="module-icon">🔁</div>
                        <div class="module-title">Revancha</div>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Volvé a enfrentar los problemas que te ganaron.</div>
                        <div class="module-progress-label" id="revancha-label" style="margin-top: 0.8rem;">Sin pendientes</div>
                    </div>
                </div>

                <div>
                    <div class="mascot-container">
                        <div id="mascot-svg-wrapper">
                            <!-- SVG Mascot injected here based on level -->
                        </div>
                        <h3 style="margin-bottom: 0.5rem;" id="mascot-name">Huevo Matemático</h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;" id="mascot-desc">Resolvé problemas para evolucionar tu Ñandú.</p>

                        <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1)">
                            <h3>Modo Competencia</h3>
                            <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1rem;">Simulá las 5 instancias oficiales.</p>
                            <button class="competencia-btn" onclick="startCompetencia()">¡Inscribirse!</button>
                            <label class="comp-timer-label">
                                <input type="checkbox" id="comp-timer-check"> ⏱️ Contrarreloj (15 min por etapa)
                            </label>
                        </div>
                        <button class="btn btn-secondary" style="width: 100%; margin-top: 1.5rem; font-size: 0.95rem;" onclick="showScreen('panel')">📊 Panel del Entrenador</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Problem Playing Screen -->
        <div id="play" class="screen">
            <div class="play-area">
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <button class="btn btn-secondary" style="padding: 0.5rem 1rem" onclick="volverAlInicio()">← Volver</button>
                    <div id="mode-indicator" style="color: var(--accent-warning); font-weight: bold; align-self: center;">Entrenamiento</div>
                </div>

                <div id="competencia-tracker" class="stage-tracker" style="display: none;">
                    <div class="stage-node" id="stage-0" title="Escolar">1</div>
                    <div class="stage-node" id="stage-1" title="Intercolegial">2</div>
                    <div class="stage-node" id="stage-2" title="Zonal">3</div>
                    <div class="stage-node" id="stage-3" title="Regional">4</div>
                    <div class="stage-node" id="stage-4" title="Nacional">5</div>
                </div>

                <div id="timer-display">⏱️ 15:00</div>

                <div id="problem-category" style="text-transform: uppercase; letter-spacing: 2px; color: var(--accent-secondary); font-size: 0.9rem; font-weight: 700; margin-bottom: 1rem;">CATEGORIA</div>

                <!-- Interactive SVG Canvas for Geometry -->
                <svg id="svg-workspace"></svg>

                <div class="problem-statement" id="problem-statement">
                    Cargando problema...
                </div>

                <!-- Opciones para problemas de opción múltiple -->
                <div id="options-container"></div>

                <div class="answer-section">
                    <input type="text" id="answer-input" class="answer-input" placeholder="Tu respuesta final..." onkeypress="if(event.key === 'Enter') checkAnswer()">
                    <button class="btn btn-primary" id="responder-btn" onclick="checkAnswer()">Responder</button>
                    <button class="btn btn-secondary" onclick="showHint()" id="hint-btn">💡 Pista</button>
                </div>

                <div class="hint-box" id="hint-box"></div>

                <div id="feedback" class="feedback">
                    <h3 id="feedback-title" style="margin-bottom: 0.5rem;"></h3>
                    <p id="feedback-desc"></p>
                    <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                        <button class="btn btn-primary" id="next-problem-btn" onclick="nextProblem()">Siguiente Problema →</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Coach Panel Screen -->
        <div id="panel" class="screen">
            <div class="play-area">
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <button class="btn btn-secondary" style="padding: 0.5rem 1rem" onclick="showScreen('home')">← Volver</button>
                </div>
                <h2 style="margin-bottom: 0.5rem;">📊 Panel del Entrenador</h2>
                <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">Cómo viene el entrenamiento, módulo por módulo.</p>
                <div id="panel-resumen" style="line-height: 1.8;"></div>
                <table class="panel-table">
                    <thead>
                        <tr><th>Módulo</th><th>Intentos</th><th>Correctos</th><th>Precisión</th></tr>
                    </thead>
                    <tbody id="panel-body"></tbody>
                </table>
                <div class="hint-box" id="panel-reco" style="display: block;"></div>
                <button class="btn btn-secondary" style="margin-top: 1rem; font-size: 0.9rem;" onclick="confirmarReinicio()">🗑️ Borrar todo el progreso</button>
            </div>
        </div>

    </main>

    <!-- Modal genérico (reemplaza a los alert()) -->
    <div id="modal-overlay" class="modal-overlay">
        <div class="modal-card">
            <h2 id="modal-title"></h2>
            <div id="modal-body" class="modal-body"></div>
            <div class="modal-actions">
                <button class="btn btn-secondary" id="modal-secondary" onclick="modalSecondary()"></button>
                <button class="btn btn-primary" id="modal-primary" onclick="modalPrimary()"></button>
            </div>
        </div>
    </div>

    <div id="toast-container"></div>

    <script>
        // Data
        const problemBank = PLACEHOLDER_JSON;

        // State
        let state = {
            xp: 0,
            level: 1,
            achievements: [],
            stats: {},        // por categoría: { intentos, aciertos }
            errores: [],      // problemas fallados pendientes de revancha: [{ id, ts, veces }]
            racha: { dias: 0, ultimoDia: null },
            competencia: {
                active: false,
                stageIndex: 0, // 0: Escolar, 1: Intercolegial, 2: Zonal, 3: Regional, 4: Nacional
                problemCount: 0,
                conTimer: false,
                stageAnswers: [] // respuestas de la etapa en curso (la corrección se revela al final)
            }
        };

        const stages = ["Escolar", "Intercolegial", "Zonal", "Regional", "Nacional"];
        const NOMBRES_CAT = {
            patrones: "Detective de Patrones",
            logica: "Laboratorio de Estrategias",
            geometria: "Geometría Ninja",
            conteo: "Cuenta Caminos",
            divisibilidad: "Cofre de Divisibilidad",
            error: "Encuentra el Error",
            olimpico: "Problema Olímpico"
        };
        const TIEMPO_ETAPA = 15 * 60; // segundos por etapa en modo contrarreloj

        let currentProblem = null;
        let currentModule = null;
        let recentIds = [];          // ids mostrados recientemente, para no repetir los últimos N
        let attemptsOnCurrent = 0;   // intentos sobre el problema actual
        let hintUsed = false;        // si pidió pista en el problema actual
        let problemaResuelto = false;
        let timerInterval = null;
        let timerRestante = 0;

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
            // anterior no debe dejar claves sin definir.
            const defaultCompetencia = state.competencia;
            state = Object.assign({}, state, parsed);
            state.competencia = Object.assign({}, defaultCompetencia, parsed.competencia || {});
            // Una competencia a medias no sobrevive a recargar la página: se abandona.
            state.competencia.active = false;
            state.competencia.stageAnswers = [];
            if (!Array.isArray(state.achievements)) state.achievements = [];
            if (typeof state.xp !== 'number') state.xp = 0;
            if (typeof state.level !== 'number') state.level = 1;
            if (!state.stats || typeof state.stats !== 'object') state.stats = {};
            if (!Array.isArray(state.errores)) state.errores = [];
            if (!state.racha || typeof state.racha !== 'object') state.racha = { dias: 0, ultimoDia: null };
            // Migración desde versiones que solo guardaban 'progress' (resueltos por categoría).
            if (parsed.progress && typeof parsed.progress === 'object' && !parsed.stats) {
                for (const cat in parsed.progress) {
                    const n = parsed.progress[cat] || 0;
                    state.stats[cat] = { intentos: n, aciertos: n };
                }
            }
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
            if (id === 'panel') updatePanelUI();
        }

        window.volverAlInicio = function() {
            if (state.competencia.active) {
                showModal({
                    titulo: '¿Abandonar la competencia?',
                    html: 'Si salís ahora perdés el avance de esta competencia (el XP ganado se conserva).',
                    primario: 'Seguir compitiendo',
                    secundario: 'Salir',
                    onSecundario: () => { abandonarCompetencia(); showScreen('home'); }
                });
                return;
            }
            showScreen('home');
        }

        // Modal genérico
        let modalPrimaryAction = null;
        let modalSecondaryAction = null;

        function showModal(opts) {
            document.getElementById('modal-title').innerHTML = opts.titulo || '';
            document.getElementById('modal-body').innerHTML = opts.html || '';
            const prim = document.getElementById('modal-primary');
            const sec = document.getElementById('modal-secondary');
            prim.innerText = opts.primario || 'Entendido';
            modalPrimaryAction = opts.onPrimario || null;
            if (opts.secundario) {
                sec.style.display = '';
                sec.innerText = opts.secundario;
                modalSecondaryAction = opts.onSecundario || null;
            } else {
                sec.style.display = 'none';
                modalSecondaryAction = null;
            }
            document.getElementById('modal-overlay').classList.add('visible');
        }

        function closeModal() {
            document.getElementById('modal-overlay').classList.remove('visible');
        }

        window.modalPrimary = function() {
            closeModal();
            if (modalPrimaryAction) modalPrimaryAction();
        }

        window.modalSecondary = function() {
            closeModal();
            if (modalSecondaryAction) modalSecondaryAction();
        }

        // Toasts no bloqueantes
        function toast(mensaje) {
            const cont = document.getElementById('toast-container');
            const el = document.createElement('div');
            el.className = 'toast';
            el.innerHTML = mensaje;
            cont.appendChild(el);
            setTimeout(() => el.classList.add('show'), 10);
            setTimeout(() => {
                el.classList.remove('show');
                setTimeout(() => el.remove(), 400);
            }, 3200);
        }

        const escHtml = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

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
            document.getElementById('streak-display').innerText = state.racha.dias;
        }

        function updateProgressUI() {
            const cats = Object.keys(NOMBRES_CAT);
            cats.forEach(cat => {
                const s = state.stats[cat] || { intentos: 0, aciertos: 0 };
                const pct = Math.min(s.aciertos / 20, 1) * 100;
                const barEl = document.getElementById(`prog-${cat}`);
                const labelEl = document.getElementById(`prog-${cat}-label`);
                if (barEl) barEl.style.width = `${pct}%`;
                if (labelEl) labelEl.innerText = `${s.aciertos} resueltos`;
            });
            const pendientes = state.errores.length;
            document.getElementById('revancha-label').innerText = pendientes
                ? `${pendientes} problema${pendientes === 1 ? '' : 's'} esperando revancha`
                : 'Sin pendientes ¡bien ahí!';
            document.getElementById('revancha-card').classList.toggle('dimmed', pendientes === 0);
        }

        function updatePanelUI() {
            let filas = '';
            let totInt = 0, totOk = 0;
            let peor = null;
            for (const cat of Object.keys(NOMBRES_CAT)) {
                const s = state.stats[cat] || { intentos: 0, aciertos: 0 };
                totInt += s.intentos;
                totOk += s.aciertos;
                const prec = s.intentos ? Math.round(100 * s.aciertos / s.intentos) : null;
                // Solo sugerimos módulos con suficientes intentos como para que la precisión diga algo.
                if (s.intentos >= 5 && (peor === null || prec < peor.prec)) peor = { nombre: NOMBRES_CAT[cat], prec };
                filas += `<tr><td>${NOMBRES_CAT[cat]}</td><td>${s.intentos}</td><td>${s.aciertos}</td><td>${prec === null ? '—' : prec + '%'}</td></tr>`;
            }
            document.getElementById('panel-body').innerHTML = filas;
            document.getElementById('panel-resumen').innerHTML =
                `🔥 Racha: <strong>${state.racha.dias} día${state.racha.dias === 1 ? '' : 's'}</strong> seguidos · ` +
                `✅ <strong>${totOk}</strong> correctos sobre <strong>${totInt}</strong> intentos · ` +
                `🔁 <strong>${state.errores.length}</strong> pendientes de revancha`;
            let reco;
            if (peor && peor.prec < 85) {
                reco = `🎯 Sugerencia: hoy conviene entrenar <strong>${peor.nombre}</strong> (precisión ${peor.prec}%).`;
            } else if (totInt < 10) {
                reco = '🧭 Jugá un poco más y acá va a aparecer una sugerencia de qué entrenar.';
            } else {
                reco = '🌟 Vas muy parejo en todos los módulos. ¡Probá el Modo Competencia!';
            }
            document.getElementById('panel-reco').innerHTML = reco;
        }

        window.confirmarReinicio = function() {
            showModal({
                titulo: '¿Borrar todo el progreso?',
                html: 'Se pierde el nivel, el XP, la racha, las estadísticas y la lista de revancha. No hay vuelta atrás.',
                primario: 'Cancelar',
                secundario: 'Sí, borrar todo',
                onSecundario: () => {
                    localStorage.removeItem('nandu_state');
                    location.reload();
                }
            });
        }

        function gainXP(amount) {
            state.xp += amount;
            let xpForNext = state.level * 100;
            while (state.xp >= xpForNext) {
                state.xp -= xpForNext;
                state.level++;
                xpForNext = state.level * 100;
                toast(`🏆 ¡Subiste al Nivel ${state.level}! Tu ñandú está creciendo.`);
                updateMascot();
            }
            saveState();
            updateStatsUI();
        }

        // Racha de días entrenando (cuenta días con al menos un problema correcto).
        function hoyKey(offsetDias) {
            const d = new Date(Date.now() + (offsetDias || 0) * 86400000);
            return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
        }

        function actualizarRacha() {
            const hoy = hoyKey(0);
            if (state.racha.ultimoDia === hoy) return;
            state.racha.dias = (state.racha.ultimoDia === hoyKey(-1)) ? state.racha.dias + 1 : 1;
            state.racha.ultimoDia = hoy;
            if (state.racha.dias > 1) toast(`🔥 ¡Racha de ${state.racha.dias} días entrenando!`);
            updateStatsUI();
        }

        // Estadísticas y cola de revancha
        function registrarResultado(categoria, correcto) {
            if (!categoria) return;
            if (!state.stats[categoria]) state.stats[categoria] = { intentos: 0, aciertos: 0 };
            state.stats[categoria].intentos++;
            if (correcto) state.stats[categoria].aciertos++;
        }

        function agregarAErrores(id) {
            if (id == null) return;
            const e = state.errores.find(x => x.id === id);
            if (e) {
                e.veces++;
                e.ts = Date.now();
            } else {
                state.errores.push({ id, ts: Date.now(), veces: 1 });
            }
        }

        function quitarDeErrores(id) {
            const i = state.errores.findIndex(x => x.id === id);
            if (i >= 0) {
                state.errores.splice(i, 1);
                if (currentModule === 'revancha') toast('🎯 ¡Revancha ganada!');
            }
        }

        // Gameplay
        function startModule(category) {
            state.competencia.active = false;
            detenerTimer();
            document.getElementById('competencia-tracker').style.display = 'none';
            document.getElementById('mode-indicator').innerText = `Entrenamiento: ${NOMBRES_CAT[category] || category}`;
            currentModule = category;
            loadNextProblem();
            showScreen('play');
        }

        window.startRevancha = function() {
            if (!state.errores.length) {
                toast('🎉 No tenés problemas pendientes. ¡A entrenar otro módulo!');
                return;
            }
            state.competencia.active = false;
            detenerTimer();
            document.getElementById('competencia-tracker').style.display = 'none';
            document.getElementById('mode-indicator').innerText = '🔁 Revancha';
            currentModule = 'revancha';
            loadNextProblem();
            showScreen('play');
        }

        function startCompetencia() {
            state.competencia = {
                active: true,
                stageIndex: 0,
                problemCount: 0,
                conTimer: document.getElementById('comp-timer-check').checked,
                stageAnswers: []
            };
            document.getElementById('competencia-tracker').style.display = 'flex';
            currentModule = 'olimpico'; // Mezcla de problemas
            if (state.competencia.conTimer) iniciarTimer();
            loadNextProblem();
            showScreen('play');
        }

        function abandonarCompetencia() {
            state.competencia.active = false;
            state.competencia.stageAnswers = [];
            detenerTimer();
            document.getElementById('competencia-tracker').style.display = 'none';
            saveState();
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

        // Timer de competencia (opcional)
        function iniciarTimer() {
            detenerTimer();
            timerRestante = TIEMPO_ETAPA;
            const disp = document.getElementById('timer-display');
            disp.style.display = 'block';
            pintarTimer();
            timerInterval = setInterval(() => {
                timerRestante--;
                pintarTimer();
                if (timerRestante <= 0) tiempoAgotado();
            }, 1000);
        }

        function detenerTimer() {
            if (timerInterval) clearInterval(timerInterval);
            timerInterval = null;
            const disp = document.getElementById('timer-display');
            disp.style.display = 'none';
            disp.classList.remove('warning');
        }

        function pintarTimer() {
            const disp = document.getElementById('timer-display');
            const m = Math.max(0, Math.floor(timerRestante / 60));
            const s = Math.max(0, timerRestante % 60);
            disp.innerText = `⏱️ ${m}:${String(s).padStart(2, '0')}`;
            disp.classList.toggle('warning', timerRestante <= 60);
        }

        function tiempoAgotado() {
            detenerTimer();
            const st = state.competencia;
            if (!st.active) return;
            // Los problemas que quedaron sin responder cuentan como incorrectos.
            while (st.stageAnswers.length < 3) {
                st.stageAnswers.push({
                    id: null, categoria: null, dificultad: 0,
                    enunciado: '(Sin responder: se acabó el tiempo)',
                    dada: '—', respuesta: '—', explicacion: '', correcto: false
                });
            }
            st.problemCount = 3;
            showStageSummary();
        }

        function loadNextProblem() {
            document.getElementById('feedback').style.display = 'none';
            document.getElementById('feedback').className = 'feedback';
            document.getElementById('answer-input').value = '';
            document.getElementById('answer-input').disabled = false;
            document.getElementById('next-problem-btn').innerText = 'Siguiente Problema →';
            document.getElementById('svg-workspace').style.display = 'none';
            document.getElementById('svg-workspace').innerHTML = '';
            const hintBox = document.getElementById('hint-box');
            hintBox.style.display = 'none';
            hintBox.innerHTML = '';
            const hintBtn = document.getElementById('hint-btn');
            hintBtn.disabled = false;
            // En el certamen real no hay pistas: las deshabilitamos en competencia.
            hintBtn.style.display = state.competencia.active ? 'none' : '';
            attemptsOnCurrent = 0;
            hintUsed = false;
            problemaResuelto = false;

            let available;
            if (state.competencia.active) {
                // La competencia es de respuesta escrita: excluimos los de opción múltiple.
                const diff = Math.min(Math.floor(state.competencia.stageIndex / 2) + 1, 3);
                available = problemBank.filter(p => p.dificultad === diff && p.categoria !== 'error');
                if (available.length === 0) available = problemBank.filter(p => p.categoria !== 'error');
            } else if (currentModule === 'revancha') {
                const ids = state.errores.map(e => e.id);
                available = problemBank.filter(p => ids.includes(p.id));
                if (available.length === 0) {
                    toast('🎉 ¡No te queda ningún problema pendiente!');
                    showScreen('home');
                    return;
                }
                // El fallado hace más tiempo va primero.
                const orden = {};
                state.errores.forEach(e => { orden[e.id] = e.ts || 0; });
                available.sort((a, b) => (orden[a.id] || 0) - (orden[b.id] || 0));
            } else {
                available = problemBank.filter(p => p.categoria === currentModule);
                if (available.length === 0) available = problemBank;
            }

            // Evita repetir los últimos N problemas (N se adapta al tamaño del bucket).
            const windowSize = Math.min(5, Math.max(0, available.length - 1));
            let candidates = available.filter(p => !recentIds.includes(p.id));
            if (candidates.length === 0) candidates = available;
            currentProblem = (currentModule === 'revancha' && !state.competencia.active)
                ? candidates[0]
                : candidates[Math.floor(Math.random() * candidates.length)];
            recentIds.push(currentProblem.id);
            while (recentIds.length > windowSize) recentIds.shift();

            document.getElementById('problem-category').innerText = `MÓDULO: ${NOMBRES_CAT[currentProblem.categoria] || currentProblem.categoria}`;
            document.getElementById('problem-statement').innerText = currentProblem.enunciado;
            renderEntrada();

            // Easter egg interactive SVG for Geometry
            if (currentProblem.categoria === 'geometria') {
                setupInteractiveGeometry();
            }
            if (state.competencia.active) updateCompetenciaUI();
        }

        // Muestra el campo de texto o los botones de opción múltiple según el problema.
        function renderEntrada() {
            const input = document.getElementById('answer-input');
            const respBtn = document.getElementById('responder-btn');
            const cont = document.getElementById('options-container');
            cont.innerHTML = '';
            if (Array.isArray(currentProblem.opciones) && currentProblem.opciones.length) {
                input.style.display = 'none';
                respBtn.style.display = 'none';
                cont.style.display = 'flex';
                const ops = currentProblem.opciones.slice();
                for (let i = ops.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [ops[i], ops[j]] = [ops[j], ops[i]];
                }
                ops.forEach(op => {
                    const b = document.createElement('button');
                    b.className = 'btn btn-option';
                    b.innerText = op;
                    b.onclick = () => elegirOpcion(b, op);
                    cont.appendChild(b);
                });
            } else {
                cont.style.display = 'none';
                input.style.display = '';
                respBtn.style.display = '';
                // Teclado numérico en tablets/celulares cuando la respuesta es un número.
                input.setAttribute('inputmode', parseNumero(String(currentProblem.respuesta)) !== null ? 'numeric' : 'text');
                input.focus();
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

        window.showHint = function() {
            if (state.competencia.active || problemaResuelto) return;
            hintUsed = true;
            const box = document.getElementById('hint-box');
            box.innerHTML = '💡 <strong>Pista del Entrenador:</strong> ' +
                escHtml(currentProblem.pista || '¡Vos podés! Leé con cuidado y hacé un dibujo.') +
                '<span class="hint-cost">Resolver con pista da la mitad de XP.</span>';
            box.style.display = 'block';
            document.getElementById('hint-btn').disabled = true;
        }

        // --- Validación de respuestas ---

        // Interpreta "16", "16 cm", "1.000", "3,5" o "$ 120" como número.
        // Devuelve null si el texto no es una respuesta numérica.
        function parseNumero(s) {
            const m = String(s).trim().match(/^[^0-9\\-]*(-?\\d[\\d.,]*)\\s*[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ°º²³%$\\s.]*$/);
            if (!m) return null;
            let num = m[1].replace(/[.,]$/, '');
            const tienePunto = num.includes('.');
            const tieneComa = num.includes(',');
            if (tienePunto && tieneComa) {
                // "1.234,5": puntos de miles y coma decimal
                num = num.replace(/\\./g, '').replace(',', '.');
            } else if (tieneComa) {
                num = num.replace(',', '.');
            } else if (tienePunto && /^-?\\d{1,3}(\\.\\d{3})+$/.test(num)) {
                // "1.000" es mil, no uno: punto de miles
                num = num.replace(/\\./g, '');
            }
            const v = parseFloat(num);
            return isNaN(v) ? null : v;
        }

        function esRespuestaCorrecta(input, problema) {
            const normalizar = s => String(s).normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').trim().toLowerCase();
            const aceptadas = [problema.respuesta].concat(problema.respuestas_aceptadas || []);
            const numInput = parseNumero(input);
            return aceptadas.some(resp => {
                const numResp = parseNumero(resp);
                if (numInput !== null && numResp !== null) return Math.abs(numInput - numResp) < 1e-9;
                return normalizar(input) === normalizar(resp);
            });
        }

        window.checkAnswer = function() {
            const input = document.getElementById('answer-input').value.trim();
            if (!input || problemaResuelto) return;
            resolverRespuesta(input, null);
        }

        function elegirOpcion(btn, valor) {
            if (problemaResuelto || btn.disabled) return;
            resolverRespuesta(valor, btn);
        }

        function deshabilitarEntrada() {
            document.getElementById('answer-input').disabled = true;
            document.querySelectorAll('#options-container .btn-option').forEach(b => b.disabled = true);
        }

        function marcarOpciones(btnElegido, correcto) {
            document.querySelectorAll('#options-container .btn-option').forEach(b => {
                if (esRespuestaCorrecta(b.innerText, currentProblem)) b.classList.add('ok');
            });
            if (btnElegido && !correcto) btnElegido.classList.add('mal');
        }

        function resolverRespuesta(valor, btnElegido) {
            const correcto = esRespuestaCorrecta(valor, currentProblem);
            attemptsOnCurrent++;
            const feedback = document.getElementById('feedback');

            // En competencia no se corrige en el momento: se registra y se sigue.
            if (state.competencia.active) {
                problemaResuelto = true;
                deshabilitarEntrada();
                const st = state.competencia;
                st.stageAnswers.push({
                    id: currentProblem.id,
                    categoria: currentProblem.categoria,
                    dificultad: currentProblem.dificultad,
                    enunciado: currentProblem.enunciado,
                    dada: valor,
                    respuesta: currentProblem.respuesta,
                    explicacion: currentProblem.explicacion,
                    correcto
                });
                st.problemCount++;
                feedback.className = 'feedback neutral';
                document.getElementById('feedback-title').innerText = `Respuesta registrada (${st.problemCount}/3) 📝`;
                document.getElementById('feedback-desc').innerText = 'Como en el certamen real, la corrección llega al final de la etapa. ¡Seguí!';
                document.getElementById('next-problem-btn').innerText = st.problemCount >= 3 ? 'Ver resultado de la etapa' : 'Siguiente Problema →';
                feedback.style.display = 'block';
                updateCompetenciaUI();
                return;
            }

            // Entrenamiento: el primer error da una segunda oportunidad sin revelar la respuesta.
            if (!correcto && attemptsOnCurrent === 1) {
                if (btnElegido) {
                    btnElegido.classList.add('mal');
                    btnElegido.disabled = true;
                } else {
                    const inp = document.getElementById('answer-input');
                    inp.select();
                    inp.focus();
                }
                feedback.className = 'feedback retry';
                document.getElementById('feedback-title').innerText = '¡Casi! Probá una vez más 💪';
                document.getElementById('feedback-desc').innerText = 'Revisá tu cuenta con calma. Si querés, pedí una pista.';
                feedback.style.display = 'block';
                return;
            }

            // Resolución final del problema de entrenamiento.
            problemaResuelto = true;
            deshabilitarEntrada();
            if (btnElegido || document.querySelector('#options-container .btn-option')) marcarOpciones(btnElegido, correcto);
            registrarResultado(currentProblem.categoria, correcto);

            if (correcto) {
                let xp = 20 * currentProblem.dificultad;
                if (hintUsed || attemptsOnCurrent > 1) xp = Math.ceil(xp / 2);
                feedback.className = 'feedback success';
                document.getElementById('feedback-title').innerText = `¡Excelente Resolución! ✨ +${xp} XP`;
                quitarDeErrores(currentProblem.id);
                actualizarRacha();
                gainXP(xp);
            } else {
                feedback.className = 'feedback error';
                document.getElementById('feedback-title').innerText = 'Hay un detalle para revisar... 🤔';
                agregarAErrores(currentProblem.id);
            }

            document.getElementById('feedback-desc').innerHTML = `
                <strong>Respuesta correcta:</strong> ${currentProblem.respuesta}<br><br>
                <strong>Estrategia Olímpica:</strong><br> ${currentProblem.explicacion}
            `;
            feedback.style.display = 'block';
            updateProgressUI();
            saveState();
        }

        // Cierre de etapa de competencia: corrección completa + avance o salida.
        function showStageSummary() {
            detenerTimer();
            const st = state.competencia;
            const respuestas = st.stageAnswers.slice(0, 3);
            const aciertos = respuestas.filter(a => a.correcto).length;
            const aprobo = aciertos >= 2;
            const etapaActual = stages[st.stageIndex];

            // Recién acá impactan las estadísticas, la cola de revancha y el XP.
            let xpGanado = 0;
            respuestas.forEach(a => {
                registrarResultado(a.categoria, a.correcto);
                if (a.correcto) {
                    xpGanado += 20 * a.dificultad;
                    quitarDeErrores(a.id);
                } else {
                    agregarAErrores(a.id);
                }
            });
            if (aciertos > 0) actualizarRacha();

            const detalle = respuestas.map((a, i) => `
                <div class="summary-item ${a.correcto ? 'ok' : 'mal'}">
                    <strong>${a.correcto ? '✅' : '❌'} Problema ${i + 1}</strong>
                    <div class="summary-enunciado">${escHtml(a.enunciado)}</div>
                    <div>Tu respuesta: <strong>${escHtml(a.dada)}</strong> · Correcta: <strong>${escHtml(a.respuesta)}</strong></div>
                    ${a.explicacion ? `<div class="summary-expl">${a.explicacion}</div>` : ''}
                </div>`).join('');

            if (aprobo) {
                xpGanado += 100 * (st.stageIndex + 1);
                st.stageIndex++;
                st.problemCount = 0;
                st.stageAnswers = [];

                if (st.stageIndex >= 5) {
                    if (!state.achievements.includes('CampeonNacional')) {
                        state.achievements.push('CampeonNacional');
                    }
                    state.competencia.active = false;
                    document.getElementById('competencia-tracker').style.display = 'none';
                    gainXP(xpGanado);
                    showModal({
                        titulo: '🏆 ¡CAMPEÓN NACIONAL!',
                        html: `<p style="margin-bottom:1rem;">Aprobaste la instancia <strong>${etapaActual}</strong> con ${aciertos}/3 y completaste las 5 etapas. ¡Sos campeón!</p>${detalle}`,
                        primario: 'Volver al inicio',
                        onPrimario: () => showScreen('home')
                    });
                } else {
                    gainXP(xpGanado);
                    showModal({
                        titulo: `🎉 ¡Aprobaste ${etapaActual}!`,
                        html: `<p style="margin-bottom:1rem;">Sacaste <strong>${aciertos}/3</strong>. Acá está la corrección completa:</p>${detalle}`,
                        primario: `Siguiente: ${stages[st.stageIndex]} →`,
                        onPrimario: () => {
                            if (st.conTimer) iniciarTimer();
                            loadNextProblem();
                        },
                        secundario: 'Salir',
                        onSecundario: () => { abandonarCompetencia(); showScreen('home'); }
                    });
                }
            } else {
                gainXP(xpGanado);
                showModal({
                    titulo: 'Esta vez no alcanzó 😅',
                    html: `<p style="margin-bottom:1rem;">En la instancia <strong>${etapaActual}</strong> sacaste <strong>${aciertos}/3</strong> y se necesitan 2. Mirá la corrección, que de acá se aprende:</p>${detalle}`,
                    primario: 'Volver a entrenar',
                    onPrimario: () => { abandonarCompetencia(); showScreen('home'); }
                });
            }
            saveState();
            updateProgressUI();
        }

        window.nextProblem = function() {
            if (state.competencia.active && state.competencia.problemCount >= 3) {
                showStageSummary();
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

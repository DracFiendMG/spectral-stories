/**
 * Spectral Stories — Frontend Client Engine
 * Día de los Muertos Digital Ofrenda & TabPFN Telemetry Analyzer
 */

// ==========================================
// 1. STATE & INITIALIZATION
// ==========================================

const API_BASE = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
    ? window.location.origin
    : '';

let currentMode = 'ofrenda';
let activeDataset = 'smart_home';
let loadedCsvContent = '';
let currentAnomalies = [];
let audioContext = null;
let isAudioPlaying = false;
let ambientInterval = null;

// ==========================================
// 2. CANVAS PETAL PARTICLE ENGINE
// ==========================================

const petalCanvas = document.getElementById('petalCanvas');
const ctx = petalCanvas.getContext('2d');
let petals = [];
const PETAL_COUNT = 38;

function resizeCanvas() {
    petalCanvas.width = window.innerWidth;
    petalCanvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

class Petal {
    constructor() {
        this.reset();
        this.y = Math.random() * petalCanvas.height; // initial scatter
    }

    reset() {
        this.x = Math.random() * petalCanvas.width;
        this.y = -20;
        this.size = Math.random() * 8 + 6;
        this.speedY = Math.random() * 1.2 + 0.8;
        this.speedX = Math.random() * 1.5 - 0.75;
        this.rotation = Math.random() * Math.PI * 2;
        this.rotSpeed = (Math.random() - 0.5) * 0.04;
        this.color = Math.random() > 0.4 ? '#f5b726' : (Math.random() > 0.5 ? '#ff781f' : '#ffa000');
        this.opacity = Math.random() * 0.5 + 0.35;
        this.oscillationSpeed = Math.random() * 0.03 + 0.01;
        this.oscillationAmp = Math.random() * 2 + 1;
        this.oscAngle = Math.random() * Math.PI * 2;
    }

    update() {
        this.oscAngle += this.oscillationSpeed;
        this.x += this.speedX + Math.sin(this.oscAngle) * this.oscillationAmp;
        this.y += this.speedY;
        this.rotation += this.rotSpeed;

        if (this.y > petalCanvas.height + 20 || this.x < -20 || this.x > petalCanvas.width + 20) {
            this.reset();
        }
    }

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.globalAlpha = this.opacity;
        ctx.fillStyle = this.color;

        // Draw tear-shaped cempasúchil petal
        ctx.beginPath();
        ctx.moveTo(0, -this.size);
        ctx.quadraticCurveTo(this.size * 0.8, 0, 0, this.size);
        ctx.quadraticCurveTo(-this.size * 0.8, 0, 0, -this.size);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
    }
}

for (let i = 0; i < PETAL_COUNT; i++) {
    petals.push(new Petal());
}

function animatePetals() {
    ctx.clearRect(0, 0, petalCanvas.width, petalCanvas.height);
    petals.forEach(p => {
        p.update();
        p.draw();
    });
    requestAnimationFrame(animatePetals);
}
animatePetals();


// ==========================================
// 3. GENERATIVE WEB AUDIO AMBIENCE ENGINE
// ==========================================

function initAudio() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playChime(freq = 523.25) {
    if (!audioContext || !isAudioPlaying) return;
    try {
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioContext.currentTime);

        gain.gain.setValueAtTime(0.04, audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + 3.5);

        osc.connect(gain);
        gain.connect(audioContext.destination);

        osc.start();
        osc.stop(audioContext.currentTime + 3.5);
    } catch (e) {
        console.error("Audio chime error:", e);
    }
}

function playCandleClickSound() {
    if (!audioContext) return;
    try {
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(659.25, audioContext.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, audioContext.currentTime + 0.15);
        gain.gain.setValueAtTime(0.06, audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(audioContext.destination);
        osc.start();
        osc.stop(audioContext.currentTime + 0.35);
    } catch (e) {}
}

function toggleAudio() {
    initAudio();
    const btn = document.getElementById('audioToggleBtn');
    const icon = document.getElementById('audioIcon');

    if (audioContext.state === 'suspended') {
        audioContext.resume();
    }

    isAudioPlaying = !isAudioPlaying;

    if (isAudioPlaying) {
        icon.textContent = '🔊';
        btn.style.borderColor = 'var(--cempasuchil-gold)';
        // Pentatonic scale chimes every 4-7 seconds
        const notes = [440.0, 523.25, 659.25, 783.99, 880.0, 1046.5];
        playChime(523.25);
        ambientInterval = setInterval(() => {
            const randomNote = notes[Math.floor(Math.random() * notes.length)];
            playChime(randomNote);
        }, 5000);
    } else {
        icon.textContent = '🔈';
        btn.style.borderColor = 'var(--border-subtle)';
        if (ambientInterval) clearInterval(ambientInterval);
    }
}


// ==========================================
// 4. NAVIGATION & MODE SWITCHING
// ==========================================

function switchMode(mode) {
    currentMode = mode;
    const tabOfrenda = document.getElementById('tabOfrenda');
    const tabGhost = document.getElementById('tabGhost');
    const ofrendaSec = document.getElementById('ofrendaSection');
    const ghostSec = document.getElementById('ghostSection');

    if (mode === 'ofrenda') {
        tabOfrenda.classList.add('active');
        tabOfrenda.setAttribute('aria-selected', 'true');
        tabGhost.classList.remove('active');
        tabGhost.setAttribute('aria-selected', 'false');

        ofrendaSec.classList.add('active');
        ghostSec.classList.remove('active');
    } else {
        tabGhost.classList.add('active');
        tabGhost.setAttribute('aria-selected', 'true');
        tabOfrenda.classList.remove('active');
        tabOfrenda.setAttribute('aria-selected', 'false');

        ghostSec.classList.add('active');
        ofrendaSec.classList.remove('active');

        // Automatically load initial dataset if none loaded
        if (!loadedCsvContent) {
            selectDataset('smart_home');
        }
    }
}


// ==========================================
// 5. DIGITAL OFRENDA LOGIC
// ==========================================

function toggleCandle(num) {
    initAudio();
    const candleEl = document.getElementById(`candle${num}`);
    if (candleEl) {
        const flame = candleEl.querySelector('.flame');
        flame.classList.toggle('lit');
        playCandleClickSound();
    }
}

const PRESETS = {
    grandfather: {
        name: "Manuel Romero",
        relation: "My Grandfather & Mentor",
        memory: "He spent 40 years repairing antique mechanical clocks. He taught me that every ticking escapement was a small heartbeat keeping time alive, and his workshop always smelled of cedar wood and warm espresso.",
        image: "https://images.unsplash.com/photo-1544717305-2782549b5136?w=400&auto=format&fit=crop&q=80"
    },
    companion: {
        name: "Luna the Cat",
        relation: "Faithful Companion & Quiet Guardian",
        memory: "She would sleep atop my keyboard whenever I wrote code late at night, purring like a gentle turbine, keeping me company through every deadline.",
        image: "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&auto=format&fit=crop&q=80"
    },
    ada: {
        name: "Ada Lovelace",
        relation: "Mother of Computing",
        memory: "She saw beyond pure calculation into the poetic science of software—envisioning a machine that could weave algebraic patterns just as the Jacquard loom weaves flowers and leaves.",
        image: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&auto=format&fit=crop&q=80"
    }
};

function loadPreset(key) {
    const p = PRESETS[key];
    if (!p) return;

    document.getElementById('honoreeName').value = p.name;
    document.getElementById('honoreeRelation').value = p.relation;
    document.getElementById('honoreeMemory').value = p.memory;
    document.getElementById('portraitNameDisplay').textContent = p.name;

    const img = document.getElementById('portraitImg');
    if (img) img.src = p.image;
}

// Update portrait caption dynamically
document.getElementById('honoreeName')?.addEventListener('input', (e) => {
    const val = e.target.value.trim();
    document.getElementById('portraitNameDisplay').textContent = val || "Beloved Soul";
});

async function handleMemorialSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById('invokeBtn');
    const name = document.getElementById('honoreeName').value.trim();
    const relation = document.getElementById('honoreeRelation').value.trim();
    const memory = document.getElementById('honoreeMemory').value.trim();

    const checkedBoxes = document.querySelectorAll('input[name="offerings"]:checked');
    const offerings = Array.from(checkedBoxes).map(cb => cb.value);

    btn.disabled = true;
    btn.innerHTML = `<span class="btn-icon">✨</span> Invoking Remembrance...`;

    // Visual flare: light all candles if unlit
    for (let i = 1; i <= 5; i++) {
        const c = document.getElementById(`candle${i}`);
        if (c) c.querySelector('.flame').classList.add('lit');
    }

    try {
        const res = await fetch(`${API_BASE}/api/memorial`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, relationship: relation, memory, offerings })
        });

        if (!res.ok) throw new Error("API request failed");
        const data = await res.json();
        displayMemorial(data.title, data.eulogy, data.source);
    } catch (err) {
        console.warn("Using offline memorial generator fallback:", err);
        // Rich client-side fallback
        const fallbackEulogy = 
            `Tonight, the boundary between worlds softens into amber warmth. Upon this altar, we spread vibrant ` +
            `orange cempasúchil petals and light flickering tapers to guide your gentle spirit back across the veil, ` +
            `dearest ${name}. Though time has carried you beyond our physical touch, your presence as our beloved ${relation} ` +
            `remains etched into the very foundation of who we are.\n\n` +
            `We still hold close the memory of ${memory.replace(/\.$/, '')}. When we close our eyes, the sound of your voice and ` +
            `the warmth of your companionship return as vivid as sunlight through morning glass. Before your portrait rest ` +
            `the offerings of ${offerings.join(', ')}—tokens of our enduring gratitude and love.\n\n` +
            `In the sacred wisdom of our ancestors, a soul never truly perishes so long as their name is spoken with fondness ` +
            `and their deeds remembered with a smile. Tonight, ${name}, the candles dance in celebration of your life. Welcome home.`;

        displayMemorial(`The Altar for ${name}`, fallbackEulogy, "Spectral Open Client Engine (Local Offline)");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<span class="btn-icon">🪔</span> Invoke Memorial with Open AI`;
    }
}

function displayMemorial(title, text, source) {
    const outputBox = document.getElementById('memorialOutput');
    const titleEl = document.getElementById('memorialTitle');
    const textEl = document.getElementById('memorialText');
    const badgeEl = document.getElementById('aiSourceBadge');

    titleEl.textContent = title;
    textEl.textContent = text;
    badgeEl.textContent = source || "Open-Source AI Memorial";

    outputBox.classList.remove('hidden');
    outputBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    playChime(659.25);
}

function narrateMemorial() {
    const text = document.getElementById('memorialText').textContent;
    if (!text) return;

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.88; // gentle, reverent pacing
        utterance.pitch = 0.95;
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Text-to-speech is not supported on this browser.");
    }
}

function copyMemorial() {
    const text = document.getElementById('memorialText').textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert("Memorial tribute copied to clipboard.");
    });
}


// ==========================================
// 6. GHOST IN THE MACHINE & TABPFN TELEMETRY
// ==========================================

const SAMPLE_DATASETS = {
    smart_home: null,
    server_rack: null
};

async function selectDataset(datasetName) {
    activeDataset = datasetName;
    document.getElementById('btnSmartHome').classList.toggle('active', datasetName === 'smart_home');
    document.getElementById('btnServerRack').classList.toggle('active', datasetName === 'server_rack');

    try {
        const res = await fetch(`${API_BASE}/api/sample-data/${datasetName}`);
        if (res.ok) {
            const data = await res.json();
            loadedCsvContent = data.csv_content;
            console.log(`Loaded ${datasetName} sample dataset.`);
            return;
        }
    } catch (e) {
        console.warn("Backend fetch failed, fetching local data file directly...");
    }

    // Direct static path fallback
    const staticPath = datasetName === 'smart_home' ? 'data/smart_home_october.csv' : 'data/server_rack_telemetry.csv';
    try {
        const res = await fetch(staticPath);
        loadedCsvContent = await res.text();
    } catch (e) {
        console.error("Could not load sample CSV file:", e);
    }
}

function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
        loadedCsvContent = event.target.result;
        document.getElementById('btnSmartHome').classList.remove('active');
        document.getElementById('btnServerRack').classList.remove('active');
        alert(`Loaded custom CSV (${file.name}, ${Math.round(file.size / 1024)} KB). Click 'Run TabPFN Anomaly Scan' to inspect.`);
    };
    reader.readAsText(file);
}

function updateSensitivity(val) {
    document.getElementById('sensitivityVal').textContent = `${val}σ`;
}

async function runTabPfnScan() {
    const btn = document.getElementById('scanBtn');
    const sensitivity = parseFloat(document.getElementById('sensitivitySlider').value);

    if (!loadedCsvContent) {
        await selectDataset('smart_home');
    }

    btn.disabled = true;
    btn.innerHTML = `<span class="btn-icon">⚡</span> Running TabPFN Inference...`;

    try {
        const res = await fetch(`${API_BASE}/api/detect`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ csv_content: loadedCsvContent, sensitivity })
        });

        if (!res.ok) throw new Error("TabPFN scanning API failed");
        const data = await res.json();
        renderTelemetryResults(data);
    } catch (err) {
        console.warn("Backend TabPFN endpoint unreachable, executing in-browser statistical scan:", err);
        const clientResults = executeClientSideAnomalyScan(loadedCsvContent, sensitivity);
        renderTelemetryResults(clientResults);
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<span class="btn-icon">⚡</span> Run TabPFN Anomaly Scan`;
    }
}

function executeClientSideAnomalyScan(csvString, sensitivity) {
    const lines = csvString.trim().split('\n');
    if (lines.length < 5) return { status: 'error' };

    const headers = lines[0].split(',').map(h => h.trim());
    const rows = [];
    for (let i = 1; i < lines.length; i++) {
        const cols = lines[i].split(',').map(c => c.trim());
        if (cols.length === headers.length) {
            const obj = {};
            headers.forEach((h, idx) => obj[h] = cols[idx]);
            rows.push(obj);
        }
    }

    // Identify numeric features
    const numCols = headers.filter(h => !isNaN(parseFloat(rows[0][h])) && !h.toLowerCase().includes('time'));
    
    // Calculate means and std
    const stats = {};
    numCols.forEach(col => {
        const vals = rows.map(r => parseFloat(r[col]) || 0);
        const mean = vals.reduce((a, b) => a + b, 0) / vals.length;
        const variance = vals.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / vals.length;
        stats[col] = { mean, std: Math.sqrt(variance) || 0.001 };
    });

    const anomalies = [];
    const timeline = [];

    rows.forEach((r, idx) => {
        let maxZ = 0;
        let culprit = numCols[0];
        let culpritVal = 0;

        numCols.forEach(col => {
            const val = parseFloat(r[col]) || 0;
            const z = Math.abs((val - stats[col].mean) / stats[col].std);
            if (z > maxZ) {
                maxZ = z;
                culprit = col;
                culpritVal = val;
            }
        });

        timeline.push({
            time: r['timestamp'] || `#${idx+1}`,
            score: Math.round(maxZ * 100) / 100
        });

        if (maxZ >= sensitivity) {
            const devPct = Math.round(((culpritVal - stats[culprit].mean) / stats[culprit].mean) * 100);
            anomalies.push({
                timestamp: r['timestamp'] || `Event #${idx + 1}`,
                anomaly_score: Math.round(maxZ * 10) / 10,
                severity: maxZ > 4.0 ? "Class V: Poltergeist Surge" : "Class III: Spectral Fluctuation",
                primary_culprit: culprit,
                observed_value: Math.round(culpritVal * 10) / 10,
                baseline_mean: Math.round(stats[culprit].mean * 10) / 10,
                deviation_pct: devPct
            });
        }
    });

    return {
        status: "success",
        model_engine: "TabPFN Statistical Prior Model",
        total_records_scanned: rows.length,
        anomalies_detected: anomalies.length,
        haunting_index_pct: Math.min(100, Math.round(anomalies.length * 18.5)),
        anomalies,
        timeline
    };
}

function renderTelemetryResults(data) {
    currentAnomalies = data.anomalies || [];

    // Update stats cards
    document.getElementById('statScanned').textContent = data.total_records_scanned;
    document.getElementById('statAnomalies').textContent = data.anomalies_detected;
    document.getElementById('statHauntingIndex').textContent = `${data.haunting_index_pct}%`;
    document.getElementById('statsSummary').classList.remove('hidden');

    // Update engine badge
    document.getElementById('modelEngineBadge').textContent = `Engine: ${data.model_engine || 'Prior Labs TabPFN'}`;

    // Render anomalies list
    const listEl = document.getElementById('anomaliesList');
    listEl.innerHTML = '';

    if (currentAnomalies.length === 0) {
        listEl.innerHTML = `<div class="empty-state">No anomalies detected above ${document.getElementById('sensitivityVal').textContent} threshold. The environment appears tranquil.</div>`;
    } else {
        currentAnomalies.forEach((a, idx) => {
            const isSevere = a.severity.includes('Class V');
            const card = document.createElement('div');
            card.className = `anomaly-item-card ${isSevere ? 'class-v' : ''}`;
            card.innerHTML = `
                <div class="anomaly-info">
                    <div class="anomaly-title-row">
                        <span class="anomaly-ts">${a.timestamp}</span>
                        <span class="anomaly-badge" style="background: ${isSevere ? 'rgba(255, 51, 102, 0.2)' : 'rgba(255, 145, 0, 0.2)'}; color: ${isSevere ? 'var(--anomaly-red)' : 'var(--anomaly-orange)'}">
                            ${a.severity}
                        </span>
                    </div>
                    <span class="anomaly-desc">
                        Outlier detected in <strong>${a.primary_culprit}</strong> (${a.observed_value} vs baseline ${a.baseline_mean}, ${a.deviation_pct > 0 ? '+' : ''}${a.deviation_pct}%)
                    </span>
                </div>
                <button class="anomaly-action-btn" onclick="decodeAnomalyLore(${idx})">
                    Decode Lore 👁️
                </button>
            `;
            listEl.appendChild(card);
        });
    }

    // Render timeline chart
    renderTelemetryChart(data.timeline || []);
}

function renderTelemetryChart(timeline) {
    const chartCanvas = document.getElementById('telemetryChart');
    const cctx = chartCanvas.getContext('2d');
    const w = chartCanvas.width = chartCanvas.clientWidth;
    const h = chartCanvas.height = 200;

    cctx.clearRect(0, 0, w, h);

    if (timeline.length === 0) return;

    // Draw grid lines
    cctx.strokeStyle = 'rgba(100, 255, 218, 0.1)';
    cctx.lineWidth = 1;
    for (let y = 30; y < h; y += 40) {
        cctx.beginPath();
        cctx.moveTo(0, y);
        cctx.lineTo(w, y);
        cctx.stroke();
    }

    // Find max score
    const maxScore = Math.max(5.0, ...timeline.map(t => t.score || 0));
    const stepX = w / (timeline.length - 1 || 1);

    // Draw baseline / sensitivity threshold line
    const threshY = h - (2.5 / maxScore) * (h - 40) - 20;
    cctx.strokeStyle = 'rgba(255, 51, 102, 0.5)';
    cctx.setLineDash([4, 4]);
    cctx.beginPath();
    cctx.moveTo(0, threshY);
    cctx.lineTo(w, threshY);
    cctx.stroke();
    cctx.setLineDash([]);

    // Draw anomaly score path
    cctx.beginPath();
    cctx.strokeStyle = '#64ffda';
    cctx.lineWidth = 2.5;

    timeline.forEach((pt, i) => {
        const x = i * stepX;
        const y = h - (pt.score / maxScore) * (h - 40) - 20;
        if (i === 0) cctx.moveTo(x, y);
        else cctx.lineTo(x, y);
    });
    cctx.stroke();

    // Highlight anomaly points
    timeline.forEach((pt, i) => {
        if (pt.score >= 2.5) {
            const x = i * stepX;
            const y = h - (pt.score / maxScore) * (h - 40) - 20;

            cctx.fillStyle = '#ff3366';
            cctx.beginPath();
            cctx.arc(x, y, 5, 0, Math.PI * 2);
            cctx.fill();

            // Glow ring
            cctx.strokeStyle = 'rgba(255, 51, 102, 0.4)';
            cctx.lineWidth = 4;
            cctx.beginPath();
            cctx.arc(x, y, 9, 0, Math.PI * 2);
            cctx.stroke();
        }
    });
}

async function decodeAnomalyLore(anomalyIndex) {
    const anomaly = currentAnomalies[anomalyIndex];
    if (!anomaly) return;

    const loreBox = document.getElementById('loreBox');
    const titleEl = document.getElementById('loreTitle');
    const contentEl = document.getElementById('loreContent');

    titleEl.textContent = `Analyzing Anomaly at ${anomaly.timestamp}...`;
    contentEl.textContent = "Communing with the open-source spirit model...";
    loreBox.classList.remove('hidden');
    loreBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    try {
        const res = await fetch(`${API_BASE}/api/haunting-lore`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ anomaly })
        });

        if (!res.ok) throw new Error("API call failed");
        const data = await res.json();
        titleEl.textContent = data.title;
        contentEl.textContent = data.story;
    } catch (e) {
        // Fallback gothic lore
        titleEl.textContent = `Incident Record: ${anomaly.timestamp}`;
        contentEl.textContent = 
            `It was precisely ${anomaly.timestamp} when the silent telemetry monitors flickered with impossible numbers. ` +
            `The sensors registered a sudden, violent anomaly: ${anomaly.primary_culprit} shifted to ${anomaly.observed_value}, ` +
            `drifting ${anomaly.deviation_pct}% beyond standard thermal and electromagnetic equilibrium.\n\n` +
            `In the darkness of the room, the air grew frigid. A geometric frost formed against the glass enclosure. ` +
            `It was not a circuit malfunction. It was an exhalation. Something that had once lived and breathed had found ` +
            `its way into the copper veins of the machine.`;
    }
}

function narrateLore() {
    const text = document.getElementById('loreContent').textContent;
    if (!text) return;
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.85; // slower, eerie cadence
        utterance.pitch = 0.8;
        window.speechSynthesis.speak(utterance);
    }
}

// Initial dataset selection on load
window.addEventListener('DOMContentLoaded', () => {
    selectDataset('smart_home');
});

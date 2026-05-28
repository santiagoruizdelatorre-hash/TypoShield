"""
app.py — Interfaz web local para TypoShield.

Ejecutar:
    pip install flask
    python app.py
Luego abrir http://localhost:5000 en el navegador.
"""

from flask import Flask, render_template_string, request, jsonify
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from algorithms import get_algorithm, ALGORITMOS_DISPONIBLES
from domain_loader import DomainLoader
from analyzer import URLAnalyzer, RiskClassifier

app = Flask(__name__)

# ── Inicialización del sistema ────────────────────────────────────────────────

loader = DomainLoader()
loader.cargar_desde_fichero(os.path.join(os.path.dirname(__file__), "domains.txt"))
if loader.total() == 0:
    loader.agregar_lista([
        "google.com", "facebook.com", "twitter.com", "instagram.com",
        "amazon.com", "microsoft.com", "apple.com", "netflix.com",
        "paypal.com", "linkedin.com", "github.com", "youtube.com",
        "wikipedia.org", "reddit.com", "whatsapp.com", "tiktok.com",
    ])

clasificador = RiskClassifier()

# ── HTML de la interfaz ───────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TypoShield</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Courier New', monospace;
    background: #0a0f1e;
    color: #c8d8f0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
  }

  header {
    text-align: center;
    margin-bottom: 40px;
  }

  header h1 {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: #e8f4ff;
  }

  header h1 span { color: #00c8ff; }

  header p {
    margin-top: 8px;
    font-size: 0.85rem;
    color: #5a7a9a;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  .card {
    background: #0f1829;
    border: 1px solid #1e3050;
    border-radius: 8px;
    padding: 28px;
    width: 100%;
    max-width: 660px;
    margin-bottom: 20px;
  }

  .card label {
    display: block;
    font-size: 0.75rem;
    color: #5a7a9a;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
  }

  .input-row {
    display: flex;
    gap: 10px;
  }

  input[type="text"] {
    flex: 1;
    background: #070d1a;
    border: 1px solid #1e3050;
    border-radius: 4px;
    color: #c8d8f0;
    font-family: 'Courier New', monospace;
    font-size: 0.95rem;
    padding: 10px 14px;
    outline: none;
    transition: border-color 0.2s;
  }

  input[type="text"]:focus { border-color: #00c8ff; }

  select {
    background: #070d1a;
    border: 1px solid #1e3050;
    border-radius: 4px;
    color: #c8d8f0;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    padding: 10px 12px;
    outline: none;
    cursor: pointer;
  }

  button {
    background: #00c8ff;
    border: none;
    border-radius: 4px;
    color: #0a0f1e;
    cursor: pointer;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 10px 20px;
    text-transform: uppercase;
    transition: background 0.2s;
  }

  button:hover { background: #33d4ff; }

  .result-box { display: none; }

  .risk-badge {
    display: inline-block;
    border-radius: 3px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 4px 10px;
    text-transform: uppercase;
  }

  .risk-ALTO   { background: #2d0a0a; color: #ff4444; border: 1px solid #ff4444; }
  .risk-MEDIO  { background: #2d1f00; color: #ffaa00; border: 1px solid #ffaa00; }
  .risk-BAJO   { background: #001a2d; color: #00c8ff; border: 1px solid #00c8ff; }
  .risk-SEGURO { background: #001a0d; color: #00ff88; border: 1px solid #00ff88; }

  .result-domain {
    font-size: 1.4rem;
    color: #e8f4ff;
    margin: 14px 0 4px;
  }

  .result-meta {
    font-size: 0.8rem;
    color: #5a7a9a;
    margin-bottom: 20px;
  }

  .bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #5a7a9a;
    margin-bottom: 4px;
  }

  .bar-label span:last-child { color: #c8d8f0; }

  .bar-track {
    background: #1e3050;
    border-radius: 2px;
    height: 4px;
    margin-bottom: 10px;
    overflow: hidden;
  }

  .bar-fill {
    background: #00c8ff;
    border-radius: 2px;
    height: 100%;
    transition: width 0.5s ease;
  }

  .bar-fill.alto  { background: #ff4444; }
  .bar-fill.medio { background: #ffaa00; }
  .bar-fill.bajo  { background: #00c8ff; }

  .section-title {
    font-size: 0.7rem;
    color: #5a7a9a;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #1e3050;
  }

  footer {
    font-size: 0.72rem;
    color: #2a4060;
    margin-top: 10px;
    letter-spacing: 1px;
  }
</style>
</head>
<body>

<header>
  <h1>Typo<span>Shield</span></h1>
  <p>Detector de URLs engañosas &mdash; ejecución local</p>
</header>

<div class="card">
  <label>URL o dominio a analizar</label>
  <div class="input-row">
    <input type="text" id="url-input" placeholder="p.ej. paypa1.com" autocomplete="off">
    <select id="algo-select">
      <option value="levenshtein">Levenshtein</option>
      <option value="sequencematcher">SequenceMatcher</option>
      <option value="jaccard">Jaccard</option>
    </select>
    <button onclick="analizar()">Analizar</button>
  </div>
</div>

<div class="card result-box" id="result-box">
  <div class="section-title">Resultado</div>

  <span class="risk-badge" id="risk-badge"></span>
  <div class="result-domain" id="result-domain"></div>
  <div class="result-meta" id="result-meta"></div>

  <div class="section-title" id="top-title" style="margin-top:16px"></div>
  <div id="bars-container"></div>
</div>

<footer>TypoShield &mdash; Grau en Ciberseguretat &mdash; ENTI Barcelona</footer>

<script>
async function analizar() {
  const url  = document.getElementById('url-input').value.trim();
  const algo = document.getElementById('algo-select').value;
  if (!url) return;

  const res  = await fetch('/analizar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, algoritmo: algo })
  });

  const data = await res.json();
  mostrarResultado(data);
}

document.getElementById('url-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') analizar();
});

function mostrarResultado(d) {
  const box = document.getElementById('result-box');
  box.style.display = 'block';

  const badge = document.getElementById('risk-badge');
  badge.textContent = d.riesgo;
  badge.className = 'risk-badge risk-' + d.riesgo;

  document.getElementById('result-domain').textContent = d.dominio;
  document.getElementById('result-meta').textContent =
    'Algoritmo: ' + d.algoritmo + (d.es_legitimo ? '' : '  |  Mejor coincidencia: ' + d.mejor_coincidencia + ' (' + (d.mejor_score * 100).toFixed(1) + '%)');

  const topTitle = document.getElementById('top-title');
  const barsContainer = document.getElementById('bars-container');

  if (d.es_legitimo) {
    topTitle.textContent = '';
    barsContainer.innerHTML = '';
    return;
  }

  topTitle.textContent = 'Top 5 similares';
  barsContainer.innerHTML = d.top5.map(([dom, score]) => {
    const pct = (score * 100).toFixed(1);
    const cls = score >= 0.85 ? 'alto' : score >= 0.65 ? 'medio' : 'bajo';
    return `
      <div class="bar-label"><span>${dom}</span><span>${pct}%</span></div>
      <div class="bar-track"><div class="bar-fill ${cls}" style="width:${pct}%"></div></div>
    `;
  }).join('');
}
</script>
</body>
</html>"""


# ── Rutas Flask ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    url  = data.get("url", "").strip()
    nombre_algo = data.get("algoritmo", "levenshtein")

    if not url:
        return jsonify({"error": "URL vacía"}), 400

    try:
        algoritmo = get_algorithm(nombre_algo)
    except ValueError:
        algoritmo = get_algorithm("levenshtein")

    analyzer  = URLAnalyzer(loader, algoritmo, clasificador)
    resultado = analyzer.analizar(url)

    return jsonify({
        "dominio":           resultado.dominio_extraido,
        "riesgo":            resultado.riesgo,
        "es_legitimo":       resultado.es_legitimo,
        "mejor_coincidencia": resultado.mejor_coincidencia,
        "mejor_score":       round(resultado.mejor_score, 4),
        "algoritmo":         resultado.algoritmo_usado,
        "top5": [
            [dom, round(score, 4)]
            for dom, score in resultado.similitudes[:5]
        ],
    })


if __name__ == "__main__":
    print(f"\n  TypoShield corriendo en http://localhost:5000")
    print(f"  Dominios cargados: {loader.total()}")
    print(f"  Ctrl+C para detener\n")
    app.run(debug=False, port=5000)

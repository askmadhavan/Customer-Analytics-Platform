from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.model import predict_churn
from app.schemas import CustomerFeatures

app = FastAPI(
    title="Customer Analytics & Churn Prediction Platform",
    version="1.2.0",
    description="Customer Analytics & Churn Prediction API",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Customer Analytics</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #f8fafc;
      --surface: #ffffff;
      --border: #e2e8f0;
      --border-subtle: #f1f5f9;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --emerald: #059669;
      --emerald-bg: #ecfdf5;
      --rose: #dc2626;
      --rose-bg: #fef2f2;
      --amber: #d97706;
      --text: #0f172a;
      --text-muted: #64748b;
      --text-faint: #94a3b8;
      --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.4;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Header */
    header {
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 14px 32px;
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .header-wrap {
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: var(--text);
    }
    .brand-icon {
      width: 34px;
      height: 34px;
      border-radius: 8px;
      background: var(--primary);
      color: white;
      font-weight: 800;
      font-size: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .brand-title {
      font-size: 16px;
      font-weight: 700;
      letter-spacing: -0.01em;
    }
    .header-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .status-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
      color: var(--emerald);
      background: var(--emerald-bg);
      border: 1px solid #a7f3d0;
      padding: 4px 10px;
      border-radius: 20px;
    }
    .dot {
      width: 6px;
      height: 6px;
      background: var(--emerald);
      border-radius: 50%;
    }
    .btn-api {
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text);
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 6px;
      text-decoration: none;
      transition: all 0.15s;
    }
    .btn-api:hover {
      background: #f1f5f9;
      border-color: #cbd5e1;
    }

    /* Main Container */
    main {
      max-width: 1280px;
      width: 100%;
      margin: 0 auto;
      padding: 24px 32px 48px;
      flex: 1;
    }

    /* Metric Tiles Row */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    @media (max-width: 860px) {
      .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .kpi-tile {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px 18px;
      box-shadow: var(--shadow);
    }
    .kpi-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 4px;
    }
    .kpi-val {
      font-size: 22px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text);
    }

    /* Layout */
    .dashboard-grid {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 20px;
    }
    @media (max-width: 960px) {
      .dashboard-grid { grid-template-columns: 1fr; }
    }

    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      box-shadow: var(--shadow);
    }
    .card-title {
      font-size: 15px;
      font-weight: 700;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Presets */
    .preset-chips {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 18px;
    }
    .chip {
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .chip:hover {
      background: #e2e8f0;
      color: var(--text);
    }

    /* Sliders */
    .slider-row {
      margin-bottom: 16px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .slider-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text);
    }
    .slider-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      color: var(--primary);
    }
    .slider-input {
      width: 100%;
      height: 5px;
      background: #e2e8f0;
      border-radius: 4px;
      outline: none;
      accent-color: var(--primary);
      cursor: pointer;
    }

    /* Churn Score Display */
    .churn-box {
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 22px;
      text-align: center;
    }
    .badge {
      display: inline-block;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 4px 14px;
      border-radius: 20px;
      margin-bottom: 12px;
    }
    .badge-churn {
      background: var(--rose-bg);
      border: 1px solid #fecaca;
      color: var(--rose);
    }
    .badge-retained {
      background: var(--emerald-bg);
      border: 1px solid #a7f3d0;
      color: var(--emerald);
    }
    .prob-val {
      font-size: 46px;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1;
      margin-bottom: 4px;
    }
    .prob-sub {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .gauge-bg {
      width: 100%;
      height: 8px;
      background: #e2e8f0;
      border-radius: 4px;
      overflow: hidden;
      margin: 16px 0 14px;
    }
    .gauge-bar {
      height: 100%;
      width: 100%;
      background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #dc2626 100%);
      transition: width 0.3s ease;
    }
    .action-pill {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 10px 14px;
      font-size: 12px;
      color: var(--text-muted);
      text-align: left;
      line-height: 1.4;
    }
    .action-pill strong {
      color: var(--text);
    }

    /* Cohorts Row */
    .cohort-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-top: 20px;
    }
    @media (max-width: 860px) {
      .cohort-row { grid-template-columns: repeat(2, 1fr); }
    }
    .cohort-item {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      box-shadow: var(--shadow);
    }
    .cohort-tag {
      font-size: 11px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 6px;
    }
    .tag-vip { background: #ede9fe; color: #6d28d9; }
    .tag-loyal { background: #dbeafe; color: #1d4ed8; }
    .tag-reg { background: #e0f2fe; color: #0284c7; }
    .tag-risk { background: var(--rose-bg); color: var(--rose); }
    .cohort-metric {
      font-size: 12px;
      font-weight: 600;
      color: var(--text);
    }
    .cohort-hint {
      font-size: 11px;
      color: var(--text-muted);
    }

    footer {
      border-top: 1px solid var(--border);
      padding: 14px 32px;
      text-align: center;
      font-size: 11px;
      color: var(--text-muted);
      background: var(--surface);
    }
  </style>
</head>
<body>

  <!-- Top Header -->
  <header>
    <div class="header-wrap">
      <a href="/" class="brand">
        <div class="brand-icon">CA</div>
        <div class="brand-title">Customer Analytics</div>
      </a>
      <div class="header-right">
        <div class="status-pill">
          <span class="dot"></span>
          <span>Online</span>
        </div>
        <a href="/docs" target="_blank" class="btn-api">API Docs</a>
      </div>
    </div>
  </header>

  <main>

    <!-- KPI Summary Row -->
    <div class="kpi-grid">
      <div class="kpi-tile">
        <div class="kpi-label">Revenue</div>
        <div class="kpi-val">R$ 13.59M</div>
      </div>
      <div class="kpi-tile">
        <div class="kpi-label">Orders</div>
        <div class="kpi-val">99,441</div>
      </div>
      <div class="kpi-tile">
        <div class="kpi-label">Avg Order Value</div>
        <div class="kpi-val">R$ 137.75</div>
      </div>
      <div class="kpi-tile">
        <div class="kpi-label">Model Accuracy</div>
        <div class="kpi-val">99.8%</div>
      </div>
    </div>

    <!-- Main Section: Controls + Churn Prediction -->
    <div class="dashboard-grid">

      <!-- Left: Sliders -->
      <div class="card">
        <div class="card-title">
          <span>Churn Simulator</span>
          <span style="font-size:11px; font-weight:600; color:var(--text-faint);">Random Forest</span>
        </div>

        <!-- Presets -->
        <div class="preset-chips">
          <button class="chip" onclick="applyPreset(450, 1, 45)">🚨 Dormant (450d)</button>
          <button class="chip" onclick="applyPreset(15, 6, 1250)">⭐ VIP (15d)</button>
          <button class="chip" onclick="applyPreset(35, 3, 390)">🔄 Repeat (35d)</button>
        </div>

        <!-- Recency -->
        <div class="slider-row">
          <div class="slider-header">
            <span class="slider-label">Recency</span>
            <span id="v-rec" class="slider-val">450 days</span>
          </div>
          <input type="range" class="slider-input" id="s-rec" min="1" max="600" value="450" oninput="sync('s-rec', 'v-rec', ' days'); run();">
        </div>

        <!-- Frequency -->
        <div class="slider-row">
          <div class="slider-header">
            <span class="slider-label">Frequency</span>
            <span id="v-freq" class="slider-val">1 order</span>
          </div>
          <input type="range" class="slider-input" id="s-freq" min="1" max="25" value="1" oninput="sync('s-freq', 'v-freq', ' order'); calc(); run();">
        </div>

        <!-- Monetary -->
        <div class="slider-row">
          <div class="slider-header">
            <span class="slider-label">Monetary Spend</span>
            <span id="v-mon" class="slider-val">R$ 45.00</span>
          </div>
          <input type="range" class="slider-input" id="s-mon" min="10" max="3000" step="10" value="45" oninput="sync('s-mon', 'v-mon', ' R$'); calc(); run();">
        </div>

        <!-- Auto AOV -->
        <div class="slider-row" style="margin-bottom:0;">
          <div class="slider-header">
            <span class="slider-label">Calculated AOV</span>
            <span id="v-aov" class="slider-val" style="color:var(--emerald);">R$ 45.00</span>
          </div>
        </div>
      </div>

      <!-- Right: Churn Score -->
      <div class="card">
        <div class="churn-box">
          <div id="b-risk" class="badge badge-churn">High Churn Risk</div>
          <div id="v-prob" class="prob-val" style="color:var(--rose);">100%</div>
          <div class="prob-sub">Estimated Churn Risk</div>

          <div class="gauge-bg">
            <div id="g-bar" class="gauge-bar" style="width: 100%;"></div>
          </div>

          <div class="action-pill">
            <strong>Recommended Action:</strong>
            <span id="v-act">Customer dormant >120 days. Send win-back discount voucher.</span>
          </div>
        </div>
      </div>

    </div>

    <!-- RFM Segmentation Cards (Clean & Minimal) -->
    <div class="cohort-row">
      <div class="cohort-item">
        <span class="cohort-tag tag-vip">VIP</span>
        <div class="cohort-metric">> R$ 1,000 &bull; 5+ orders</div>
        <div class="cohort-hint">Loyalty gifts & priority access</div>
      </div>
      <div class="cohort-item">
        <span class="cohort-tag tag-loyal">Loyal</span>
        <div class="cohort-metric">3 to 4 orders</div>
        <div class="cohort-hint">Category cross-sells & rewards</div>
      </div>
      <div class="cohort-item">
        <span class="cohort-tag tag-reg">Regular</span>
        <div class="cohort-metric">2 orders</div>
        <div class="cohort-hint">Replenishment reminders</div>
      </div>
      <div class="cohort-item">
        <span class="cohort-tag tag-risk">At-Risk</span>
        <div class="cohort-metric">Dormant > 120 days</div>
        <div class="cohort-hint">Time-limited discount offer</div>
      </div>
    </div>

  </main>

  <footer>
    Customer Analytics Platform &bull; FastAPI &bull; Port 8000
  </footer>

  <script>
    function sync(id, txtId, suf) {
      const v = document.getElementById(id).value;
      document.getElementById(txtId).innerText = (id === 's-mon' ? 'R$ ' + parseFloat(v).toFixed(2) : v + suf);
    }

    function calc() {
      const f = parseFloat(document.getElementById('s-freq').value) || 1;
      const m = parseFloat(document.getElementById('s-mon').value) || 0;
      document.getElementById('v-aov').innerText = 'R$ ' + (m / f).toFixed(2);
    }

    function applyPreset(rec, freq, mon) {
      document.getElementById('s-rec').value = rec;
      document.getElementById('s-freq').value = freq;
      document.getElementById('s-mon').value = mon;
      sync('s-rec', 'v-rec', ' days');
      sync('s-freq', 'v-freq', freq > 1 ? ' orders' : ' order');
      sync('s-mon', 'v-mon', ' R$');
      calc();
      run();
    }

    async function run() {
      const rec = parseFloat(document.getElementById('s-rec').value);
      const freq = parseFloat(document.getElementById('s-freq').value);
      const mon = parseFloat(document.getElementById('s-mon').value);
      const aov = parseFloat((mon / freq).toFixed(2));

      try {
        const res = await fetch('/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ frequency: freq, monetary: mon, recency: rec, avg_order_value: aov })
        });
        const data = await res.json();
        const isChurn = (data.prediction === 1 || data.churn_prediction === 1);
        const prob = data.probability !== undefined ? Math.round(data.probability * 100) : (isChurn ? 100 : 0);

        const badge = document.getElementById('b-risk');
        const probEl = document.getElementById('v-prob');
        const gauge = document.getElementById('g-bar');
        const act = document.getElementById('v-act');

        probEl.innerText = prob + '%';
        gauge.style.width = prob + '%';

        if (isChurn || prob > 50) {
          badge.className = 'badge badge-churn';
          badge.innerText = 'High Churn Risk';
          probEl.style.color = 'var(--rose)';
          act.innerText = 'Dormant ' + rec + ' days. Send 15-20% win-back discount.';
        } else {
          badge.className = 'badge badge-retained';
          badge.innerText = 'Active / Retained';
          probEl.style.color = 'var(--emerald)';
          act.innerText = 'Active customer (' + freq + ' orders). Propose loyalty perks.';
        }
      } catch (e) {
        console.warn('API error', e);
      }
    }
  </script>
</body>
</html>
"""

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "customer_analytics_churn_api",
        "version": "1.2.0",
        "model_loaded": True
    }

@app.get("/api/metrics")
def get_metrics():
    return {
        "total_revenue_brl": 13591643.70,
        "total_orders": 99441,
        "total_customers": 96096,
        "average_order_value_brl": 137.75,
        "historical_churn_rate": 0.647,
        "model_accuracy": 0.998
    }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" not in accept and "application/json" in accept:
        return JSONResponse({"message": "Churn API is running"})
    return HTMLResponse(content=HTML_DASHBOARD)

@app.post("/predict")
def predict(customer: CustomerFeatures):
    features = [
        customer.frequency,
        customer.monetary,
        customer.recency,
        customer.avg_order_value,
    ]
    result = predict_churn(features)
    return result

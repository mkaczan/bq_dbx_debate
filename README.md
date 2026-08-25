# 🚀⚡🏛️ BigQuery vs Databricks Strategic Debate Arena & Enterprise Arbiter

A multi-agent AI system, simulation engine, and interactive web application that orchestrates an evidence-backed strategic debate between **Google BigQuery Migration Strategist**, **Databricks Defense Advocate**, and an **Independent Principal Enterprise Architect & Arbiter**.

---

## 🌟 Key Capabilities & Architecture

### 1. The 3 Specialized AI Agents
- **🚀 Google BigQuery Enterprise Strategist**:
  - **Fluid Scaling**: True per-second billing with zero cooldown penalties.
  - **Dataproc Serverless with Lightning Engine**: Native SIMD C++ vectorized execution (Velox / Gluten) delivering up to 2x faster performance than Databricks Photon at $0 DBU software markup.
  - **BigLake Zero-Copy Federation**: Day-1 in-place querying of Delta Lake / Apache Iceberg tables in ADLS/S3 with $0 data movement and zero downtime.
  - **BigQuery BI Engine**: In-memory DirectQuery acceleration reducing dashboard load times to <500ms with zero DAX or report rework.
  - **Capacitor Autonomous Clustering**: Free background storage optimization eliminating the 15-30% "Delta Maintenance Tax" (`OPTIMIZE`/`VACUUM`).

- **⚡ Databricks Defense Advocate**:
  - **PySpark / bigframes Incompatibility Scanner**: Detects distributed RDDs (`mapPartitions`), Python UDFs, custom MLlib pipelines, and DLT streaming code requiring 100+ engineer hours per pipeline.
  - **Total Cost of Migration (TCOM)**: Exposes hidden dual-licensing taxes, team retraining dips, and multi-year ROI payback traps.
  - **Hidden BigQuery Surcharges**: Exposes Storage Write API ingestion fees ($0.025/GB), BI Engine RAM reservations ($30.36/GB/mo), and BigLake cross-cloud egress costs.
  - **14-Day In-Place Optimization Playbook**: Serverless SQL, Photon Engine, Liquid Clustering, and Spot Fleets delivering 40-50% cost reductions with zero migration risk.
  - **Apache 2.0 Open Unity Catalog & UniForm**: Universal multi-cloud format standard for DORA exit compliance.

- **🏛️ Independent Principal Enterprise Architect (Arbiter)**:
  - **6D Enterprise Architecture Framework**: Conway's Law, Team Topologies, M&A Ingestion Agility, Storage Decoupling, DORA Regulatory Sovereignty, and Technical Debt Modernization.
  - **7-Pillar Multi-Criteria Decision Analysis (MCDA)**: Dynamically weights options and scores:
    1. Option 1: Big-Bang BigQuery Migration (GCP Monolith)
    2. Option 2: Databricks In-Place Optimization (Status Quo Tuning)
    3. Option 3: Strategic Open Lakehouse Mesh (Delta UniForm / Iceberg + Domain Federation)
  - **Phased Implementation Blueprint & Net Value Model**.

---

## 🏢 Preset Scenarios
1. **🏥 Pan-European Healthcare & Hospital Network**: M&A integration, EU DORA compliance, 1,000 legacy T-SQL stored procedures, and Azure Databricks spend.
2. **🛍️ Global Omnichannel Retail**: 220 Power BI users, SQL Warehouse slot queues, Black Friday burst queries, and Delta maintenance tax.
3. **💳 NextGen FinTech & Payment Gateway**: 24/7 DLT fraud streaming, multi-cloud active-active resilience, and cross-cloud egress minimization.
4. **📊 Acuity Media AdTech**: Spiky clickstream queries, Fluid Scaling price-performance, and Gemini in-situ SQL multimodal analytics.

---

## 🛠️ Project Structure
```
bq_dbx_debate/
├── app/
│   ├── config.py                 # Benchmarks, DBU rates, model configuration
│   ├── models/
│   │   └── schemas.py            # Pydantic schemas (EnterpriseContext, DebateTurn, Verdict, etc.)
│   ├── engine/
│   │   ├── presets.py            # 4 Preset enterprise scenarios
│   │   └── orchestrator.py       # Multi-agent turn management & prompt dispatch
│   ├── tools/
│   │   ├── bq_tools.py           # Telemetry, Power BI, TCO, and BigLake calculators
│   │   ├── dbx_tools.py          # Spark compatibility, TCOM, hidden costs, optimization
│   │   └── arch_tools.py         # MCDA 7-pillar matrix & decision scorecard
│   ├── agents/
│   │   ├── base.py               # Gemini client & heuristic fallback engine
│   │   ├── bq_strategist.py      # BigQuery Compete Specialist Agent
│   │   ├── dbx_advocate.py       # Databricks Defense Advocate Agent
│   │   └── principal_architect.py# Independent Principal Enterprise Architect
│   └── server/
│       ├── api.py                # FastAPI REST API & static file mount
│       └── static/
│           ├── index.html        # Interactive glassmorphic single-page web UI
│           ├── style.css         # Dark-mode enterprise CSS & glow animations
│           └── app.js            # Frontend orchestration, charts, and intervention
├── tests/
│   ├── test_debate.py            # Unit tests for models, tools, agents, and orchestrator
│   └── test_api.py               # Integration tests for FastAPI endpoints and static UI
├── start.py                      # Application runner
└── README.md
```

---

## 🚀 How to Run

### 1. Run the Web Application
```bash
.venv/bin/python3 start.py
```
Open your browser at **`http://127.0.0.1:8000`**.

### 2. Run the Test Suite
```bash
.venv/bin/python3 -m unittest discover tests
```

---

## 📡 REST API Endpoints
- `GET /api/presets` — Retrieve all preset scenarios
- `POST /api/debate/start` — Start a new debate session
- `POST /api/debate/step` — Execute next turn
- `POST /api/debate/run-all` — Execute all turns and synthesize verdict
- `POST /api/debate/intervene` — Inject user prompt/challenge and get instant agent response
- `GET /api/debate/{session_id}` — Get session status and full transcript
- `POST /api/tools/diagnostics` — Run all mathematical forensic tools on a custom workload
- `GET /api/export/markdown/{session_id}` — Export executive brief as Markdown
- `GET /api/export/json/{session_id}` — Export session state as JSON
- `GET /api/health` — Health check

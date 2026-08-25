/**
 * BigQuery vs Databricks Strategic Debate Arena - Frontend Engine
 */

// Application State
const state = {
  sessionId: null,
  session: null,
  presets: {},
  currentContext: null,
  activeTab: 'tab-mcda',
  isAutoPlaying: false,
  charts: {
    radar: null,
    tco: null,
    powerBi: null
  }
};

// DOM Elements
const elements = {
  presetSelector: document.getElementById('preset-selector'),
  displayEnterpriseName: document.getElementById('display-enterprise-name'),
  displayIndustryBadge: document.getElementById('display-industry-badge'),
  displayScenarioSummary: document.getElementById('display-scenario-summary'),
  
  // Stat Badges
  statDbuSpend: document.getElementById('stat-dbu-spend'),
  statStorageTb: document.getElementById('stat-storage-tb'),
  statPysparkJobs: document.getElementById('stat-pyspark-jobs'),
  statPowerbiUsers: document.getElementById('stat-powerbi-users'),
  statStoredProcs: document.getElementById('stat-stored-procs'),
  statCloudStrategy: document.getElementById('stat-cloud-strategy'),
  
  // Status Chips & Indicators
  sessionStatusChip: document.getElementById('session-status-chip'),
  sessionStatusText: document.getElementById('session-status-text'),
  turnCounterBadge: document.getElementById('turn-counter-badge'),
  liveTypingIndicator: document.getElementById('live-typing-indicator'),
  typingAgentName: document.getElementById('typing-agent-name'),
  
  // Agent Cards
  cardAgentBq: document.getElementById('card-agent-bq'),
  cardAgentArch: document.getElementById('card-agent-arch'),
  cardAgentDbx: document.getElementById('card-agent-dbx'),
  badgeStatusBq: document.getElementById('badge-status-bq'),
  badgeStatusArch: document.getElementById('badge-status-arch'),
  badgeStatusDbx: document.getElementById('badge-status-dbx'),
  
  // Controls
  btnStartDebate: document.getElementById('btn-start-debate'),
  btnStepTurn: document.getElementById('btn-step-turn'),
  btnRunAll: document.getElementById('btn-run-all'),
  btnOpenIntervene: document.getElementById('btn-open-intervene'),
  btnResetDebate: document.getElementById('btn-reset-debate'),
  
  // Transcript Container
  transcriptStream: document.getElementById('transcript-stream'),
  emptyPlaceholder: document.getElementById('empty-transcript-placeholder'),
  
  // Modals & Panels
  paramsModal: document.getElementById('params-modal'),
  btnOpenParamsModal: document.getElementById('btn-open-params-modal'),
  btnCloseParamsModal: document.getElementById('btn-close-params-modal'),
  btnCancelParams: document.getElementById('btn-cancel-params'),
  btnSaveParams: document.getElementById('btn-save-params'),
  
  interveneModal: document.getElementById('intervene-modal'),
  btnCloseInterveneModal: document.getElementById('btn-close-intervene-modal'),
  btnCancelIntervene: document.getElementById('btn-cancel-intervene'),
  btnSubmitIntervene: document.getElementById('btn-submit-intervene'),
  textareaUserPrompt: document.getElementById('textarea-user-prompt'),
  
  exportModal: document.getElementById('export-modal'),
  btnExportModal: document.getElementById('btn-export-modal'),
  btnCloseExportModal: document.getElementById('btn-close-export-modal'),
  exportMarkdownPreview: document.getElementById('export-markdown-preview'),
  btnCopyMarkdown: document.getElementById('btn-copy-markdown'),
  btnDownloadMarkdown: document.getElementById('btn-download-markdown'),
  btnDownloadJson: document.getElementById('btn-download-json'),

  // Power BI Slider
  pbiSlider: document.getElementById('pbi-concurrency-slider'),
  pbiSliderVal: document.getElementById('pbi-slider-val'),
  pbiDbxTime: document.getElementById('pbi-dbx-time'),
  pbiBqTime: document.getElementById('pbi-bq-time'),
  pbiQueueRisk: document.getElementById('pbi-queue-risk')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  await loadPresets();
  setupDiagnosticsTabs();
});

// Event Listeners Setup
function setupEventListeners() {
  // Preset selection
  elements.presetSelector.addEventListener('change', (e) => {
    const key = e.target.value;
    if (state.presets[key]) {
      applyContext(state.presets[key]);
    }
  });

  // Debate Controls
  elements.btnStartDebate.addEventListener('click', () => handleStartDebate());
  elements.btnStepTurn.addEventListener('click', () => handleStepTurn());
  elements.btnRunAll.addEventListener('click', () => handleRunAll());
  elements.btnResetDebate.addEventListener('click', () => handleResetDebate());

  // Modal Open / Close
  elements.btnOpenParamsModal.addEventListener('click', () => openParamsModal());
  elements.btnCloseParamsModal.addEventListener('click', () => closeParamsModal());
  elements.btnCancelParams.addEventListener('click', () => closeParamsModal());
  elements.btnSaveParams.addEventListener('click', () => saveParamsModal());

  elements.btnOpenIntervene.addEventListener('click', () => openInterveneModal());
  elements.btnCloseInterveneModal.addEventListener('click', () => closeInterveneModal());
  elements.btnCancelIntervene.addEventListener('click', () => closeInterveneModal());
  elements.btnSubmitIntervene.addEventListener('click', () => submitIntervene());

  elements.btnExportModal.addEventListener('click', () => openExportModal());
  elements.btnCloseExportModal.addEventListener('click', () => closeExportModal());
  elements.btnCopyMarkdown.addEventListener('click', () => copyMarkdownToClipboard());
  elements.btnDownloadMarkdown.addEventListener('click', () => downloadMarkdownFile());
  elements.btnDownloadJson.addEventListener('click', () => downloadJsonFile());

  // Quick preset intervention prompts
  document.querySelectorAll('.quick-prompt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      elements.textareaUserPrompt.value = btn.textContent.trim();
    });
  });

  // Power BI Slider
  if (elements.pbiSlider) {
    elements.pbiSlider.addEventListener('input', (e) => {
      const users = parseInt(e.target.value);
      elements.pbiSliderVal.textContent = `${users} Users`;
      updatePowerBiSimulation(users);
    });
  }
}

// Load Preset Scenarios from Backend
async function loadPresets() {
  try {
    const res = await fetch('/api/presets');
    if (!res.ok) throw new Error('Failed to load presets');
    state.presets = await res.json();

    const defaultKey = 'healthcare_m_and_a';
    if (state.presets[defaultKey]) {
      elements.presetSelector.value = defaultKey;
      applyContext(state.presets[defaultKey]);
    }
  } catch (err) {
    console.error('Error loading presets:', err);
  }
}

// Apply Workload Context to UI and Forensics
function applyContext(ctx) {
  state.currentContext = JSON.parse(JSON.stringify(ctx));

  elements.displayEnterpriseName.firstElementChild.textContent = ctx.enterprise_name;
  elements.displayIndustryBadge.textContent = ctx.industry;
  elements.displayScenarioSummary.textContent = `${ctx.cloud_strategy} | ${ctx.regulatory_framework}`;

  elements.statDbuSpend.textContent = `$${Number(ctx.annual_dbu_spend).toLocaleString()}`;
  elements.statStorageTb.textContent = `${ctx.storage_tb} TB`;
  elements.statPysparkJobs.textContent = `${ctx.total_pyspark_jobs} Jobs`;
  elements.statPowerbiUsers.textContent = `${ctx.powerbi_users_count} Users`;
  elements.statStoredProcs.textContent = `${Number(ctx.legacy_stored_procs).toLocaleString()} Procs`;
  elements.statCloudStrategy.textContent = ctx.primary_cloud;

  if (elements.pbiSlider) {
    elements.pbiSlider.value = ctx.powerbi_users_count;
    elements.pbiSliderVal.textContent = `${ctx.powerbi_users_count} Users`;
  }

  // Populate form fields
  document.getElementById('input-enterprise-name').value = ctx.enterprise_name;
  document.getElementById('input-industry').value = ctx.industry;
  document.getElementById('input-dbu-spend').value = ctx.annual_dbu_spend;
  document.getElementById('input-storage-tb').value = ctx.storage_tb;
  document.getElementById('input-pyspark-jobs').value = ctx.total_pyspark_jobs;
  document.getElementById('input-loc').value = ctx.lines_of_code;
  document.getElementById('input-powerbi-users').value = ctx.powerbi_users_count;
  document.getElementById('input-stored-procs').value = ctx.legacy_stored_procs;
  document.getElementById('input-primary-cloud').value = ctx.primary_cloud;
  document.getElementById('input-regulatory').value = ctx.regulatory_framework;

  // Run diagnostics for updated context
  refreshDiagnostics(state.currentContext);
}

// Refresh Live Diagnostics & Charts
async function refreshDiagnostics(ctx) {
  try {
    const res = await fetch('/api/tools/diagnostics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ctx)
    });
    if (!res.ok) throw new Error('Diagnostics call failed');
    const diag = await res.json();

    renderMCDADiagnostics(diag.mcda_matrix);
    renderTCODiagnostics(diag);
    renderSparkFrictionDiagnostics(diag.databricks_forensics.compatibility);
    renderPowerBiDiagnostics(diag.bigquery_forensics.powerbi);
  } catch (err) {
    console.error('Error refreshing diagnostics:', err);
  }
}

// Render MCDA Scorecard & Radar Chart
function renderMCDADiagnostics(mcda) {
  const labels = Object.keys(mcda.weights).map(k => k.replace(/_/g, ' ').toUpperCase());
  const bqScores = Object.keys(mcda.weights).map(k => mcda.scores_by_option.option_1_bigquery_migration[k]);
  const dbxScores = Object.keys(mcda.weights).map(k => mcda.scores_by_option.option_2_databricks_status_quo_tuning[k]);
  const meshScores = Object.keys(mcda.weights).map(k => mcda.scores_by_option.option_3_open_lakehouse_data_mesh[k]);

  // Render Radar Chart
  const ctx = document.getElementById('mcdaRadarChart');
  if (ctx) {
    if (state.charts.radar) state.charts.radar.destroy();
    state.charts.radar = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Option 1: BigQuery Migration',
            data: bqScores,
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            borderWidth: 2,
            pointBackgroundColor: '#3b82f6'
          },
          {
            label: 'Option 2: Databricks In-Place',
            data: dbxScores,
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.2)',
            borderWidth: 2,
            pointBackgroundColor: '#ef4444'
          },
          {
            label: 'Option 3: Strategic Open Mesh',
            data: meshScores,
            borderColor: '#f59e0b',
            backgroundColor: 'rgba(245, 158, 11, 0.25)',
            borderWidth: 2.5,
            pointBackgroundColor: '#f59e0b'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            angleLines: { color: 'rgba(75, 85, 99, 0.3)' },
            grid: { color: 'rgba(75, 85, 99, 0.3)' },
            pointLabels: { color: '#9ca3af', font: { size: 10 } },
            ticks: { display: false, min: 0, max: 10 }
          }
        },
        plugins: {
          legend: { labels: { color: '#d1d5db', font: { size: 10 } } }
        }
      }
    });
  }

  // Populate Table
  const tbody = document.getElementById('mcda-table-body');
  if (tbody) {
    tbody.innerHTML = '';
    Object.keys(mcda.weights).forEach(k => {
      const tr = document.createElement('tr');
      tr.className = 'hover:bg-gray-800/40';
      tr.innerHTML = `
        <td class="p-2 border border-gray-800 font-medium text-gray-300">${k.replace(/_/g, ' ').titleCase()}</td>
        <td class="p-2 border border-gray-800 text-center text-gray-400 font-mono">${Math.round(mcda.weights[k] * 100)}%</td>
        <td class="p-2 border border-gray-800 text-center text-blue-400 font-mono">${mcda.scores_by_option.option_1_bigquery_migration[k].toFixed(1)}</td>
        <td class="p-2 border border-gray-800 text-center text-red-400 font-mono">${mcda.scores_by_option.option_2_databricks_status_quo_tuning[k].toFixed(1)}</td>
        <td class="p-2 border border-gray-800 text-center text-amber-400 font-mono font-bold">${mcda.scores_by_option.option_3_open_lakehouse_data_mesh[k].toFixed(1)}</td>
      `;
      tbody.appendChild(tr);
    });

    // Total Row
    const trTotal = document.createElement('tr');
    trTotal.className = 'bg-gray-900/90 font-bold';
    trTotal.innerHTML = `
      <td class="p-2 border border-gray-800 text-white">Weighted Composite Score</td>
      <td class="p-2 border border-gray-800 text-center text-white font-mono">100%</td>
      <td class="p-2 border border-gray-800 text-center text-blue-400 font-mono">${mcda.weighted_totals.option_1_bigquery_migration.toFixed(2)}</td>
      <td class="p-2 border border-gray-800 text-center text-red-400 font-mono">${mcda.weighted_totals.option_2_databricks_status_quo_tuning.toFixed(2)}</td>
      <td class="p-2 border border-gray-800 text-center text-amber-400 font-mono text-sm">${mcda.weighted_totals.option_3_open_lakehouse_data_mesh.toFixed(2)}</td>
    `;
    tbody.appendChild(trTotal);
  }

  // Callout
  const callout = document.getElementById('mcda-winner-callout');
  if (callout) {
    callout.innerHTML = `<strong>🏆 Principal Architect Recommendation:</strong> ${mcda.winning_option_name} achieves the highest weighted enterprise score (<strong>${mcda.weighted_totals[mcda.winning_option_key]} / 10</strong>).`;
  }
}

// Render TCO Diagnostics & Chart
function renderTCODiagnostics(diag) {
  const tcoBq = diag.bigquery_forensics.tco;
  const dbxOpt = diag.databricks_forensics.inplace_optimization;
  const tcom = diag.databricks_forensics.tcom_risk;

  document.getElementById('tco-current-spend').textContent = `$${Math.round(tcoBq.current_databricks_annual_spend).toLocaleString()}`;
  document.getElementById('tco-bq-spend').textContent = `$${Math.round(tcoBq.bigquery_modeled_annual_spend).toLocaleString()}`;
  document.getElementById('tco-dbx-opt-spend').textContent = `$${Math.round(dbxOpt.optimized_annual_spend_usd).toLocaleString()}`;
  document.getElementById('tco-migration-risk').textContent = `$${Math.round(tcom.total_cost_of_migration_tcom_usd).toLocaleString()}`;

  const ctx = document.getElementById('tcoBarChart');
  if (ctx) {
    if (state.charts.tco) state.charts.tco.destroy();
    state.charts.tco = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Current DBX Spend', 'BigQuery Editions', 'DBX In-Place Opt.', 'Upfront TCOM Sunk'],
        datasets: [{
          label: 'Annual Cost ($ USD)',
          data: [
            tcoBq.current_databricks_annual_spend,
            tcoBq.bigquery_modeled_annual_spend,
            dbxOpt.optimized_annual_spend_usd,
            tcom.total_cost_of_migration_tcom_usd
          ],
          backgroundColor: [
            'rgba(156, 163, 175, 0.7)',
            'rgba(59, 130, 246, 0.8)',
            'rgba(239, 68, 68, 0.8)',
            'rgba(139, 92, 246, 0.8)'
          ],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { ticks: { color: '#9ca3af', font: { size: 10 } }, grid: { display: false } },
          y: {
            ticks: {
              color: '#9ca3af',
              font: { size: 10 },
              callback: (val) => `$${val/1000}k`
            },
            grid: { color: 'rgba(75, 85, 99, 0.2)' }
          }
        }
      }
    });
  }
}

// Render Spark Refactoring Table
function renderSparkFrictionDiagnostics(compat) {
  const tbody = document.getElementById('spark-friction-tbody');
  if (!tbody) return;

  tbody.innerHTML = '';
  const breakdown = compat.friction_breakdown;
  Object.keys(breakdown).forEach(k => {
    const item = breakdown[k];
    const tr = document.createElement('tr');
    tr.className = 'hover:bg-gray-800/40';
    tr.innerHTML = `
      <td class="p-2.5 border border-gray-800 font-semibold text-gray-200">${k.replace(/_/g, ' ').titleCase()}</td>
      <td class="p-2.5 border border-gray-800 text-center text-gray-300 font-mono">${item.instances}</td>
      <td class="p-2.5 border border-gray-800 text-center"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${item.severity === 'CRITICAL' ? 'bg-red-950 text-red-300 border border-red-800' : 'bg-yellow-950 text-yellow-300 border border-yellow-800'}">${item.severity}</span></td>
      <td class="p-2.5 border border-gray-800 text-center text-red-400 font-mono font-bold">${item.rewrite_hours} hrs</td>
      <td class="p-2.5 border border-gray-800 text-gray-400">${item.issue}</td>
    `;
    tbody.appendChild(tr);
  });

  document.getElementById('spark-total-hours').textContent = `${compat.total_engineering_rewrite_hours.toLocaleString()} Hours`;
  document.getElementById('spark-total-cost').textContent = `$${compat.total_refactoring_consulting_cost_usd.toLocaleString()}`;
}

// Render Power BI Concurrency Diagnostics
function renderPowerBiDiagnostics(pbi) {
  elements.pbiDbxTime.textContent = `${pbi.databricks_avg_dashboard_load_time_sec}s`;
  elements.pbiBqTime.textContent = `${pbi.bigquery_bi_engine_load_time_sec}s`;
  elements.pbiQueueRisk.textContent = `${pbi.databricks_queue_risk} Queue Risk`;

  const ctx = document.getElementById('powerBiBarChart');
  if (ctx) {
    if (state.charts.powerBi) state.charts.powerBi.destroy();
    state.charts.powerBi = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Databricks SQL DirectQuery', 'BigQuery BI Engine In-Memory'],
        datasets: [{
          label: 'Avg Dashboard Load Time (seconds)',
          data: [pbi.databricks_avg_dashboard_load_time_sec, pbi.bigquery_bi_engine_load_time_sec],
          backgroundColor: ['rgba(239, 68, 68, 0.8)', 'rgba(59, 130, 246, 0.8)'],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: '#9ca3af', font: { size: 10 } }, grid: { display: false } },
          y: {
            ticks: { color: '#9ca3af', font: { size: 10 }, callback: (v) => `${v}s` },
            grid: { color: 'rgba(75, 85, 99, 0.2)' }
          }
        }
      }
    });
  }
}

// Power BI Interactive Simulation
function updatePowerBiSimulation(users) {
  const whSlots = 16;
  const simDax = Math.floor(users * 0.60);
  const queueRatio = Math.max(1.0, simDax / whSlots);
  const dbxTime = (3.8 * queueRatio).toFixed(2);
  const bqTime = 0.45;

  elements.pbiDbxTime.textContent = `${dbxTime}s`;
  elements.pbiBqTime.textContent = `${bqTime}s`;
  elements.pbiQueueRisk.textContent = queueRatio > 1.5 ? 'HIGH Queue Risk' : (queueRatio > 1.0 ? 'MEDIUM Queue Risk' : 'LOW Queue Risk');

  if (state.charts.powerBi) {
    state.charts.powerBi.data.datasets[0].data = [parseFloat(dbxTime), bqTime];
    state.charts.powerBi.update();
  }
}

// Render Blueprint Roadmap
function renderBlueprintRoadmap(roadmap) {
  const container = document.getElementById('blueprint-roadmap-container');
  if (!container) return;

  container.innerHTML = '';
  roadmap.forEach(step => {
    const card = document.createElement('div');
    card.className = 'p-3 rounded-lg bg-gray-900 border border-gray-800 space-y-1.5';
    card.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="font-bold text-amber-300 text-xs">${step.phase}</span>
        <span class="text-[10px] px-2 py-0.5 rounded bg-gray-800 text-gray-400 font-mono">${step.timeline}</span>
      </div>
      <p class="text-gray-300 text-xs">${step.action}</p>
      <div class="text-[11px] text-gray-400 flex flex-col sm:flex-row sm:items-center justify-between gap-1 pt-1 border-t border-gray-800/60">
        <span><strong class="text-emerald-400">Deliverable:</strong> ${step.key_deliverable}</span>
        <span class="text-gray-500 italic">${step.risk_mitigation}</span>
      </div>
    `;
    container.appendChild(card);
  });
}

// Setup Diagnostics Tabs
function setupDiagnosticsTabs() {
  document.querySelectorAll('.diag-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.diag-tab-btn').forEach(b => {
        b.classList.remove('active', 'bg-indigo-600', 'text-white');
        b.classList.add('text-gray-400');
      });
      btn.classList.add('active', 'bg-indigo-600', 'text-white');
      btn.classList.remove('text-gray-400');

      const targetTab = btn.getAttribute('data-tab');
      document.querySelectorAll('.diag-tab-content').forEach(c => c.classList.add('hidden'));
      document.getElementById(targetTab).classList.remove('hidden');
      state.activeTab = targetTab;
    });
  });
}

// ==========================================
// Multi-Agent Debate Execution Handlers
// ==========================================

async function handleStartDebate() {
  if (!state.currentContext) return;

  try {
    elements.btnStartDebate.disabled = true;
    setTypingIndicator(true, 'Initializing Multi-Agent Session...');

    const res = await fetch('/api/debate/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        context: state.currentContext,
        rounds: 2
      })
    });
    if (!res.ok) throw new Error('Failed to start debate session');

    state.session = await res.json();
    state.sessionId = state.session.session_id;

    // Update UI
    elements.sessionStatusChip.classList.remove('hidden');
    elements.sessionStatusText.textContent = `Live Session: Round 1`;
    elements.btnStepTurn.disabled = false;
    elements.btnRunAll.disabled = false;
    elements.btnOpenIntervene.disabled = false;

    // Clear stream
    elements.transcriptStream.innerHTML = '';

    // Automatically execute the opening speech from BigQuery Strategist
    await handleStepTurn();
  } catch (err) {
    console.error('Error starting debate:', err);
    setTypingIndicator(false);
    elements.btnStartDebate.disabled = false;
  }
}

async function handleStepTurn() {
  if (!state.sessionId) return;

  try {
    elements.btnStepTurn.disabled = true;
    setTypingIndicator(true, 'Agent is formulating strategic speech...');

    const res = await fetch('/api/debate/step', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: state.sessionId })
    });
    if (!res.ok) throw new Error('Failed to step turn');

    const data = await res.json();
    state.session = data.session;

    setTypingIndicator(false);

    if (data.turn) {
      appendTurnToStream(data.turn);
      highlightActiveAgent(data.turn.speaker);
    }

    elements.turnCounterBadge.textContent = `${state.session.turns.length} Turns`;
    elements.sessionStatusText.textContent = data.is_completed ? 'Debate Completed' : `Round ${state.session.current_round}`;

    if (data.is_completed) {
      elements.btnStepTurn.disabled = true;
      elements.btnRunAll.disabled = true;
      highlightActiveAgent('principal_architect');
      if (state.session.final_verdict) {
        renderBlueprintRoadmap(state.session.final_verdict.phased_roadmap);
      }
    } else {
      elements.btnStepTurn.disabled = false;
    }
  } catch (err) {
    console.error('Error executing turn:', err);
    setTypingIndicator(false);
    elements.btnStepTurn.disabled = false;
  }
}

async function handleRunAll() {
  if (!state.sessionId) return;

  state.isAutoPlaying = true;
  elements.btnRunAll.disabled = true;
  elements.btnStepTurn.disabled = true;

  while (state.isAutoPlaying && state.session && state.session.status !== 'completed') {
    await handleStepTurn();
    if (state.session.status !== 'completed') {
      await new Promise(r => setTimeout(r, 1200));
    }
  }

  state.isAutoPlaying = false;
}

function handleResetDebate() {
  state.sessionId = null;
  state.session = null;
  state.isAutoPlaying = false;

  elements.transcriptStream.innerHTML = '';
  elements.transcriptStream.appendChild(elements.emptyPlaceholder);
  elements.emptyPlaceholder.classList.remove('hidden');

  elements.btnStartDebate.disabled = false;
  elements.btnStepTurn.disabled = true;
  elements.btnRunAll.disabled = true;
  elements.btnOpenIntervene.disabled = true;
  elements.turnCounterBadge.textContent = '0 Turns';
  elements.sessionStatusText.textContent = 'Ready';

  resetAgentHighlight();
}

// Append Turn Speech Bubble to UI Stream
function appendTurnToStream(turn) {
  if (elements.emptyPlaceholder) {
    elements.emptyPlaceholder.classList.add('hidden');
  }

  const turnEl = document.createElement('div');
  turnEl.className = 'glass-card p-5 turn-enter space-y-3';

  // Speaker Badge styling
  let badgeClass = 'badge-bq';
  let glowClass = 'glow-bq';
  let borderLeft = 'border-l-4 border-l-blue-500';

  if (turn.speaker === 'databricks_advocate') {
    badgeClass = 'badge-dbx';
    glowClass = 'glow-dbx';
    borderLeft = 'border-l-4 border-l-red-500';
  } else if (turn.speaker === 'principal_architect') {
    badgeClass = 'badge-arch';
    glowClass = 'glow-arch';
    borderLeft = 'border-l-4 border-l-amber-500';
  } else if (turn.speaker === 'user') {
    badgeClass = 'badge-user';
    borderLeft = 'border-l-4 border-l-emerald-500';
  }

  turnEl.className += ` ${borderLeft}`;

  // Key argument pills
  const keyArgPills = (turn.key_arguments || []).map(arg => 
    `<span class="px-2.5 py-1 rounded-full text-[11px] font-medium bg-gray-800/80 text-gray-200 border border-gray-700/60 flex items-center gap-1"><i class="fa-solid fa-check text-indigo-400"></i> ${arg}</span>`
  ).join('');

  // Citations
  const citationList = (turn.citations || []).map(c => 
    `<span class="text-[10px] text-gray-400 italic"><i class="fa-solid fa-bookmark text-gray-500 mr-1"></i>${c}</span>`
  ).join(' &bull; ');

  // Render markdown content
  const renderedContent = marked.parse(turn.content);

  turnEl.innerHTML = `
    <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-2 border-b border-gray-800/80 gap-2">
      <div class="flex items-center space-x-2.5">
        <span class="text-2xl">${turn.avatar}</span>
        <div>
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <span>${turn.speaker_display_name}</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${badgeClass}">Round ${turn.round_number}</span>
          </h4>
          <span class="text-[11px] text-gray-400">${turn.speaker_role}</span>
        </div>
      </div>
      <div class="text-xs text-gray-400 flex items-center space-x-2">
        <span>Stance: <strong class="text-gray-200">${turn.stance}</strong></span>
      </div>
    </div>

    <!-- Speech Body -->
    <div class="markdown-body text-xs sm:text-sm">
      ${renderedContent}
    </div>

    <!-- Key Arguments Pills -->
    ${keyArgPills ? `<div class="flex flex-wrap gap-1.5 pt-2">${keyArgPills}</div>` : ''}

    <!-- Citations Footer -->
    ${citationList ? `<div class="pt-2 border-t border-gray-800/50 flex flex-wrap items-center gap-2">${citationList}</div>` : ''}
  `;

  elements.transcriptStream.appendChild(turnEl);
  turnEl.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

// Highlight Agent on Top Stage
function highlightActiveAgent(speaker) {
  resetAgentHighlight();

  if (speaker === 'bigquery_strategist') {
    elements.cardAgentBq.classList.add('glow-bq', 'speaking-pulse');
    elements.badgeStatusBq.textContent = 'Speaking';
    elements.badgeStatusBq.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-blue-600 text-white animate-pulse';
  } else if (speaker === 'databricks_advocate') {
    elements.cardAgentDbx.classList.add('glow-dbx', 'speaking-pulse');
    elements.badgeStatusDbx.textContent = 'Speaking';
    elements.badgeStatusDbx.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-red-600 text-white animate-pulse';
  } else if (speaker === 'principal_architect') {
    elements.cardAgentArch.classList.add('glow-arch', 'speaking-pulse');
    elements.badgeStatusArch.textContent = 'Delivering Verdict';
    elements.badgeStatusArch.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-amber-500 text-gray-950 font-bold animate-pulse';
  }
}

function resetAgentHighlight() {
  elements.cardAgentBq.classList.remove('glow-bq', 'speaking-pulse');
  elements.cardAgentDbx.classList.remove('glow-dbx', 'speaking-pulse');
  elements.cardAgentArch.classList.remove('glow-arch', 'speaking-pulse');

  elements.badgeStatusBq.textContent = 'Ready';
  elements.badgeStatusBq.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-blue-950 text-blue-300 border border-blue-800';

  elements.badgeStatusDbx.textContent = 'Ready';
  elements.badgeStatusDbx.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-red-950 text-red-300 border border-red-800';

  elements.badgeStatusArch.textContent = 'Awaiting Debate';
  elements.badgeStatusArch.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-amber-950 text-amber-300 border border-amber-800';
}

function setTypingIndicator(show, text = 'Agent formulating speech...') {
  if (show) {
    elements.liveTypingIndicator.classList.remove('hidden');
    elements.typingAgentName.textContent = text;
  } else {
    elements.liveTypingIndicator.classList.add('hidden');
  }
}

// ==========================================
// User Intervention Modal & Flow
// ==========================================

function openInterveneModal() {
  elements.interveneModal.classList.remove('hidden');
  elements.textareaUserPrompt.focus();
}

function closeInterveneModal() {
  elements.interveneModal.classList.add('hidden');
}

async function submitIntervene() {
  const promptText = elements.textareaUserPrompt.value.trim();
  if (!promptText || !state.sessionId) return;

  try {
    closeInterveneModal();
    setTypingIndicator(true, 'Injecting intervention & calculating counter-argument...');

    const res = await fetch('/api/debate/intervene', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: state.sessionId,
        user_prompt: promptText
      })
    });
    if (!res.ok) throw new Error('Intervention failed');

    const data = await res.json();
    state.session = data.session;

    setTypingIndicator(false);

    if (data.user_turn) appendTurnToStream(data.user_turn);
    if (data.agent_turn) {
      appendTurnToStream(data.agent_turn);
      highlightActiveAgent(data.agent_turn.speaker);
    }

    elements.turnCounterBadge.textContent = `${state.session.turns.length} Turns`;
    elements.textareaUserPrompt.value = '';
  } catch (err) {
    console.error('Error submitting intervention:', err);
    setTypingIndicator(false);
  }
}

// ==========================================
// Workload Parameters Modal & Flow
// ==========================================

function openParamsModal() {
  elements.paramsModal.classList.remove('hidden');
}

function closeParamsModal() {
  elements.paramsModal.classList.add('hidden');
}

function saveParamsModal() {
  const newCtx = {
    enterprise_name: document.getElementById('input-enterprise-name').value,
    industry: document.getElementById('input-industry').value,
    annual_dbu_spend: parseFloat(document.getElementById('input-dbu-spend').value) || 750000.0,
    storage_tb: parseFloat(document.getElementById('input-storage-tb').value) || 350.0,
    total_pyspark_jobs: parseInt(document.getElementById('input-pyspark-jobs').value) || 120,
    lines_of_code: parseInt(document.getElementById('input-loc').value) || 95000,
    powerbi_users_count: parseInt(document.getElementById('input-powerbi-users').value) || 75,
    legacy_stored_procs: parseInt(document.getElementById('input-stored-procs').value) || 600,
    primary_cloud: document.getElementById('input-primary-cloud').value,
    regulatory_framework: document.getElementById('input-regulatory').value,
    cloud_strategy: state.currentContext.cloud_strategy || "Multi-Cloud Strategy",
    mlflow_models_count: state.currentContext.mlflow_models_count || 30,
    streaming_pipelines_count: state.currentContext.streaming_pipelines_count || 10,
    m_and_a_acquisitions_per_year: state.currentContext.m_and_a_acquisitions_per_year || 2,
    current_pain_points: state.currentContext.current_pain_points || [],
    strategic_priorities: state.currentContext.strategic_priorities || []
  };

  applyContext(newCtx);
  closeParamsModal();
  handleResetDebate();
}

// ==========================================
// Export Report Handlers
// ==========================================

async function openExportModal() {
  if (!state.sessionId) {
    alert('Please start or run a debate session before exporting the brief.');
    return;
  }

  try {
    const res = await fetch(`/api/export/markdown/${state.sessionId}`);
    if (!res.ok) throw new Error('Failed to fetch markdown export');
    const mdText = await res.text();

    elements.exportMarkdownPreview.textContent = mdText;
    elements.exportModal.classList.remove('hidden');
  } catch (err) {
    console.error('Error opening export:', err);
  }
}

function closeExportModal() {
  elements.exportModal.classList.add('hidden');
}

function copyMarkdownToClipboard() {
  const text = elements.exportMarkdownPreview.textContent;
  navigator.clipboard.writeText(text).then(() => {
    elements.btnCopyMarkdown.innerHTML = `<i class="fa-solid fa-check text-emerald-400"></i><span>Copied!</span>`;
    setTimeout(() => {
      elements.btnCopyMarkdown.innerHTML = `<i class="fa-regular fa-copy"></i><span>Copy Markdown</span>`;
    }, 2000);
  });
}

function downloadMarkdownFile() {
  const text = elements.exportMarkdownPreview.textContent;
  const blob = new Blob([text], { type: 'text/markdown;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Debate_Brief_${state.currentContext.enterprise_name.replace(/\s+/g, '_')}_${state.sessionId.substring(0,8)}.md`;
  a.click();
  URL.revokeObjectURL(url);
}

async function downloadJsonFile() {
  if (!state.sessionId) return;
  try {
    const res = await fetch(`/api/export/json/${state.sessionId}`);
    const data = await res.json();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Debate_Session_${state.sessionId.substring(0,8)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error('Error downloading JSON:', err);
  }
}

// Utility: Title Case helper
String.prototype.titleCase = function() {
  return this.replace(/\w\S*/g, function(txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
};

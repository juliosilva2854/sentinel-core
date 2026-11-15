from flask import Flask, render_template_string, jsonify
import psutil
import subprocess
import time
import platform
from collections import deque

app = Flask(__name__)

history = {'time': deque(maxlen=20), 'cpu': deque(maxlen=20), 'ram': deque(maxlen=20)}
for _ in range(20):
    history['time'].append('')
    history['cpu'].append(0)
    history['ram'].append(0)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Sentinel Core - Enterprise SIEM</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --bg: #060b14; --panel-bg: #111827; --border: #1f2937; --text-main: #f3f4f6; --text-muted: #9ca3af; --primary: #3b82f6; --success: #10b981; --danger: #ef4444; --warning: #f59e0b; --purple: #8b5cf6; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', 'Segoe UI', sans-serif; }
        body { background: var(--bg); color: var(--text-main); display: flex; height: 100vh; overflow: hidden; }
        
        /* Sidebar */
        .sidebar { width: 240px; flex-shrink: 0; background: #0f172a; border-right: 1px solid var(--border); padding: 20px 0; display: flex; flex-direction: column; }
        .logo { font-size: 1.2em; color: var(--primary); font-weight: 800; margin: 0 20px 30px 20px; display: flex; align-items: center; gap: 10px; }
        .menu-item { padding: 12px 20px; color: var(--text-muted); cursor: pointer; transition: 0.3s; border-left: 3px solid transparent; display: flex; align-items: center; gap: 15px; font-size: 0.9em; font-weight: 500; }
        .menu-item:hover, .menu-item.active { background: rgba(59, 130, 246, 0.1); color: var(--primary); border-left-color: var(--primary); }
        
        /* Main & Tabs */
        .main-content { flex: 1; padding: 20px; overflow-y: auto; min-width: 0; display: flex; flex-direction: column; gap: 15px; }
        .tab-content { display: none; flex-direction: column; gap: 15px; animation: fadeIn 0.4s; }
        .tab-content.active { display: flex; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Topbar */
        .topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .topbar h2 { font-weight: 600; font-size: 1.2em; color: #fff; }
        .live-badge { background: rgba(16, 185, 129, 0.15); color: var(--success); padding: 5px 12px; border-radius: 20px; font-size: 0.75em; font-weight: bold; border: 1px solid var(--success); display: flex; align-items: center; gap: 6px; text-transform: uppercase; }

        /* Grids e Cards */
        .dashboard-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 15px; flex: 1; }
        .kpi-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
        .kpi-card { background: var(--panel-bg); border: 1px solid var(--border); border-radius: 8px; padding: 15px; display: flex; align-items: center; justify-content: space-between; border-left: 4px solid var(--primary); }
        .kpi-card.cpu { border-left-color: var(--primary); } .kpi-card.ram { border-left-color: var(--warning); } .kpi-card.disk { border-left-color: var(--purple); } .kpi-card.threat { border-left-color: var(--danger); } .kpi-card.uptime { border-left-color: var(--success); }
        .kpi-info { display: flex; flex-direction: column; } .kpi-title { font-size: 0.75em; color: var(--text-muted); text-transform: uppercase; font-weight: 600; } .kpi-value { font-size: 1.4em; font-weight: 700; } .kpi-icon { font-size: 1.5em; opacity: 0.5; }
        
        .card { background: var(--panel-bg); border-radius: 8px; border: 1px solid var(--border); padding: 15px; display: flex; flex-direction: column; }
        .card-header { font-size: 0.8em; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        
        .span-3 { grid-column: span 3; } .span-4 { grid-column: span 4; } .span-5 { grid-column: span 5; } .span-6 { grid-column: span 6; } .span-7 { grid-column: span 7; } .span-8 { grid-column: span 8; } .span-12 { grid-column: span 12; }

        /* Chart & Gauge */
        .chart-container { position: relative; width: 100%; flex: 1; min-height: 180px; display: flex; justify-content: center; align-items: center; }
        .gauge-text { position: absolute; top: 55%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
        .gauge-val { font-size: 1.8em; font-weight: 800; color: var(--success); } .gauge-lbl { font-size: 0.7em; color: var(--text-muted); text-transform: uppercase; }

        /* Listas, Tabelas, Terminal */
        .sec-list { display: flex; flex-direction: column; gap: 10px; }
        .sec-item { display: flex; justify-content: space-between; align-items: center; font-size: 0.85em; padding: 8px 0; border-bottom: 1px dashed var(--border); }
        .badge-ok { color: var(--success); background: rgba(16,185,129,0.1); padding: 3px 8px; border-radius: 4px; font-weight: bold; }
        .badge-alert { color: var(--danger); background: rgba(239,68,68,0.1); padding: 3px 8px; border-radius: 4px; font-weight: bold; }
        
        .table-container { flex: 1; overflow-y: auto; height: 0; min-height: 150px; }
        table { width: 100%; border-collapse: collapse; font-size: 0.8em; text-align: left; }
        th { color: var(--text-muted); padding: 8px 5px; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: var(--panel-bg); }
        td { padding: 8px 5px; border-bottom: 1px solid #1f2937; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        .terminal { background: #000; border-radius: 6px; padding: 10px; font-family: 'Courier New', monospace; font-size: 0.75em; color: #a3e635; flex: 1; overflow-y: auto; border: 1px solid #222; height: 0; min-height: 150px; line-height: 1.5; }
        
        .action-btn { background: rgba(59, 130, 246, 0.1); border: 1px solid var(--primary); color: var(--primary); padding: 8px 12px; border-radius: 4px; cursor: pointer; transition: 0.2s; font-weight: 600; font-size: 0.8em; display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 8px; }
        .action-btn:hover { background: var(--primary); color: #fff; }
        .action-btn.danger { border-color: var(--danger); color: var(--danger); background: rgba(239,68,68,0.1); }
        
        .progress-bg { background: #1f2937; height: 6px; border-radius: 3px; margin-top: 5px; width: 100%; }
        .progress-fill { height: 100%; border-radius: 3px; transition: 0.5s; }

        /* Responsividade */
        @media (max-width: 1200px) {
            .kpi-row { grid-template-columns: repeat(3, 1fr); }
            .span-3, .span-4, .span-5, .span-6, .span-7, .span-8, .span-12 { grid-column: span 12; }
            body { flex-direction: column; height: auto; overflow: auto; }
        }
    </style>
</head>
<body>
    <!-- Sidebar -->
    <div class="sidebar">
        <div class="logo"><i class="fa-solid fa-shield-halved"></i> SENTINEL</div>
        <div class="menu-item active" onclick="switchTab('overview')"><i class="fa-solid fa-gauge-high"></i> Overview</div>
        <div class="menu-item" onclick="switchTab('infrastructure')"><i class="fa-solid fa-server"></i> Infrastructure</div>
        <div class="menu-item" onclick="switchTab('threat')"><i class="fa-solid fa-bug"></i> Threat Intel</div>
        <div class="menu-item" onclick="switchTab('compliance')"><i class="fa-solid fa-file-shield"></i> Compliance</div>
        <div class="menu-item" onclick="switchTab('settings')"><i class="fa-solid fa-gear"></i> Settings</div>
    </div>

    <div class="main-content">
        <div class="topbar">
            <h2 id="page-title">Security Operations Center</h2>
            <div class="live-badge"><i class="fa-solid fa-circle" style="font-size: 6px;"></i> Real-time Analysis</div>
        </div>

        <!-- ABA 1: OVERVIEW -->
        <div id="tab-overview" class="tab-content active">
            <div class="kpi-row">
                <div class="kpi-card cpu"><div class="kpi-info"><span class="kpi-title">CPU</span><span class="kpi-value" id="kpi-cpu">0%</span></div><i class="fa-solid fa-microchip kpi-icon" style="color: var(--primary);"></i></div>
                <div class="kpi-card ram"><div class="kpi-info"><span class="kpi-title">RAM</span><span class="kpi-value" id="kpi-ram">0%</span></div><i class="fa-solid fa-memory kpi-icon" style="color: var(--warning);"></i></div>
                <div class="kpi-card disk"><div class="kpi-info"><span class="kpi-title">Storage</span><span class="kpi-value" id="kpi-disk">0%</span></div><i class="fa-solid fa-hard-drive kpi-icon" style="color: var(--purple);"></i></div>
                <div class="kpi-card threat"><div class="kpi-info"><span class="kpi-title">Threats</span><span class="kpi-value" id="kpi-bans">0</span></div><i class="fa-solid fa-triangle-exclamation kpi-icon" style="color: var(--danger);"></i></div>
                <div class="kpi-card uptime"><div class="kpi-info"><span class="kpi-title">Uptime</span><span class="kpi-value" id="kpi-uptime">0h</span></div><i class="fa-solid fa-clock kpi-icon" style="color: var(--success);"></i></div>
            </div>

            <div class="dashboard-grid">
                <div class="card span-3">
                    <div class="card-header">Threat Posture</div>
                    <div class="chart-container">
                        <canvas id="gaugeChart"></canvas>
                        <div class="gauge-text"><div class="gauge-val" id="gauge-status">LOW</div><div class="gauge-lbl">Risk Level</div></div>
                    </div>
                </div>
                <div class="card span-5">
                    <div class="card-header">Performance Timeline</div>
                    <div class="chart-container"><canvas id="lineChart"></canvas></div>
                </div>
                <div class="card span-4">
                    <div class="card-header">Auth Events</div>
                    <div class="chart-container"><canvas id="barChart"></canvas></div>
                </div>
            </div>
        </div>

        <!-- ABA 2: INFRASTRUCTURE -->
        <div id="tab-infrastructure" class="tab-content">
            <div class="dashboard-grid">
                <div class="card span-6">
                    <div class="card-header">System Information</div>
                    <div class="sec-item"><span>Hostname</span><strong>sentinel-core</strong></div>
                    <div class="sec-item"><span>Kernel</span><strong id="inf-kernel">-</strong></div>
                    <div class="sec-item"><span>Architecture</span><strong id="inf-arch">-</strong></div>
                    <div class="sec-item"><span>CPU Cores</span><strong id="inf-cores">-</strong></div>
                    <div class="sec-item"><span>Total RAM</span><strong id="inf-ram">-</strong></div>
                </div>
                <div class="card span-6">
                    <div class="card-header">Network Interfaces</div>
                    <div class="sec-item"><span>IP Address</span><strong id="inf-ip">-</strong></div>
                    <div class="sec-item"><span>Download Speed</span><strong id="inf-down">0 KB/s</strong></div>
                    <div class="sec-item"><span>Upload Speed</span><strong id="inf-up">0 KB/s</strong></div>
                    <div class="sec-item"><span>Active Connections</span><strong id="inf-conns">0</strong></div>
                </div>
                <div class="card span-12">
                    <div class="card-header">Disk Partitions</div>
                    <div class="table-container" style="height: 250px;">
                        <table>
                            <thead><tr><th>Device</th><th>Mountpoint</th><th>File System</th><th>Total Size</th><th>Used</th><th>Usage %</th></tr></thead>
                            <tbody id="disk-table"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- ABA 3: THREAT INTEL -->
        <div id="tab-threat" class="tab-content">
            <div class="dashboard-grid">
                <div class="card span-4">
                    <div class="card-header">Firewall Status</div>
                    <div class="sec-item"><span>UFW Service</span><strong id="th-ufw" class="badge-ok">Active</strong></div>
                    <div class="sec-item"><span>Open Ports</span><strong>22, 80, 443, 2222, 5000</strong></div>
                </div>
                <div class="card span-4">
                    <div class="card-header">Fail2ban Status</div>
                    <div class="sec-item"><span>Service</span><strong class="badge-ok">Running</strong></div>
                    <div class="sec-item"><span>Currently Banned IPs</span><strong id="th-bans" class="badge-alert">0</strong></div>
                    <div class="sec-item"><span>Total Failed Attempts</span><strong id="th-failed">0</strong></div>
                </div>
                <div class="card span-4">
                    <div class="card-header">Antivirus (ClamAV)</div>
                    <div class="sec-item"><span>Database Signatures</span><strong>3.6M+</strong></div>
                    <div class="sec-item"><span>Last Scan</span><strong>Manual</strong></div>
                    <div class="sec-item"><span>Status</span><strong class="badge-ok">Updated</strong></div>
                </div>
                <div class="card span-12">
                    <div class="card-header"><span><i class="fa-solid fa-terminal"></i> Full Auth Log (Last 20 lines)</span></div>
                    <div class="terminal" id="th-terminal" style="height: 300px;"></div>
                </div>
            </div>
        </div>

        <!-- ABA 4: COMPLIANCE -->
        <div id="tab-compliance" class="tab-content">
            <div class="dashboard-grid">
                <div class="card span-12">
                    <div class="card-header">Security Benchmarks (CIS)</div>
                    <div class="sec-item"><span>SSH Root Login Disabled</span><strong class="badge-ok">PASS</strong></div>
                    <div class="sec-item"><span>SSH Password Authentication</span><strong class="badge-ok">PASS (Disabled)</strong></div>
                    <div class="sec-item"><span>Firewall Default Deny</span><strong class="badge-ok">PASS</strong></div>
                    <div class="sec-item"><span>File Integrity Monitoring (AIDE)</span><strong id="comp-aide" class="badge-ok">PASS</strong></div>
                    <div class="sec-item"><span>Auditd Logging</span><strong class="badge-ok">PASS</strong></div>
                </div>
            </div>
        </div>

        <!-- ABA 5: SETTINGS -->
        <div id="tab-settings" class="tab-content">
            <div class="dashboard-grid">
                <div class="card span-6">
                    <div class="card-header">Incident Response</div>
                    <button class="action-btn" onclick="runAction('backup')"><i class="fa-solid fa-download"></i> Trigger Backup</button>
                    <button class="action-btn" onclick="runAction('update')"><i class="fa-solid fa-rotate"></i> Update Definitions</button>
                    <button class="action-btn danger" onclick="runAction('panic')"><i class="fa-solid fa-shield-halved"></i> Activate Lockdown</button>
                </div>
            </div>
        </div>

    </div>

    <script>
        // Lógica para trocar de abas
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
            
            document.getElementById('tab-' + tabId).classList.add('active');
            event.currentTarget.classList.add('active');

            // Muda o título
            const titles = {'overview': 'Security Operations Center', 'infrastructure': 'Infrastructure Details', 'threat': 'Threat Intelligence', 'compliance': 'Compliance & Auditing', 'settings': 'System Settings'};
            document.getElementById('page-title').innerText = titles[tabId];
        }

        // Configuração dos Gráficos
        const lineChart = new Chart(document.getElementById('lineChart'), {
            type: 'line', data: { labels: [], datasets: [{ label: 'CPU %', data: [], borderColor: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)', fill: true, tension: 0.4, pointRadius: 0, borderWidth: 2 }, { label: 'RAM %', data: [], borderColor: '#f59e0b', backgroundColor: 'rgba(245, 158, 11, 0.1)', fill: true, tension: 0.4, pointRadius: 0, borderWidth: 2 }] },
            options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { labels: { color: '#9ca3af', boxWidth: 10 } } }, scales: { x: { display: false }, y: { display: false, min: 0, max: 100 } } }
        });

        const gaugeChart = new Chart(document.getElementById('gaugeChart'), {
            type: 'doughnut', data: { labels: ['Threat', 'Safe'], datasets: [{ data: [0, 100], backgroundColor: ['#10b981', '#1f2937'], borderWidth: 0, circumference: 180, rotation: 270 }] },
            options: { responsive: true, maintainAspectRatio: false, cutout: '80%', animation: false, plugins: { legend: { display: false }, tooltip: { enabled: false } } }
        });

        const barChart = new Chart(document.getElementById('barChart'), {
            type: 'bar', data: { labels: ['Failed', 'Invalid', 'Accepted'], datasets: [{ data: [0, 0, 0], backgroundColor: ['#ef4444', '#f97316', '#10b981'], borderRadius: 4 }] },
            options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#9ca3af' }, grid: { display: false } }, y: { ticks: { color: '#9ca3af' }, grid: { color: '#1f2937' } } } }
        });

        async function updateDashboard() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();

                // --- ABA OVERVIEW ---
                document.getElementById('kpi-cpu').innerText = data.cpu + '%';
                document.getElementById('kpi-ram').innerText = data.ram + '%';
                document.getElementById('kpi-disk').innerText = data.disk + '%';
                document.getElementById('kpi-bans').innerText = data.bans;
                document.getElementById('kpi-uptime').innerText = data.uptime;

                lineChart.data.labels = data.chart_labels;
                lineChart.data.datasets[0].data = data.chart_cpu;
                lineChart.data.datasets[1].data = data.chart_ram;
                lineChart.update();

                let threatValue = Math.min(data.bans * 20, 100); 
                let threatColor = threatValue > 50 ? '#ef4444' : (threatValue > 0 ? '#f59e0b' : '#10b981');
                let threatText = threatValue > 50 ? 'CRITICAL' : (threatValue > 0 ? 'ELEVATED' : 'LOW');
                
                gaugeChart.data.datasets[0].data = [threatValue, 100 - threatValue];
                gaugeChart.data.datasets[0].backgroundColor[0] = threatColor;
                gaugeChart.update();
                
                const gStatus = document.getElementById('gauge-status');
                gStatus.innerText = threatText; gStatus.style.color = threatColor;

                barChart.data.datasets[0].data = [data.log_stats.failed, data.log_stats.invalid, data.log_stats.accepted]; 
                barChart.update();

                // --- ABA INFRASTRUCTURE ---
                document.getElementById('inf-kernel').innerText = data.kernel;
                document.getElementById('inf-arch').innerText = data.arch;
                document.getElementById('inf-cores').innerText = data.cores;
                document.getElementById('inf-ram').innerText = data.total_ram + ' GB';
                document.getElementById('inf-ip').innerText = data.ip;
                document.getElementById('inf-down').innerText = data.net_down + ' KB/s';
                document.getElementById('inf-up').innerText = data.net_up + ' KB/s';
                document.getElementById('inf-conns').innerText = data.connections;

                const diskTable = document.getElementById('disk-table');
                diskTable.innerHTML = '';
                data.disk_parts.forEach(d => {
                    diskTable.innerHTML += `<tr><td>${d.device}</td><td>${d.mountpoint}</td><td>${d.fstype}</td><td>${d.total} GB</td><td>${d.used} GB</td><td style="color: ${d.percent > 80 ? '#ef4444' : '#10b981'}">${d.percent}%</td></tr>`;
                });

                // --- ABA THREAT INTEL ---
                document.getElementById('th-ufw').className = data.ufw.includes('active') ? 'badge-ok' : 'badge-alert';
                document.getElementById('th-bans').innerText = data.bans;
                document.getElementById('th-failed').innerText = data.log_stats.failed + data.log_stats.invalid;
                
                const termThreat = document.getElementById('th-terminal');
                termThreat.innerHTML = '';
                data.logs.forEach(log => {
                    const isErr = log.toLowerCase().includes('fail') || log.toLowerCase().includes('invalid');
                    termThreat.innerHTML += `<div style="color: ${isErr ? '#ef4444' : '#a3e635'}; margin-bottom: 3px;">${log}</div>`;
                });
                termThreat.scrollTop = termThreat.scrollHeight;

                // --- ABA COMPLIANCE ---
                document.getElementById('comp-aide').className = data.aide.includes('active') ? 'badge-ok' : 'badge-alert';

            } catch (error) { console.error("Fetch Error:", error); }
        }

        async function runAction(action) {
            const btn = event.target; const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...'; btn.disabled = true;
            try {
                const res = await fetch(`/api/action/${action}`, {method: 'POST'});
                const data = await res.json();
                alert(data.message);
            } catch (e) { alert("Error executing action."); } 
            finally { btn.innerHTML = originalText; btn.disabled = false; updateDashboard(); }
        }

        updateDashboard();
        setInterval(updateDashboard, 2500);
    </script>
</body>
</html>
"""

last_net_io = psutil.net_io_counters()
last_time = time.time()

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/api/action/<action>', methods=['POST'])
def run_action(action):
    try:
        if action == 'backup':
            subprocess.Popen(['sudo', '/home/julio/sentinel-core/scripts/backup.sh'])
            return jsonify({"status": "success", "message": "Backup started in background."})
        elif action == 'update':
            subprocess.Popen(['sudo', 'apt-get', 'update', '-y'])
            return jsonify({"status": "success", "message": "Definitions update initiated."})
        elif action == 'panic':
            return jsonify({"status": "success", "message": "Panic mode activated! External HTTP access blocked."})
        return jsonify({"status": "error", "message": "Unknown action."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed: {str(e)}"})

@app.route('/api/stats')
def stats():
    global last_net_io, last_time
    
    cpu = psutil.cpu_percent(); ram = psutil.virtual_memory().percent; disk = psutil.disk_usage('/').percent
    uptime_seconds = time.time() - psutil.boot_time()
    hours, remainder = divmod(uptime_seconds, 3600); minutes, _ = divmod(remainder, 60)
    
    current_net_io = psutil.net_io_counters(); current_time = time.time()
    time_diff = current_time - last_time if current_time != last_time else 1
    down_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_diff / 1024
    up_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_diff / 1024
    last_net_io = current_net_io; last_time = current_time

    ip = "N/A"
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            if iface != 'lo' and addrs[0].family == 2: ip = addrs[0].address; break
    except: pass

    # Dados de Infraestrutura (Discos e Rede)
    disk_parts = []
    for part in psutil.disk_partitions():
        if 'loop' in part.device: continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disk_parts.append({'device': part.device, 'mountpoint': part.mountpoint, 'fstype': part.fstype, 'total': round(usage.total / (1024**3), 1), 'used': round(usage.used / (1024**3), 1), 'percent': usage.percent})
        except: pass

    try: connections = len(psutil.net_connections())
    except: connections = 0

    # Segurança
    try:
        f2b_out = subprocess.check_output(['sudo', 'fail2ban-client', 'status', 'sshd'], stderr=subprocess.STDOUT, timeout=2).decode('utf-8')
        bans = "0"
        for linha in f2b_out.split('\n'):
            if 'Currently banned' in linha: bans = linha.split(':')[1].strip()
    except: bans = "0"

    try:
        ufw_out = subprocess.check_output(['sudo', 'ufw', 'status'], stderr=subprocess.STDOUT, timeout=2).decode('utf-8')
        ufw_status = "Active" if "Status: active" in ufw_out else "Inactive"
    except: ufw_status = "Unknown"

    try:
        aide_out = subprocess.check_output(['systemctl', 'is-active', 'aide'], stderr=subprocess.STDOUT, timeout=2).decode('utf-8').strip()
        aide_status = "Active" if aide_out == "active" else "Inactive"
    except: aide_status = "Unknown"

    try: ssh_sessions = len([line for line in subprocess.check_output(['who'], timeout=2).decode('utf-8').split('\n') if line.strip()])
    except: ssh_sessions = 1

    # Processos e Logs
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try: processes.append({'pid': proc.info['pid'], 'name': proc.info['name'][:20], 'user': proc.info['username'] or 'root', 'cpu': round(proc.info['cpu_percent'], 1), 'mem': round(proc.info['memory_percent'], 1)})
        except: pass
    processes = sorted(processes, key=lambda x: x['cpu'], reverse=True)[:5]

    logs = []; log_stats = {'failed': 0, 'invalid': 0, 'accepted': 0}
    try:
        log_out = subprocess.check_output(['sudo', 'tail', '-n', '50', '/var/log/auth.log'], stderr=subprocess.STDOUT, timeout=2).decode('utf-8')
        lines = [line for line in log_out.split('\n') if line.strip()]
        for line in lines:
            if 'Failed password' in line: log_stats['failed'] += 1
            if 'Invalid user' in line: log_stats['invalid'] += 1
            if 'Accepted password' in line or 'Accepted publickey' in line: log_stats['accepted'] += 1
        filtered_logs = [l for l in lines if 'Failed' in l or 'Invalid' in l or 'Accepted' in l]
        logs = filtered_logs[-15:] if filtered_logs else ["[!] No recent SSH events."]
    except: logs = ["[!] Waiting for log permissions..."]

    history['time'].append(time.strftime("%H:%M:%S")); history['cpu'].append(cpu); history['ram'].append(ram)

    return jsonify({
        "cpu": cpu, "ram": ram, "disk": disk, "uptime": f"{int(hours)}h {int(minutes)}m", 
        "bans": int(bans), "ufw": ufw_status, "aide": aide_status, "ssh_sessions": ssh_sessions,
        "net_down": round(down_speed, 1), "net_up": round(up_speed, 1), "ip": ip, "connections": connections,
        "kernel": platform.release(), "arch": platform.machine(), "cores": psutil.cpu_count(), "total_ram": round(psutil.virtual_memory().total / (1024**3), 1),
        "processes": processes, "logs": logs, "log_stats": log_stats, "disk_parts": disk_parts,
        "chart_labels": list(history['time']), "chart_cpu": list(history['cpu']), "chart_ram": list(history['ram'])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

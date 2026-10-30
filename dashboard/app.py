<!DOCTYPE html>
<html>
<head>
    <title>Sentinel Core - Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #fff; text-align: center; padding: 20px; }
        .container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }
        .card { background: #1e293b; padding: 20px; border-radius: 12px; width: 250px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h1 { color: #38bdf8; }
        canvas { max-width: 100%; }
    </style>
</head>
<body>
    <h1>🛡️ Sentinel Core Monitor</h1>
    <p>Status do Servidor em Tempo Real</p>
    <div class="container">
        <div class="card">
            <h3>CPU</h3>
            <canvas id="cpuChart"></canvas>
            <h2>{{ cpu }}%</h2>
        </div>
        <div class="card">
            <h3>RAM</h3>
            <canvas id="ramChart"></canvas>
            <h2>{{ ram }}%</h2>
        </div>
        <div class="card">
            <h3>Disco</h3>
            <canvas id="diskChart"></canvas>
            <h2>{{ disk }}%</h2>
        </div>
    </div>

    <script>
        function createChart(id, value, color) {
            new Chart(document.getElementById(id), {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [value, 100 - value],
                        backgroundColor: [color, '#334155'],
                        borderWidth: 0
                    }]
                },
                options: { cutout: '75%', plugins: { legend: { display: false } } }
            });
        }
        createChart('cpuChart', {{ cpu }}, '#38bdf8');
        createChart('ramChart', {{ ram }}, '#fbbf24');
        createChart('diskChart', {{ disk }}, '#f87171');
    </script>
</body>
</html>b
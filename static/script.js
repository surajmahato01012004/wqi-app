const ctx = document.getElementById('wqiChart').getContext('2d');

let wqiChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Current Score', 'Remaining'],
        datasets: [{
            data: [0, 150],
            backgroundColor: ['#e9ecef', '#e9ecef'],
            borderWidth: 0
        }]
    },
    options: {
        rotation: -90,
        circumference: 180,
        cutout: '70%',
        plugins: {
            legend: { display: false },
            tooltip: { enabled: false }
        }
    }
});

const wqiForm = document.getElementById('wqiForm');

wqiForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    const data = {
        ph: document.getElementById('ph').value,
        do: document.getElementById('do').value,
        turbidity: document.getElementById('turbidity').value,
        tds: document.getElementById('tds').value,
        nitrate: document.getElementById('nitrate').value
    };

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        document.getElementById('scoreDisplay').innerText = result.wqi;

        const statusBadge = document.getElementById('statusBadge');
        statusBadge.innerText = result.status;
        statusBadge.className = `badge fs-4 px-4 py-2 bg-${result.color}`;

        if (result.color === 'orange') {
            statusBadge.style.backgroundColor = '#fd7e14';
            statusBadge.style.color = '#fff';
        } else {
            statusBadge.style.backgroundColor = '';
            statusBadge.style.color = '';
        }

        let chartColor;
        if (result.wqi < 25) chartColor = '#28a745';
        else if (result.wqi < 50) chartColor = '#17a2b8';
        else if (result.wqi < 75) chartColor = '#ffc107';
        else if (result.wqi < 100) chartColor = '#fd7e14';
        else chartColor = '#343a40';

        wqiChart.data.datasets[0].data = [result.wqi, Math.max(0, 150 - result.wqi)];
        wqiChart.data.datasets[0].backgroundColor = [chartColor, '#e9ecef'];
        wqiChart.update();

    } catch (err) {
        console.error(err);
        alert("Server error!");
    }
});

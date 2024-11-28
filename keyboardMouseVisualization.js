// Initialize Chart.js
const combinedCanvas = document.getElementById("combinedActivityChart").getContext("2d");
const combinedActivityChart = new Chart(combinedCanvas, {
    type: "line",
    data: {
        labels: [], // Time labels
        datasets: [
            {
                label: "Keyboard Presses",
                data: [],
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                tension: 0.3,
                fill: true,
            },
            {
                label: "Mouse Movements",
                data: [],
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                tension: 0.3,
                fill: true,
            },
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: "Time",
                },
            },
            y: {
                title: {
                    display: true,
                    text: "Activity Count",
                },
                beginAtZero: true,
            },
        },
    },
});

// Update the chart every second
setInterval(() => {
    const timeline = combinedActivityData.timeline;
    const labels = timeline.map((entry) => entry.time);
    const keyboardData = timeline.map((entry) => entry.keyboard);
    const mouseData = timeline.map((entry) => entry.mouse);

    combinedActivityChart.data.labels = labels;
    combinedActivityChart.data.datasets[0].data = keyboardData;
    combinedActivityChart.data.datasets[1].data = mouseData;

    combinedActivityChart.update();
}, 1000); // Update every second

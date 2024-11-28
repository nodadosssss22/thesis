// Initialize bar chart for event counts
const mouseBarCanvas = document.getElementById("mouseEventChart").getContext("2d");
const mouseEventChart = new Chart(mouseBarCanvas, {
    type: "bar",
    data: {
        labels: ["Movements", "Left Clicks", "Right Clicks", "Dragging", "Scrolling"],
        datasets: [
            {
                label: "Mouse Events",
                data: [0, 0, 0, 0, 0],
                backgroundColor: [
                    "rgba(75, 192, 192, 0.6)",
                    "rgba(54, 162, 235, 0.6)",
                    "rgba(255, 99, 132, 0.6)",
                    "rgba(255, 206, 86, 0.6)",
                    "rgba(153, 102, 255, 0.6)",
                ],
                borderColor: [
                    "rgba(75, 192, 192, 1)",
                    "rgba(54, 162, 235, 1)",
                    "rgba(255, 99, 132, 1)",
                    "rgba(255, 206, 86, 1)",
                    "rgba(153, 102, 255, 1)",
                ],
                borderWidth: 1,
            },
        ],
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Event Count",
                },
            },
        },
    },
});

// Update bar chart every second
setInterval(() => {
    const { movements, leftClicks, rightClicks, dragging, scrolling } = mouseActivityData;

    mouseEventChart.data.datasets[0].data = [movements, leftClicks, rightClicks, dragging, scrolling];
    mouseEventChart.update();
}, 1000);
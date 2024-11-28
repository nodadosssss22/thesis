// Get the canvas element for keyboard visualization
const keyboardCtx = document.getElementById("keyboardChart").getContext("2d");

// Initialize dataset for keyboard activity
const keyboardData = {
    labels: [], // Key names
    datasets: [
        {
            label: "Key Press Frequency",
            data: [], // Frequency of key presses
            backgroundColor: [],
            borderColor: [],
            borderWidth: 1,
        },
    ],
};

// Create the bar chart
const keyboardChart = new Chart(keyboardCtx, {
    type: "bar",
    data: keyboardData,
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: "Keys",
                },
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Frequency",
                },
            },
        },
        plugins: {
            legend: {
                display: true,
            },
        },
        animation: {
            duration: 500,
            easing: "easeOutBounce",
        },
    },
});

// Function to update chart data dynamically
function updateKeyboardChart(key, frequency) {
    const index = keyboardData.labels.indexOf(key);

    if (index === -1) {
        // Add new key to the chart
        keyboardData.labels.push(key);
        keyboardData.datasets[0].data.push(frequency);
        keyboardData.datasets[0].backgroundColor.push(getRandomColor());
        keyboardData.datasets[0].borderColor.push("rgba(0, 0, 0, 0.1)");
    } else {
        // Update frequency of existing key
        keyboardData.datasets[0].data[index] = frequency;
    }

    // Sort the chart by frequency (highest to lowest)
    const sortedIndices = keyboardData.datasets[0].data
        .map((value, i) => [i, value])
        .sort((a, b) => b[1] - a[1])
        .map((pair) => pair[0]);

    keyboardData.labels = sortedIndices.map((i) => keyboardData.labels[i]);
    keyboardData.datasets[0].data = sortedIndices.map((i) => keyboardData.datasets[0].data[i]);
    keyboardData.datasets[0].backgroundColor = sortedIndices.map(
        (i) => keyboardData.datasets[0].backgroundColor[i]
    );
    keyboardData.datasets[0].borderColor = sortedIndices.map(
        (i) => keyboardData.datasets[0].borderColor[i]
    );

    keyboardChart.update();
}

// Function to generate random colors for bars
function getRandomColor() {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return `rgba(${r}, ${g}, ${b}, 0.7)`;
}

// Periodically update the chart with data from monitor.js
setInterval(() => {
    if (typeof keyPressData !== "undefined") {
        for (const key in keyPressData) {
            updateKeyboardChart(key, keyPressData[key]);
        }
    }
}, 1000); // Update every second

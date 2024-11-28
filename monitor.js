// Data structure to store keyboard activity
const keyPressData = {};

// Mouse activity data
const mouseActivityData = {
    movements: 0,
    leftClicks: 0,
    rightClicks: 0,
    dragging: 0,
    scrolling: 0,
    timeline: [], // Stores activity per second
    isDragging: false,
};

// Track mouse movement
document.addEventListener("mousemove", () => {
    mouseActivityData.movements++;
    if (mouseActivityData.isDragging) mouseActivityData.dragging++;
});

// Track mouse clicks
document.addEventListener("mousedown", (e) => {
    if (e.button === 0) mouseActivityData.leftClicks++; // Left-click
    if (e.button === 2) mouseActivityData.rightClicks++; // Right-click
    if (e.button === 0) mouseActivityData.isDragging = true; // Start drag
});

// Track mouse release
document.addEventListener("mouseup", (e) => {
    if (e.button === 0) mouseActivityData.isDragging = false; // End drag
});

// Track mouse scrolling
document.addEventListener("wheel", () => {
    mouseActivityData.scrolling++;
});

// Record activity over time
setInterval(() => {
    const timestamp = new Date().toLocaleTimeString();

    // Push the current activity into the timeline
    mouseActivityData.timeline.push({
        time: timestamp,
        movements: mouseActivityData.movements,
        leftClicks: mouseActivityData.leftClicks,
        rightClicks: mouseActivityData.rightClicks,
        dragging: mouseActivityData.dragging,
        scrolling: mouseActivityData.scrolling,
    });

    // Reset counters for the next interval
    mouseActivityData.movements = 0;
    mouseActivityData.leftClicks = 0;
    mouseActivityData.rightClicks = 0;
    mouseActivityData.dragging = 0;
    mouseActivityData.scrolling = 0;

    // Keep only the last 60 seconds of data
    if (mouseActivityData.timeline.length > 60) {
        mouseActivityData.timeline.shift();
    }
}, 1000); // Update every second

// Function to handle inactivity tracking
let inactivityStartTime = null;
let totalInactiveTime = 0;

function handleInactivity() {
    if (!inactivityStartTime) {
        inactivityStartTime = Date.now(); // Record the start of inactivity
    }
}

// Function to reset inactivity tracking
function resetInactivity() {
    if (inactivityStartTime) {
        const inactiveDuration = Date.now() - inactivityStartTime;
        totalInactiveTime += inactiveDuration; // Add to total inactivity
        inactivityStartTime = null; // Reset inactivity timer
    }
}

// Function to get total inactive time broken down
function getInactiveTimeBreakdown() {
    const hours = Math.floor(totalInactiveTime / 3600000);
    const minutes = Math.floor((totalInactiveTime % 3600000) / 60000);
    const seconds = Math.floor((totalInactiveTime % 60000) / 1000);
    const milliseconds = totalInactiveTime % 1000;

    return { hours, minutes, seconds, milliseconds };
}

// Combined Activity Data
const combinedActivityData = {
    keyboardPresses: 0,
    mouseMovements: 0,
    timeline: [], // Stores activity per second
};

// Track keyboard activity
document.addEventListener("keydown", (e) => {
    combinedActivityData.keyboardPresses++;
});

// Track mouse movement activity
document.addEventListener("mousemove", (e) => {
    combinedActivityData.mouseMovements++;
});

// Record activity over time
setInterval(() => {
    const timestamp = new Date().toLocaleTimeString();

    // Push the current activity into the timeline
    combinedActivityData.timeline.push({
        time: timestamp,
        keyboard: combinedActivityData.keyboardPresses,
        mouse: combinedActivityData.mouseMovements,
    });

    // Reset counters for the next interval
    combinedActivityData.keyboardPresses = 0;
    combinedActivityData.mouseMovements = 0;

    // Keep only the last 60 seconds of data
    if (combinedActivityData.timeline.length > 60) {
        combinedActivityData.timeline.shift();
    }
}, 1000); // Update every second

// Function to update the activity summary
function updateActivitySummary() {
    // Keyboard Summary
    const keyboardSummaryDiv = document.getElementById("keyboard-summary");
    keyboardSummaryDiv.innerHTML = "<h3>Keyboard Activity</h3>";
    const sortedKeys = Object.entries(keyPressData)
        .sort(([, a], [, b]) => b - a)
        .map(([key, count]) => `<p>${key}: ${count} times</p>`)
        .join("");
    keyboardSummaryDiv.innerHTML += sortedKeys || "<p>No keyboard activity recorded.</p>";

    // Mouse Summary
    const mouseSummaryDiv = document.getElementById("mouse-summary");
    mouseSummaryDiv.innerHTML = `<h3>Mouse Activity</h3>
        <p>Movements: ${mouseActivityData.movements}</p>
        <p>Left Clicks: ${mouseActivityData.leftClicks}</p>
        <p>Right Clicks: ${mouseActivityData.rightClicks}</p>
        <p>Dragging: ${mouseActivityData.dragging}</p>
        <p>Scrolling: ${mouseActivityData.scrolling}</p>`;

    // Combined Summary
    const combinedSummaryDiv = document.getElementById("combined-summary");
    const totalKeyboardPresses = combinedActivityData.timeline.reduce((sum, entry) => sum + entry.keyboard, 0);
    const totalMouseMovements = combinedActivityData.timeline.reduce((sum, entry) => sum + entry.mouse, 0);
    combinedSummaryDiv.innerHTML = `<h3>Combined Activity</h3>
        <p>Total Keyboard Presses: ${totalKeyboardPresses}</p>
        <p>Total Mouse Movements: ${totalMouseMovements}</p>`;

    // Inactivity Summary
    const inactivitySummaryDiv = document.getElementById("inactivity-summary");
    const { hours, minutes, seconds, milliseconds } = getInactiveTimeBreakdown();
    inactivitySummaryDiv.innerHTML = `<h3>Inactivity Summary</h3>
        <p>Total Inactive Time: ${hours} hours, ${minutes} minutes, ${seconds} seconds, ${milliseconds} ms</p>`;
}

// Update the summary every 2 seconds
setInterval(updateActivitySummary, 2000);

// Event Listeners for inactivity tracking
window.addEventListener("blur", handleInactivity); // User loses focus
window.addEventListener("focus", resetInactivity); // User regains focus

// ================================
// SignalSense Dashboard
// ================================

let predictionChart;

// -------------------------------
// Animated Counter
// -------------------------------

function animateValue(id, start, end, duration) {

    const element = document.getElementById(id);

    let startTime = null;

    function animation(currentTime) {

        if (!startTime) startTime = currentTime;

        const progress = Math.min((currentTime - startTime) / duration, 1);

        const value = Math.floor(progress * (end - start) + start);

        element.innerText = value;

        if (progress < 1) {
            requestAnimationFrame(animation);
        }

    }

    requestAnimationFrame(animation);

}

// -------------------------------
// Live Clock
// -------------------------------

function updateClock() {

    const now = new Date();

    const options = {
        weekday: "long",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    };

    document.getElementById("liveTime").innerText =
        now.toLocaleString("en-US", options);

}

setInterval(updateClock, 1000);

updateClock();

// -------------------------------
// Doughnut Chart
// -------------------------------

function createChart(normal, anomaly) {

    const ctx = document
        .getElementById("predictionChart")
        .getContext("2d");

    if (predictionChart) {
        predictionChart.destroy();
    }

    predictionChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: ["Normal", "Anomaly"],

            datasets: [{

                data: [normal, anomaly],

                backgroundColor: [

                    "#22c55e",

                    "#ef4444"

                ],

                borderWidth: 0

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "65%",

            plugins: {

                legend: {

                    labels: {

                        color: "white",

                        font: {

                            size: 14

                        }

                    }

                }

            }

        }

    });

}

// -------------------------------
// Dashboard Data
// -------------------------------

function loadDashboard() {

    fetch("/dashboard-data")

    .then(res => res.json())

    .then(data => {

        if (!data.success) return;

        animateValue(
            "totalPredictions",
            0,
            data.total,
            800
        );

        animateValue(
            "normalCount",
            0,
            data.normal,
            800
        );

        animateValue(
            "anomalyCount",
            0,
            data.anomalies,
            800
        );

        let accuracy = 0;

        if (data.total > 0) {

            accuracy = (
                data.normal /
                data.total *
                100
            ).toFixed(1);

        }

        document.getElementById("accuracy").innerText =
            accuracy + "%";

        createChart(
            data.normal,
            data.anomalies
        );

    })

    .catch(error => {

        console.log(error);

    });

}

// -------------------------------
// Auto Refresh
// -------------------------------

loadDashboard();

setInterval(loadDashboard, 5000);

// -------------------------------
// Card Hover Effect
// -------------------------------

document.querySelectorAll(".card").forEach(card => {

    card.addEventListener("mousemove", () => {

        card.style.transform = "translateY(-8px) scale(1.02)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "";

    });

});
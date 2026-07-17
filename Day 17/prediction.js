const predictionForm = document.getElementById("predictionForm");

predictionForm.addEventListener("submit", async function (e) {

    e.preventDefault();

    const device_id = document.getElementById("device_id").value.trim();

    const temperature = document.getElementById("temperature").value;

    const humidity = document.getElementById("humidity").value;

    const battery_level = document.getElementById("battery_level").value;

    if (
        device_id === "" ||
        temperature === "" ||
        humidity === "" ||
        battery_level === ""
    ) {

        alert("Please fill all fields.");

        return;

    }

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                device_id: device_id,

                temperature: temperature,

                humidity: humidity,

                battery_level: battery_level

            })

        });

        const result = await response.json();

        if (result.success) {

            document.getElementById("deviceResult").innerHTML =
                result.device_id;

            document.getElementById("predictionResult").innerHTML =
                result.prediction;

            document.getElementById("confidenceResult").innerHTML =
                result.confidence + " %";

            // Change prediction color

            if (result.prediction === "Normal") {

                document.getElementById("predictionResult").style.color =
                    "#22c55e";

            }

            else {

                document.getElementById("predictionResult").style.color =
                    "#ef4444";

            }

        }

        else {

            alert(result.message);

        }

    }

    catch (error) {

        console.log(error);

        alert("Unable to connect to the server.");

    }

});
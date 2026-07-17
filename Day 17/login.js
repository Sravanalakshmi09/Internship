const loginForm = document.getElementById("loginForm");

const message = document.getElementById("message");

loginForm.addEventListener("submit", async function (e) {

    e.preventDefault();

    const email = document.getElementById("email").value.trim();

    const password = document.getElementById("password").value.trim();

    if (email === "" || password === "") {

        message.style.color = "#ef4444";

        message.innerHTML = "Please fill all fields.";

        return;

    }

    try {

        const response = await fetch("/login", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email: email,

                password: password

            })

        });

        const result = await response.json();

        if (result.success) {

            message.style.color = "#22c55e";

            message.innerHTML = result.message;

            setTimeout(function () {

                window.location.href = "/dashboard";

            }, 1000);

        } else {

            message.style.color = "#ef4444";

            message.innerHTML = result.message;

        }

    } catch (error) {

        message.style.color = "#ef4444";

        message.innerHTML = "Server connection failed.";

        console.error(error);

    }

});
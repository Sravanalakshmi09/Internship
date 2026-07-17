const registerForm = document.getElementById("registerForm");

const message = document.getElementById("message");

registerForm.addEventListener("submit", async function (e) {

    e.preventDefault();

    const fullname = document.getElementById("fullname").value.trim();

    const email = document.getElementById("email").value.trim();

    const password = document.getElementById("password").value;

    const confirmPassword = document.getElementById("confirmPassword").value;

    // Validation

    if (
        fullname === "" ||
        email === "" ||
        password === "" ||
        confirmPassword === ""
    ) {

        message.style.color = "#ef4444";

        message.innerHTML = "Please fill all fields.";

        return;

    }

    if (password.length < 6) {

        message.style.color = "#ef4444";

        message.innerHTML = "Password must be at least 6 characters.";

        return;

    }

    if (password !== confirmPassword) {

        message.style.color = "#ef4444";

        message.innerHTML = "Passwords do not match.";

        return;

    }

    try {

        const response = await fetch("/register", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                fullname: fullname,

                email: email,

                password: password

            })

        });

        const result = await response.json();

        if (result.success) {

            message.style.color = "#22c55e";

            message.innerHTML = result.message;

            setTimeout(function () {

                window.location.href = "/";

            }, 1500);

        } else {

            message.style.color = "#ef4444";

            message.innerHTML = result.message;

        }

    } catch (error) {

        console.log(error);

        message.style.color = "#ef4444";

        message.innerHTML = "Server connection failed.";

    }

});
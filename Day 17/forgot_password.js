const sendOtpBtn = document.getElementById("sendOtpBtn");

const forgotForm = document.getElementById("forgotForm");

const message = document.getElementById("message");

// ----------------------------
// Send OTP
// ----------------------------

sendOtpBtn.addEventListener("click", async () => {

    const email = document.getElementById("email").value.trim();

    if (email === "") {

        message.style.color = "#ef4444";
        message.innerHTML = "Please enter your email.";

        return;
    }

    try {

        const response = await fetch("/forgot-password", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email: email

            })

        });

        const result = await response.json();

        if (result.success) {

            message.style.color = "#22c55e";

            message.innerHTML = "OTP has been sent to your email.";

        }

        else {

            message.style.color = "#ef4444";

            message.innerHTML = result.message;

        }

    }

    catch (error) {

        console.log(error);

        message.style.color = "#ef4444";

        message.innerHTML = "Unable to connect to the server.";

    }

});


// ----------------------------
// Reset Password
// ----------------------------

forgotForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    const email = document.getElementById("email").value.trim();

    const otp = document.getElementById("otp").value.trim();

    const password = document.getElementById("password").value;

    const confirmPassword = document.getElementById("confirmPassword").value;

    if (

        email === "" ||

        otp === "" ||

        password === "" ||

        confirmPassword === ""

    ) {

        message.style.color = "#ef4444";

        message.innerHTML = "Please fill all fields.";

        return;

    }

    if (password !== confirmPassword) {

        message.style.color = "#ef4444";

        message.innerHTML = "Passwords do not match.";

        return;

    }

    if (password.length < 6) {

        message.style.color = "#ef4444";

        message.innerHTML = "Password must be at least 6 characters.";

        return;

    }

    try {

        const response = await fetch("/reset-password", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email: email,

                otp: otp,

                password: password

            })

        });

        const result = await response.json();

        if (result.success) {

            message.style.color = "#22c55e";

            message.innerHTML = "Password reset successful! Redirecting...";

            setTimeout(() => {

                window.location.href = "/";

            }, 2000);

        }

        else {

            message.style.color = "#ef4444";

            message.innerHTML = result.message;

        }

    }

    catch (error) {

        console.log(error);

        message.style.color = "#ef4444";

        message.innerHTML = "Server connection failed.";

    }

});
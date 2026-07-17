const form = document.getElementById("profileForm");

const message = document.getElementById("message");

const imageInput = document.getElementById("profilePic");

const preview = document.getElementById("profilePreview");

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if(file){

        preview.src = URL.createObjectURL(file);

    }

});

form.addEventListener("submit", async function(e){

    e.preventDefault();

    const name=document.getElementById("name").value;

    const password=document.getElementById("password").value;

    const confirm=document.getElementById("confirmPassword").value;

    if(password!==confirm){

        message.style.color="red";

        message.innerHTML="Passwords do not match.";

        return;

    }

    const response=await fetch("/update-profile",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            name:name,

            password:password

        })

    });

    const result=await response.json();

    if(result.success){

        message.style.color="lime";

        message.innerHTML="Profile Updated Successfully";

    }

    else{

        message.style.color="red";

        message.innerHTML=result.message;

    }

});
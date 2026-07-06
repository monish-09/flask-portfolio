function showMessage(message){

    document.getElementById("fullMessage").innerText = message;

    document.getElementById("messageModal").style.display = "block";

}

function closeModal(){

    document.getElementById("messageModal").style.display = "none";

}

window.onclick = function(event){

    const modal = document.getElementById("messageModal");

    if(event.target == modal){

        modal.style.display = "none";

    }

}

function togglePassword(inputId, icon){

    const input = document.getElementById(inputId);
    const eye = icon.querySelector("i");

    if(input.type === "password"){

        input.type = "text";
        eye.classList.remove("fa-eye");
        eye.classList.add("fa-eye-slash");

    }else{

        input.type = "password";
        eye.classList.remove("fa-eye-slash");
        eye.classList.add("fa-eye");

    }

}
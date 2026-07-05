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
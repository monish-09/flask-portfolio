const words = [
    "Python Developer",
    "Flask Developer",
    "Data Science Learner",
    "Final Year CSE Student"
];

let wordIndex = 0;
let charIndex = 0;
let currentWord = "";
let isDeleting = false;

function typeEffect(){

    currentWord = words[wordIndex];

    if(!isDeleting){

        document.getElementById("typing").textContent =
        currentWord.substring(0,charIndex++);

        if(charIndex > currentWord.length){
            isDeleting = true;
            setTimeout(typeEffect,1200);
            return;
        }

    }else{

        document.getElementById("typing").textContent =
        currentWord.substring(0,charIndex--);

        if(charIndex < 0){
            isDeleting = false;
            wordIndex = (wordIndex+1)%words.length;
        }

    }

    setTimeout(typeEffect,isDeleting ? 60 : 120);
}

typeEffect();

const menu = document.querySelector(".menu-toggle");
const nav = document.querySelector(".nav-links");

if (menu && nav) {
    menu.addEventListener("click", () => {
        nav.classList.toggle("active");
    });
}
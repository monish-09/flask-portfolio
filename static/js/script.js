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

// =======================
// Dark / Light Mode
// =======================

const themeToggle = document.getElementById("theme-toggle");
const themeIcon = themeToggle.querySelector("i");

// Saved theme
if (localStorage.getItem("theme") === "light") {

    document.body.classList.add("light-theme");

    themeIcon.classList.remove("fa-moon");
    themeIcon.classList.add("fa-sun");

}

themeToggle.addEventListener("click", () => {

    document.body.classList.toggle("light-theme");

    if(document.body.classList.contains("light-theme")){

        localStorage.setItem("theme","light");

        themeIcon.classList.remove("fa-moon");
        themeIcon.classList.add("fa-sun");

    }else{

        localStorage.setItem("theme","dark");

        themeIcon.classList.remove("fa-sun");
        themeIcon.classList.add("fa-moon");

    }

});
document.addEventListener("DOMContentLoaded", () => {

const toggle = document.getElementById("themeToggle")

// apply saved theme
if(localStorage.getItem("theme")==="light"){
document.body.classList.add("light")
}

if(toggle){

toggle.addEventListener("click", () => {

document.body.classList.toggle("light")

if(document.body.classList.contains("light")){
localStorage.setItem("theme","light")
toggle.textContent="☀️"
}else{
localStorage.setItem("theme","dark")
toggle.textContent="🌙"
}

})

}

})
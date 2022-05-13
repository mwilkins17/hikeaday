document.getElementById('map--btn').addEventListener('click', ()=>{
    document.getElementById("state--search--div").style.display = "none";
    document.getElementById("map").style.display = "";
})

document.getElementById('list--btn').addEventListener('click', ()=>{
    document.getElementById("map").style.display = "none";
    document.getElementById("state--search--div").style.display = "";
})


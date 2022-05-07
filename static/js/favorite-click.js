
fetch('/is-favorite')
.then(response => response.json())
.then(currentFavorite => {
    let fav_check = currentFavorite.favorited
    let starIcon = fav_check ? "star-filled.png" : "star-empty.png";

    document.getElementById('favorite').innerHTML= `
        <div>
        <img id="favorite-icon"
        src="../static/img/${starIcon}" 
        className="favorite"
        onClick={toggleFavorite}
        />
        </div>
        `
});



function toggleFavorite() {
    fetch('/update-favorite')
    .then(response => response.json())
    .then(currentFavorite => {
    let fav_check = currentFavorite.fav;
    let starIcon = fav_check ? "star-filled.png" : "star-empty.png";

    document.getElementById('favorite').innerHTML= `
    <div>
    <img id="favorite-icon"
    src="../static/img/${starIcon}" 
    className="favorite"
    onClick={toggleFavorite}
    />
    </div>
    `

    });
    
}

document.getElementById('favorite').addEventListener("click", toggleFavorite);

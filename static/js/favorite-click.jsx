// document.getElementById("favorite").addEventListener("click", ()=>

// )

// function Favorite() {

// }

import React from "react"
import ReactDOM from "react-dom"


export default function Favorite() {
    const [favorite, setFavorite] = React.useState({
        isFavorite: false
    })
    
    let starIcon = contact.isFavorite ? "star-filled.png" : "star-empty.png"
    
    function toggleFavorite() {
        setFavorite(prevFavorite => ({
            ...prevFavorite,
            isFavorite: !prevFavorite.isFavorite
        }))
    }

    return (
        <div>
            <img src="../static/img/star-empty.png"></img>
                    <img id={starIcon}
                        src={`../static/img/${starIcon}`} 
                        className="favorite"
                        onClick={toggleFavorite}
                    />
        </div>
    )
}

ReactDOM.render(<Favorite />, document.getElementById("favorite"))
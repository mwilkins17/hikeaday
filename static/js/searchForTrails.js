document.getElementById('state--searching--form').addEventListener('submit', () => {

    
    document.getElementById('state--trails--div').innerHTML = "";

    fetch('/trails/all-state')
        .then((response) => response.json())
        .then((trails) => {
        for (const trail of trails)
        document.getElementById('state--trails--div').insertAdjacentHTML('beforeend', `<button class="btn btn-link" style="text-align:center" href="/trails/${trail.name}"><a href="/trails/${trail.name}">${trail.name}<br>City/Area: ${trail.city}, ${trail.area_name}</a></button>
        `)})
    
    });

function toTitleCase(str) {
    return str.toLowerCase().split(' ').map(function (word) {
        return (word.charAt(0).toUpperCase() + word.slice(1));
    }).join(' ');
    }

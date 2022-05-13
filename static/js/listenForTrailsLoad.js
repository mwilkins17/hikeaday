    fetch('/trails/map-state', {
    method: 'GET',
    })
    .then((response) => response.json())
    .then((responseJSON) => {
        for (const trail of responseJSON) {
        document.getElementById('state--trails--div').insertAdjacentHTML(
            'beforeend', `<button class="btn btn-link" style="text-align:center" href="/trails/${trail.name}">
            <a href="/trails/${trail.name}">${trail.name}<br>City/Area: ${trail.city}, ${trail.area_name}</a>
            </button>
        `)}
    })

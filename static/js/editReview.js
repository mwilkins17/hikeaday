document.getElementById('review--form').addEventListener('submit', (evt) => {
    evt.preventDefault();
    
    
    const formInputs = {
    review: document.getElementById('edited--review').value,
    trail_name : document.getElementById('trail_name').innerText,
    };

    fetch('/api/edit-review', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
        'Content-Type': 'application/json',
    },
    })
    .then((response) => response.json())
    .then((responseJSON) => {
        alert(document.getElementById('trail_name').innerText)
        document.getElementById('this--review').innerHTML = `${responseJSON.review}`;
    });
});

function alertStatus() {
    return (alert('Your review has been updated'))
}
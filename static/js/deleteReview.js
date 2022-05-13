document.getElementById('delete--review').addEventListener('submit', (evt) => {
    evt.preventDefault();

    fetch('/api/delete-review')
    .then((response) => response.json())
    .then((responseJSON) => {
        document.getElementById('this--review').innerHTML = ``;
    });
});

function alertStatus() {
    return (alert('Your review has been updated'))
}
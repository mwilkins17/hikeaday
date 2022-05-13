document.getElementById('edit--review').addEventListener('change', ()=> {
fetch('/trails/reviews')
.then(response => response.json())
.then(reviews => {
    for (const review of reviews) {
        document.getElementById('trail--reviews').innerHTML = document.getElementById('edited--review').value
        document.getElementById('trail--reviews').insertAdjacentHTML('beforeend', `
        <h3 style="border-style:solid; border-color:black; color:black; text-align: center; background-color: white; border-radius: 15px;">
        ${review.review_text}</h3>
        <p>Created on: ${review.created_at} by ${review.username}</p>
        `)}
    })
})
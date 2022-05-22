fetch('/trails/reviews')
.then(response => response.json())
.then(reviews => {
    for (const review of reviews) {
        document.getElementById('trail--reviews').insertAdjacentHTML('beforeend', `
        <div style="border-style:solid; border-color:black; color:black; text-align: center; background-color: white; border-radius: 15px; margin-bottom: 15px;">
            <h4>${review.review_text}</h4>
            <p>Created on: ${review.created_at} by ${review.username}</p>
        </div>
        `)
    }
})
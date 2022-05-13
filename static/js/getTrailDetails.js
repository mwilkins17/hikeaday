  fetch('/api/get-trail-details', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
    })
    .then((response) => response.json())
    .then((responseData) => {
    alert(responseData)
    document.getElementById('trail--header').insertAdjacentHTML('beforeend', `
    <span>${responseData.trail_name}</span>
    <span>${responseData.state}</span>
    <span>${responseData.city}</span>    
    `)
    });
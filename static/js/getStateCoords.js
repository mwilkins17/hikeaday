fetch('/trails/state-coords')
  .then(response => response.json())
  .then(responseData => {
    let coords = responseData[0]
    document.getElementById("state-lat").innerText = coords.lat
    document.getElementById("state-lng").innerText = coords.lat
  })
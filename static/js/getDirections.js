fetch('/get-trail-details')
      .then((response) => response.json())
      .then((trails) => {
        let trail = trails[0];
          document.getElementById('get--directions').addEventListener('click',()=> {
            window.open(`https://www.google.com/maps/search/?api=1&query=${trail.lat} ${trail.lng}`, "_blank")});
            document.getElementById('directions--div').addEventListener('click',()=> {
              window.open(`https://www.google.com/maps/search/?api=1&query=${trail.lat} ${trail.lng}`, "_blank")});
            
          })

'use strict';

function initMap() {
  const stateLat = parseFloat(document.getElementById('lat').innerText);
  const stateLng = parseFloat(document.getElementById('lng').innerText);
    const map = new google.maps.Map(document.getElementById('map'), {
      center: {
        lat: stateLat,
        lng: stateLng,
      },
      scrollwheel: true,
      zoom: 7.4,
      zoomControl: true,
      panControl: false,
      streetViewControl: false,
      // styles: MAPSTYLES, // mapStyles is defined in mapstyles.js
      mapTypeId: google.maps.MapTypeId.TERRAIN,
    });
  
    const trailInfo = new google.maps.InfoWindow();
    
   

    fetch('/get-trail-details')
      .then((response) => response.json())
      .then((trails) => {
        let trail = trails[0];
          // Define the content of the infoWindow
          const trailInfoContent = `
        <h5>${trail.name}</h5></div>
        `;

          const trailMarker = new google.maps.Marker({
            position: {
              lat: trail.lat,
              lng: trail.lng,
            },
            title: `Trail Name: ${trail.name}`,
            icon: {
              url: '../static/img/marker.png',
              scaledSize: new google.maps.Size(50, 50),
            },
            map, // same as saying map: map
          });


          map.addListener('click', () => {
            trailInfo.close()
          })

          trailMarker.addListener('click', () => {
            trailInfo.close();
            trailInfo.setContent(trailInfoContent);
            trailInfo.open(map, trailMarker);
            map.setZoom(15);
            map.setCenter(trailMarker.getPosition());
          });
        }
      )
    
      .catch(() => {
        alert(`
        Error
      `);
      });
  
  }

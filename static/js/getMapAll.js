'use strict';

function initMap() {
    const map = new google.maps.Map(document.getElementById('map'), {
      center: {
        lat: 48.8097343,
        lng: -96.5556199,
      },
      scrollwheel: true,
      zoom: 3,
      zoomControl: true,
      panControl: false,
      streetViewControl: false,
      mapTypeId: google.maps.MapTypeId.TERRAIN,
    });
  
    const trailInfo = new google.maps.InfoWindow();
    
   

    fetch('/trails/all-trails')
      .then((response) => response.json())
      .then((responseData) => {
        for (const trail of responseData) {
          // Define the content of the infoWindow
          const trailInfoContent = `
          <a style="text-decoration: none; color: black;" href="trails/${trail.name}">
          <div>
            <div class="row text-center">
            <div class="col-12"><h5>${trail.name}</h5></div><br/>
                <div class="col-3 text-left">
                    <div class="trail--thumbnail">
                      <img style="width:90%"
                        src="${trail.image_url}"
                        alt=""
                      />
                    </div>
                </div>
                  
                  
                <div style="text-align: left;" class="col-8 text-left">
                    <b>National Park: </b>${trail.area_name}<br/>
                    <b>Length </b>${trail.length}<br/>
                    <b>Elevation Gain: </b>${trail.elevation_gain}<br/>
                    <b>Difficulty Rating: </b>${trail.difficulty_rating}<br/>
                    <b>Route Type: </b>${trail.route_type}<br/>
                    <b>Location: </b>${trail.lat}, ${trail.lng}<br/>
                </div>
              </div>
            </div>
          </a>
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
            google.maps.event.removeListener(mouseOut);
          })

          trailMarker.addListener("mouseover", () => {
            trailInfo.setContent(trailInfoContent)
            trailInfo.open(map, trailMarker);
          });

          let mouseOut = trailMarker.addListener("mouseout", () => {
            trailInfo.close();
          });

          trailMarker.addListener('click', () => {
            trailInfo.close();
            trailInfo.setContent(trailInfoContent);
            trailInfo.open(map, trailMarker);
            map.setZoom(14);
            map.setCenter(trailMarker.getPosition());
            google.maps.event.removeListener(mouseOut);



          });
        }
      })
    
      .catch(() => {
        alert(`
        Error
      `);
    })
    
  }


fetch('/trail/weather')
  .then(response => response.json())
  .then(responseData => {
    document.getElementById('feels_like').innerText = "Feels Like: " + JSON.stringify(Math.round((responseData.main.feels_like - 273.15) * 1.8 +32)) + "\u00B0",
    document.getElementById('temp').innerText = "Current Temp: " + JSON.stringify(Math.round((responseData.main.temp - 273.15) * 1.8 +32)) + "\u00B0",
    document.getElementById('temp_max').innerText = "Today's High: " + JSON.stringify(Math.round((responseData.main.temp_max - 273.15) * 1.8 +32)) + "\u00B0",
    document.getElementById('temp_min').innerText = "Today's Low: " + JSON.stringify(Math.round((responseData.main.temp_min - 273.15) * 1.8 +32)) + "\u00B0",
    document.getElementById('sunrise').innerText = JSON.stringify(responseData.sys.sunrise),
    document.getElementById('sunset').innerText = JSON.stringify(responseData.sys.sunset),
    document.getElementById('weather-status').innerText = toTitleCase(JSON.stringify(responseData.weather[0].description).replace(/[^\w\s]/gi, '')),
    document.getElementById('weather-icon').innerHTML = `<img src="http://openweathermap.org/img/wn/${responseData.weather[0].icon.replace(/[^\w\s]/gi)}@2x.png"/>`;
  });
  let html = `<img src=http://openweathermap.org/img/wn/10d@${JSON.stringify(responseData.weather.icon)}/>`;
  let weatherIcon = JSON.stringify(responseData.weather[0].icon).replace(/[^\w\s]/gi)
  
  function toTitleCase(str) {
    return str.toLowerCase().split(' ').map(function (word) {
      return (word.charAt(0).toUpperCase() + word.slice(1));
    }).join(' ');
  }
  stringy = JSON.stringify(responseData.weather[0].description).replace(/[^\w\s]/gi, '');
  alert(toTitleCase(stringy));

  
// responseData.main.(feels_like - 273.15) * 1.8 +32
// responseData.main.temp
// responseData.main.temp_max
// responseData.main.temp_min
// responseData.sy.sunrise
// responseData.sy.Sunset
// responseData.weather.description
// responseData.sy.Sunset

  // {"base":"stations","clouds":{"all":0},
  // "cod":200,"coord":{"lat":40.7168,"lon":-74.0663},
  // "dt":1651262824,
  // "id":5099357,
  // "main":{"feels_like":288.29,"humidity":13,"pressure":1016,"temp":290.19,"temp_max":291.69,"temp_min":288.7},
  // "name":"Hudson",
  // "sys":{"country":"US","id":4610,"sunrise":1651226241,"sunset":1651276178,"type":1},
  // "timezone":-14400,"visibility":10000,
  // "weather":[{"description":"clear sky","icon":"01d","id":800,"main":"Clear"}],
  // "wind":{"deg":310,"gust":11.83,"speed":8.23}}


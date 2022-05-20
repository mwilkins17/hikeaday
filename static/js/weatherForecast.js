fetch('/trail/weather')
  .then(response => response.json())
  .then(responseData => {
    let i = 0;
    weatherData = responseData.list;
    for (const data of weatherData) {
        let temp_min = `<span id="temp_min">Low: ${JSON.stringify(Math.round(data.temp.min))}\u00B0</span>`;
        let temp_max = `<span id="max">High: ${JSON.stringify(Math.round(data.temp.max))}\u00B0</span>`;
        let weather_description = `<span id="weather_description">${toTitleCase(data.weather[0].description)}</span>`;
        let weather_icon = `<img style="width: 50%;" src="http://openweathermap.org/img/wn/${data.weather[0].icon.replace(/[^\w\s]/gi)}@2x.png"/>`; 
        dateObj = new Date(parseInt(data.dt) * 1000);
        let utcString = dateObj.toUTCString();
        let date = utcString.slice(0, -13);
        let split_dateTime = date.split(",");
        let split_date = split_dateTime[1].split(" ");
        let dayName = split_dateTime[0];
        let dayNum = split_date[1];
        let monthName = split_date[2];
        let year = split_date[3];
        time = utcString.slice(-11, -7);
        if (i > 7 ) {
            break
        }
        else {
        document.getElementById('forecast').insertAdjacentHTML("beforeend", `
        <div id="forecast--card" class="col text-center">
              <div class="row">
              </div>
              <h7 style="font-size: 14px" >${dayName}, ${monthName} ${dayNum}, ${year}</h7>

              ${weather_icon}
              <div class="row">
              </div>

              <div class="row">
                  ${temp_max}
                  ${temp_min} 
                  ${weather_description}
              </div>
        </div>`);
        prevDate = date;
    }}
  });

  function toTitleCase(str) {
    return str.toLowerCase().split(' ').map(function (word) {
      return (word.charAt(0).toUpperCase() + word.slice(1));
    }).join(' ');
  }

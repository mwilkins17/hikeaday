fetch('/trail/weather')
  .then(response => response.json())
  .then(responseData => {
    let prevDate
    weatherData = responseData.list;
    for (const data of weatherData) {
        // let forecast = data[0]
        // alert(data.main.weather)
        // alert(Date(data.dt))
        // console.log(Object.keys(weatherData).length);
        // const weather_card = document.createElement("div");
        // weather_card.id = i;
        let feels_like = `<span id="feels-like">Feels like: ${JSON.stringify(Math.round((data.main.feels_like - 273.15) * 1.8 +32))}\u00B0</span>`;
        let temp_min = `<span id="temp_min">Low: ${JSON.stringify(Math.round((data.main.temp_min- 273.15) * 1.8 +32))}\u00B0</span>`;
        let temp_max = `<span id="max">High: ${JSON.stringify(Math.round((data.main.temp_max- 273.15) * 1.8 +32))}\u00B0</span>`;
        let weather_main = `<span id="weather_main">${data.weather[0].main}</span>`;
        let weather_description = `<span id="weather_description">${toTitleCase(data.weather[0].description)}</span>`;
        let weather_icon = `<img style="width: 50%;" src="http://openweathermap.org/img/wn/${data.weather[0].icon.replace(/[^\w\s]/gi)}@2x.png"/>`; 
        let temp = `<span id="temp">Temp: ${JSON.stringify(Math.round((data.main.temp - 273.15) * 1.8 +32))}\u00B0</span>`;
        dateObj = new Date(parseInt(data.dt) * 1000);
        let utcString = dateObj.toUTCString();
        let locale_string = dateObj.toLocaleString();
        let date = utcString.slice(0, -13);
        let split_dateTime = date.split(",");
        let split_date = split_dateTime[1].split(" ");
        let dayName = split_dateTime[0];
        let dayNum = split_date[1];
        let monthName = split_date[2];
        let year = split_date[3];
        time = utcString.slice(-11, -7);
        let dateTime = `<span style=""id="date-time">${utcString} ${time}</span>`;
        if (date === prevDate) {
            continue
        }
        else {
        document.getElementById('forecast').insertAdjacentHTML("beforeend", `
        <div id="forecast" class="col-2 text-center">
                <div class="row">
                </div>
                <h7 style="font-size: 14px" >${dayName}, ${monthName} ${dayNum}, ${year}</h7>

                ${weather_icon}
                <div class="row">
                </div>
                <div class="row">
                        ${temp}
                </div>

                <div class="row">
                    ${feels_like}
                    ${temp_min}
                    ${temp_max}
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

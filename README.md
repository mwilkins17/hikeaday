# hikeAday ![trail_name_icon](https://user-images.githubusercontent.com/100727077/168654942-fe59c639-2c1a-49f0-abf7-aff1a9c268ce.png)
 
![](file:///Users/victorsi/Desktop/Screen%20Shot%202020-03-14%20at%2012.44.09%20AM.png)<br>
hikeAday is a full-stack web application where you can look up National Park trails information. You can see trail deatils, see the local weather forecast for a trail, keep track of your favorite trail, and review trails. <br>

💻 Deployment Link: https://hikeaday.app
<br>


## Contents ![trail_name_icon](https://user-images.githubusercontent.com/100727077/168654942-fe59c639-2c1a-49f0-abf7-aff1a9c268ce.png)
* [Features](#features)
* [Technologies & Stack](#techstack)
* [Set-up & Installation](#installation)
* [About the Developer](#aboutme)

## <a name="features"></a>

User-friendly landing page
<br>
<br>
![](static/gifs/landing-page.gif)
<br>

User registration, log-in, & log-out
<br>
<br>
![](static/gifs/signup.gif)
<br>

Search for trails by state, or by selecting a map marker
<br>
<br>
![](static/gifs/add-plant.gif)
<br/>

Learn about the trail's details such as length, elevation gain, features, activtites, and more!
<br>
<br>
![](static/gifs/entries.gif)
<br/>

See local weather forecast for each trail
<br>
<br>
![](static/gifs/twilio.gif)
<br>

See reviews for each trails, and leave reviews if a user is logged in
<br>
<br>
![](static/gifs/chat.gif)
<br>

"Favorite" a trail if a user is logged in
<br>
<br>
![](static/gifs/plant-of-the-moment.gif)
<br>

Keep track of reviews and your favorite trails in the user Profile page
<br>
<br>
![](static/gifs/plant-of-the-moment.gif)
<br>


## <a name="techstack"></a>![trail_name_icon](https://user-images.githubusercontent.com/100727077/168654942-fe59c639-2c1a-49f0-abf7-aff1a9c268ce.png) Technologies and Stack
**Backend:**
Python, Flask, SQLAlchemy, PostgreSQL, FlaskSocketIO <br>
**Frontend:**
React, Javascript, jQuery, Babel, Bootstrap, Google Fonts, HTML5, CSS3 <br>
**APIs:**
Google Maps Javascript, Open Weather Map API



## <a name="installation"></a>![trail_name_icon](https://user-images.githubusercontent.com/100727077/168654942-fe59c639-2c1a-49f0-abf7-aff1a9c268ce.png) Set-up & Installation
Install a code editor such as [VS code](https://code.visualstudio.com/download) or [Sublime Text](https://www.sublimetext.com/).<br>
Install [Python3](https://www.python.org/downloads/)<br>
Install [pip](https://pip.pypa.io/en/stable/installation/), the package installer for Python <br>
Install [postgreSQL](https://www.postgresql.org/) for the relational database.<br>


Clone or fork repository:
```
$ git clone https://github.com/anjelicasilva/ISpeakPlantish.git
```
Create and activate a virtual environment inside the hikeAday directory:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip3 install -r requirements.txt
```
Make an account with [Google Developers](https://developers.google.com/maps/documentation) & get an [API key](https://console.cloud.google.com/google/maps-apis/start).<br>
Make an account with [Bing Search API](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/) & get an [API key](https://aka.ms/bingapisignup).<br>
Make an account with [Open Weather Map API](https://openweathermap.org/api) & get an [API key](https://home.openweathermap.org/users/sign_up)

Store these keys in a file named 'secrets.sh' <br> 
```
$ source secrets.sh
```
With PostgreSQL, create the hikeAday database
```
$ createdb hikeaday
```
Create all tables and relations in the database and seed all data:
```
$ python3 -i crud.py
$ _populate_database()
```
Run the app from the command line:
```
$ python3 server.py
```


## <a name="aboutme"></a>![trail_name_icon](https://user-images.githubusercontent.com/100727077/168654942-fe59c639-2c1a-49f0-abf7-aff1a9c268ce.png) About the Developer

hikeAday creator Mason Wilkins has worked in property management and the real estate industry as a realtor for most of his career. Mason has always had an interest in technology all of his life, and after trying many different career paths, he decided to puruse his love for technology by learning to program by attending a software engineering bootcamp with Hackbright Academy. Mason truly found his way as with this botocamp, he felt he was finally being challenged and his love for an ability to problem solve could be used. Mason is excited for the challanges he will get to overcome and the problems he will have the opportunity to solve after the program. This is her first full-stack project. Mason can be found on [LinkedIn](https://www.linkedin.com/in/mwilkins17/) and on [Github](https://github.com/mwilkins17).
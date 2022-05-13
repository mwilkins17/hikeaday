from crypt import methods
from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for
from random import choice 
import http.client, json, requests, datetime, crud, os
from model import connect_to_db, db, Trail, User, Favorite, Review, Images
from datetime import datetime
from geopy.geocoders import Nominatim
from functools import partial

WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
FLASK_APP_SECRET_KEY = os.environ['FLASK_APP_SECRET_KEY']
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']



app = Flask(__name__)
app.secret_key = FLASK_APP_SECRET_KEY


STATES_ABBREV = set(["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", 
          'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'dc', 'de', 'fl',
          'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me',
          'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh',
          'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri',
          'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy'])

US_STATES_TO_ABBREV = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

INVERTED_US_STATES_TO_ABBREV = dict(map(reversed, US_STATES_TO_ABBREV.items()))
print(INVERTED_US_STATES_TO_ABBREV)
###############################################################################
#                                                                             #
#                             NAVIGATION ROUTES                               #
#                                                                             #
###############################################################################



@app.route("/")
def index():
        
    return render_template('index.html')

@app.route("/contact")
def contact():
    
    return render_template('contact.html')

@app.route("/about")
def about():
    
    return render_template('about.html')


###############################################################################
#                                                                             #
#                               TRAIL ROUTES                                  #
#                                                                             #
###############################################################################


@app.route("/trails", methods=["GET"])
def trails():
    """######## Render the trails.html route ########"""

    return render_template('trails.html')


#   ----------------------------------------------------------------

#       RENDER TRAILS.HTMLTEMPLATE & SEARCH FOR TRAIL SELECTED

#   ----------------------------------------------------------------


@app.route("/trail/state/state", methods=["POST"])
def trail_search():    
    """######## Search for a trail ########"""

    state = request.form.get('state')

    if len(state) == 2:
        state = state.upper()
        
    if len(state) > 2:
        state = state.title()

    if state in STATES_ABBREV:
        state = INVERTED_US_STATES_TO_ABBREV[state]

    if state not in INVERTED_US_STATES_TO_ABBREV.keys() and state not in US_STATES_TO_ABBREV.keys() and state not in STATES_ABBREV:
        flash(f"{state} is not a state. Please check your spelling.")
        return redirect("/")
    
    session['state_name'] = state
    crud.add_state_coords_to_session()

    return redirect('/trails')



@app.route("/trails/all-state", methods=["POST", "GET"])
def get_trail_data():
    trails_data = []
    list_of_trail_dicts = []

    trail_data_in_a_state = db.session.query(Trail).filter(Trail.state_name == session['state_name']).all()

    for trail in trail_data_in_a_state:
        coords = eval(trail._geoloc)
        lat = coords['lat']
        lng = coords['lng']
        image_url = db.session.query(Images.image_url).filter(Images.trail_id == trail.trail_id).first()
        trail_info =[{
            "name": trail.name,
            "city" : trail.city_name,
            "area_name" : trail.area_name,
            'lat' : lat,
            'lng' : lng,
            'elevation_gain' : int(trail.elevation_gain),
            'difficulty_rating' : trail.difficulty_rating,
            'route_type' : trail.route_type,
            "image_url" : image_url[0],
        }]
        trails_data.extend(trail_info)

    return jsonify(trails_data)

@app.route("/trails/map-state")
def get_map_data():
    trails_data = []
    list_of_trail_dicts = []
    
    trail_data_in_a_state = db.session.query(Trail).filter(Trail.state_name == session['state_name']).all()

    for trail in trail_data_in_a_state:
        coords = eval(trail._geoloc)
        lat = coords['lat']
        lng = coords['lng']
        image_url = db.session.query(Images.image_url).filter(Images.trail_id == trail.trail_id).first()
        trail_info =[{
            "name": trail.name,
            "city" : trail.city_name,
            "area_name" : trail.area_name,
            'lat' : lat,
            'lng' : lng,
            'elevation_gain' : int(trail.elevation_gain),
            'difficulty_rating' : trail.difficulty_rating,
            'route_type' : trail.route_type,
            # "image_url" : image_url[0],
        }]
        trails_data.extend(trail_info)

    return jsonify(trails_data)


@app.route("/trails/all-trails")
def get_state_coords():
        trails_data = []

        all_trails = db.session.query(Trail).all()
        for trail in all_trails:
            coords = eval(trail._geoloc)
            lat = coords['lat']
            lng = coords['lng']
            trail_info = {
                "name": trail.name,
                "city" : trail.city_name,
                "area_name" : trail.area_name,
                'lat' : lat,
                'lng' : lng,
                'elevation_gain' : int(trail.elevation_gain),
                'difficulty_rating' : trail.difficulty_rating,
                'route_type' : trail.route_type,
            }
            trails_data.append(trail_info)

        return jsonify(trails_data)
    


#   ----------------------------------------------------------------

#       RENDER TRAILS.HTMLTEMPLATE & DISPLAY TRAIL DETAILS,
#          TRAIL REVIEWS, AND TRAIL WEATHER

#   ----------------------------------------------------------------


@app.route("/trails/<trail_name>")
def trail_details(trail_name):
    """######## Get the details page of a trail ########"""

    trail = db.session.query(Trail).filter(Trail.name == trail_name).first()
    trail_id = trail.trail_id
    session['trail_id'] = trail.trail_id

    session['trail_name'] = trail_name
    features = crud.get_features(trail_id)
    activities = crud.get_activities(trail_id)
    
    
    reviews = crud.get_all_reviews_by_current_trail(trail_id)
    
    trail_images = crud.get_all_trail_images_for_current_trail(session['trail_id'])
    coords = eval(trail._geoloc)
    lat = coords['lat']
    lng = coords['lng']

    active_image = trail_images[1]
    if session.get('user_id'):
        reviewed = crud.did_user_review(session['user_id'], trail_id)
        review_text = crud.get_user_review_for_current_trail(session['user_id'], trail_id)
        return render_template("/trail_details.html",
                            active_image = active_image,
                            reviewed=reviewed,
                            review_text=review_text,
                            reviews=reviews,
                            trail=trail,
                            features=features,
                            activities=activities,
                            trail_images = trail_images,
                            lat=lat,
                            lng=lng)
    
    else:
        reviewed=False
        return render_template("/trail_details.html",
                            active_image=active_image,
                            reviewed=reviewed,
                            trail=trail,
                            reviews=reviews,
                            features=features,
                            activities=activities,
                            trail_images = trail_images,
                            lat=lat,
                            lng=lng)



@app.route("/trails/<trail_name>", methods=["POST"])
def submit_review(trail_name):
    """Get trail details. Page renders dynamically depending on whether
                or not a user is in the session"""
                
    trail = Trail.query.filter(Trail.trail_id == session['trail_id']).first()
    
    trail_id = trail.trail_id
    session['trail_id'] = trail_id
    
    trail_name = session['trail_name']
    
    
    features = crud.get_features(trail_id)
    activities = crud.get_activities(trail_id)
    
    user_id = session['user_id']
    
    review = request.form.get("new-review")

    reviews= crud.get_all_reviews_by_current_trail(session['trail_id'])
    user_review = crud.did_user_review(user_id, trail_id)
    
    session['total_reviews'] = len(crud.get_all_current_user_reviews(user_id))
    
    delete_review = request.form.get('delete-review')
    edited_review = request.form.get('edit-review')
    
    if session['user_id']:
        if user_review:

                reviewed = True
                review_text = crud.get_user_review_for_current_trail(user_id, trail_id)
                
                if edited_review:
                    crud.edit_review(edited_review, user_id, trail_id)
                    review_text = edited_review
                    return redirect(f"/trails/{trail_name}")
                
                if delete_review:
                    reviewid = crud.get_user_review_id_for_current_trail(user_id, trail_id)
                    Review.query.filter(Review.review_id == reviewid).delete()
                    session.modified = True
                    db.session.commit()
                    return redirect(f"/trails/{trail_name}")
                
                
                return render_template("/trail_details.html",
                                        reviewed=reviewed,
                                        review_text=review_text,
                                        trail=trail,
                                        reviews=reviews,
                                        features=features,
                                        activities=activities)
        else:
            ###### Instantiate a Review / Create a Review ######
            crud.create_review(user_id=user_id,
                               trail_id=trail_id,
                               num_stars=4,
                               review_text=review)
            
            return redirect(f'/trails/{trail_name}')
    
    else:
        reviewed = False
        return render_template("/trail_details.html",
                               reviewed=reviewed,
                               trail=trail,
                               reviews=reviews,
                               features=features,
                               activities=activities)   


@app.route("/api/edit-review", methods=["POST"])
def edit_review():
    review = request.json.get("review")
    crud.edit_review(review, session['user_id'], session['trail_id'])
    # all_reviews = crud.get_all_reviews_by_current_trail(session['trail_id'])
    res = {'success' : True,
        'status' : 'Your review has been edited.',
        'review' : review}
    return res

@app.route("/api/delete-review")
def delete_review():
    reviewid = crud.get_user_review_id_for_current_trail(session['user_id'], session['trail_Id'])
    Review.query.filter(Review.review_id == reviewid).delete()
    session.modified = True
    db.session.commit()
    res = {'success' : True}
    return jsonify(res)

@app.route('/trails/reviews')
def get_reviews_for_current_trail():
    reviews = crud.get_all_reviews_by_current_trail(session['trail_id'])
    print(type(reviews))
    return jsonify(reviews)



@app.route('/get-trail-details')
def get_trail_details():
    trail = db.session.query(Trail).filter(Trail.trail_id == session['trail_id']).first()
    features = crud.get_features(session['trail_id'])
    activities = crud.get_activities(session['trail_id'])
    image_url = db.session.query(Images.image_url).filter(Images.trail_id == session['trail_id']).first()
    
    coords = eval(trail._geoloc)
    lat = coords['lat']
    lng = coords['lng']
    
    trail_info = [
    {
        "name": trail.name,
        "city" : trail.city_name,
        "area_name" : trail.area_name,
        'lat' : lat,
        'lng' : lng,
        'elevation_gain' : int(trail.elevation_gain),
        'difficulty_rating' : trail.difficulty_rating,
        'route_type' : trail.route_type,
        "image_url" : image_url[0],
        'features' : features,
        'activities' : activities,
    }]
    
    return jsonify(trail_info)


@app.route("/trail/weather")
def get_weather():
    """Route for getting weather details for each trail"""
    
    trail = Trail.query.filter(Trail.name == session['trail_name']).first()
    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    querystring = {"q":f"{trail.city_name},{trail.state_name}"}

    headers = {
        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
        "X-RapidAPI-Key": WEATHER_API_KEY,
        "units": "imperial",
        "content-type": "text/plain; charset=utf-8",
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    weather_dict = response.json()

    return weather_dict


###############################################################################
#                                                                             #
#                           FAVORITES ROUTES                                  #
#                                                                             #
###############################################################################


@app.route("/is-favorite")
def check_if_favorited():
    """Route to check if a trail is favorited or not"""
    favorite_status = crud.is_current_trail_favorited(session['user_id'], session['trail_id'])
    return {"favorited": favorite_status}


@app.route("/update-favorite")
def update_favorite():
    """Add or remove a favorite just by querying route, return
    true or false if the trail is favorited"""   

    return {"fav": crud.update_favorite(session['user_id'], session['trail_id'])}


###############################################################################
#                                                                             #
#                      USER AUTHENTICATION ROUTES                             #
#                                                                             #
###############################################################################

@app.route("/sign-up")
def sign_up():
    """Render the sign-up.html template"""
    
    return render_template('sign-up.html')

@app.route('/sign-up', methods=["POST"])
def register_user():  
        """Register a user and commit their info into the db"""

        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        password_repeat = request.form.get("password-repeat")
        user = crud.get_user_by_email(email)
        user_username = crud.get_user_by_username(username)

        if user:
            flash("A user with that email already exists")
            return redirect("/sign-up")
        
        elif user_username:
            flash("A user with that username already exists")
            return redirect("/sign-up")
            
        elif password != password_repeat:
            flash("Password do not match")
            return redirect("/sign-up")

        else:
            user = crud.create_user(fname.title(), lname.title(), email, username, password)
            db.session.add(user)
            db.session.commit()

            flash("User created successfully; you may now log in")
            return redirect("/login")
            
        return redirect('/')
    
    
@app.route("/login")
def login():
    """Render the login.html template"""
    
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def user_log_in():
    """ Log a user in"""    
    
    username = request.form.get("username")
    password = request.form.get("password")
    user = crud.get_user_by_username(username)
    
    if not user:
        flash("Invalid username. Please try again")
        return redirect("/login")
    
    elif user.password != password:
        flash("Invalid password. Please try again")
        return redirect("/login")
    
    else:
        session['username'] = user.username
        session['user_id'] = user.user_id
        username = session['username']
        flash("Successfully logged in!")
        return redirect("/")
    
    return redirect("/")


@app.route("/logout")
def logout():
    """######## Log a user out and remove everything from session ########"""
    
    session.clear()
    
    
    flash("You have been logged out. See you next time!")
    return redirect("/")


###############################################################################
#                                                                             #
#                           PROFILE ROUTES                                    #
#                                                                             #
###############################################################################


@app.route('/profile/')
def get_profile():
    """Access the user's profile"""
    
    return render_template("profile.html",)
    
@app.route('/profile-info')
def get_profile_info():
    """Route for AJAX request for updating profile info"""
    
    user = crud.get_user_by_username(session['username'])
    
    user_reviews = crud.get_all_current_user_reviews(session['user_id'])

    favorite_trails = crud.get_all_trail_names_for_favorited_trails(session['user_id'])
    

    username = user.username
    email = user.email
    first_name = user.fname
    last_name = user.lname

    user_info = {
        "user_reviews" : user_reviews,
        "user_favorites" : favorite_trails,
        "username" : username,
        "email" : email,
        "fname" : first_name,
        "lname" : last_name,
    }
    
    return user_info


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
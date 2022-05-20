from crypt import methods
from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for, g
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

###############################################################################
#                                                                             #
#                             NAVIGATION ROUTES                               #
#                                                                             #
###############################################################################

@app.route("/")
def index():
    """ Render the home page """
        
    return render_template('index.html')

@app.route("/contact")
def contact():
    """ *Not in use currently* Render the contact page """
    return render_template('contact.html')

@app.route("/about")
def about():
    """ *Not in use currently* Render the about page """
    return render_template('about.html')


###############################################################################
#                                                                             #
#                               TRAIL ROUTES                                  #
#                                                                             #
###############################################################################


@app.route("/trails", methods=["GET"])
def trails():
    """ Render the trails.html route """

    return render_template('trails.html')


#   ----------------------------------------------------------------

#       RENDER TRAILS.HTMLTEMPLATE & SEARCH FOR TRAIL SELECTED

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
    
    trail_len = "{:.2f}".format(trail.length/5280)
    length = str(trail_len) + " " + "miles"
    elevation_gain = str(int(trail.elevation_gain))+ " " + 'ft'
    route_type = trail.route_type.title()
    
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
                            route_type=route_type,
                            length=length,
                            elevation_gain = elevation_gain,
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
                            route_type=route_type,
                            length=length,
                            elevation_gain = elevation_gain,
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
                
    trail = Trail.query.filter(Trail.name == session['trail_name']).first()
    
    trail_id = trail.trail_id
    session['trail_id'] = trail_id
    
    trail_name = session['trail_name']
    
    trail_len = "{:.2f}".format(trail.length/5280)
    length = str(trail_len) + " " + "miles"
    elevation_gain = str(int(trail.elevation_gain))+ " " + 'ft'
    
    route_type = trail.route_type.title()
    
    features = crud.get_features(trail_id)
    activities = crud.get_activities(trail_id)
    
    user_id = session['user_id']
    review = request.form.get("new-review")

    reviews= crud.get_all_reviews_by_current_trail(session['trail_id'])
    user_review = crud.did_user_review(user_id, trail_id)
    
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
                    flash('Your review has been deleted')
                    return redirect(f"/trails/{trail_name}")
                
                
                return render_template("/trail_details.html",
                                        route_type=route_type,
                                        length=length,
                                        elevation_gain = elevation_gain,
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
                               route_type=route_type,
                               length=length,
                               elevation_gain = elevation_gain,
                               reviewed=reviewed,
                               trail=trail,
                               reviews=reviews,
                               features=features,
                               activities=activities)   

###############################################################################
#                                                                             #
#                        Data Routes for Google Maps API                      #
#                                                                             #
###############################################################################

@app.route("/trail/state/state", methods=["POST"])
def trail_search():    
    """ Search for a trail  by state """

    state = request.form.get('state')

    if len(state) == 2:
        state = state.upper()
        
    if len(state) > 2:
        state = state.title()

    if state in crud.STATES_ABBREV:
        state = crud.INVERTED_US_STATES_TO_ABBREV[state]

    if state not in crud.INVERTED_US_STATES_TO_ABBREV.keys() and state not in crud.US_STATES_TO_ABBREV.keys() and state not in crud.STATES_ABBREV:
        flash(f"{state} is not a state. Please check your spelling.")
        return redirect("/")
    
    session['state_name'] = state
    crud.add_state_coords_to_session()

    return redirect('/trails')


@app.route("/trails/map-state")
def get_state_map_markers():
    """Retrieve map markers for state search"""
    
    trails_data = []
    
    trail_data_in_a_state = db.session.query(Trail).filter(Trail.state_name == session['state_name']).all()

    for trail in trail_data_in_a_state:
        coords = eval(trail._geoloc)
        lat = coords['lat']
        lng = coords['lng']
        image_url = db.session.query(Images.image_url).filter(Images.trail_id == trail.trail_id).first()
        image_string = str(image_url)
        img = eval(image_string)
        elevation_gain = str(int(trail.elevation_gain))+ " " + 'feet'
        route_type = trail.route_type.title()
        trail_length = "{:.2f}".format(trail.length/5280)
        formatted_trail_length = str(trail_length) + " " + "miles"
        trail_info =[{
            "name": trail.name,
            "city" : trail.city_name,
            "area_name" : trail.area_name,
            'lat' : lat,
            'lng' : lng,
            'length' : formatted_trail_length,
            'elevation_gain' : elevation_gain,
            'difficulty_rating' : trail.difficulty_rating,
            'route_type' : route_type,
            "image_url" : img[0],
        }]
        trails_data.extend(trail_info)
    
    return jsonify(trails_data)


@app.route("/trails/all-trails")
def get_all_map_markers():
        """ Retrieve coordinates from database for every trail"""
        all_trail_markers = db.session.query(Images.image_url).filter(Images.user_id == 2).first()

        return all_trail_markers[0]




@app.route('/get-trail-details')
def get_trail_map_details():
    trail = db.session.query(Trail).filter(Trail.trail_id == session['trail_id']).first()
   
    coords = eval(trail._geoloc)
    lat = coords['lat']
    lng = coords['lng']
    
    trail_info = [
    {
        "name": trail.name,
        'lat' : lat,
        'lng' : lng,
    }]
    
    return jsonify(trail_info)


###############################################################################
#                                                                             #
#              Routes for Editing/Deleting/Adding Reviews                     #
#                                                                             #
###############################################################################


@app.route("/api/edit-review", methods=["POST"])
def edit_review():
    """Edit a user's review for the user and trail in the session"""
    
    review = request.json.get("review")

    crud.edit_review(review, session['user_id'], session['trail_id'])

    response = {'success' : True,
        'status' : 'Your review has been edited.',
        'review' : review}
    return response

@app.route("/api/delete-review")
def delete_review():
    """Delete a user's review for the user and trail in the session"""
    
    reviewid = crud.get_user_review_id_for_current_trail(session['user_id'], session['trail_Id'])
    Review.query.filter(Review.review_id == reviewid).delete()
    session.modified = True
    db.session.commit()
    res = {'success' : True}
    return jsonify(res)

@app.route('/trails/reviews')
def get_reviews_for_current_trail():
    """Get all reviews for the current trail in the session"""
    
    reviews = crud.get_all_reviews_by_current_trail(session['trail_id'])
    print(type(reviews))
    return jsonify(reviews)

###############################################################################
#                                                                             #
#                           Trail Weather Route                               #
#                                                                             #
###############################################################################

@app.route("/trail/weather")
def get_weather():
    """Route for getting weather details for the trail in the session"""
    
    trail = Trail.query.filter(Trail.trail_id == session['trail_id']).first()
    url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
    coords = eval(trail._geoloc)
    lat = str(coords['lat'])
    lng = str(coords['lng'])
    querystring = {"q":f'{trail.city_name}, US', 'lat' : f'{lat}', 'lon':f'{lng}', 'units':'imperial'}

    headers = {
        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
        "X-RapidAPI-Key": WEATHER_API_KEY,
        "units": "imperial",
        "content-type": "text/plain; charset=utf-8",
    }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    weather_dict = response.json()
    print(response.json())
    return weather_dict


###############################################################################
#                                                                             #
#                           FAVORITES ROUTES                                  #
#                                                                             #
###############################################################################


@app.route("/is-favorite")
def check_if_favorited():
    """Route to check if a trail is favorited or not for a user in the session"""
    favorite_status = crud.is_current_trail_favorited(session['user_id'], session['trail_id'])
    if favorite_status == False:
        return {"favorited": False}
    else:
        return {"favorited": True}


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
    


@app.route("/logout")
def logout():
    """ Log a user out and remove everything from session """
    
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
    """Route for AJAX request for getting profile info"""
    
    user = crud.get_user_by_username(session['username'])
    
    user_reviews = crud.get_all_current_user_reviews(session['user_id'])

    favorite_trails = crud.get_all_trail_names_for_favorited_trails(session['user_id'])    
    print(favorite_trails)
        
    username = user.username
    email = user.email
    first_name = user.fname
    last_name = user.lname

    user_info = {
        "user_reviews" : user_reviews,
        "favorites" : favorite_trails,
        "username" : username,
        "email" : email,
        "fname" : first_name,
        "lname" : last_name,
    }
    
    return user_info


if __name__ == '__main__':
    connect_to_db(app)
    app.run()
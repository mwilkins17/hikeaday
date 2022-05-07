from crypt import methods
from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for
from random import choice 
import http.client, json, requests, datetime, crud
from model import connect_to_db, db, Trail, User, Favorite, Review
from datetime import datetime
from secrets import WEATHER_API_KEY


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'


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


@app.route("/trails", methods=["POST"])
def trail_search():    
    """######## Search for a trail ########"""
    
        
    search = request.form.get('trail_search').title()
    session['search'] = search
    results = crud.search_trails(search)

    return render_template('trails.html', results = results)


@app.route("/api/trails")
def get_trail_data():
    state = session['search']
    trail_data_in_a_state = db.session.query(Trail).filter(Trail.state_name == state).all()

    
    for trail in trail_data_in_a_state:
        coords = eval(trail._geoloc)
        lat = coords['lat']
        lng = coords['lng']
        
        
        trails = [
        {
            "trail_name": trail.name,
            "city_name" : trail.city_name,
            'lat' : lat,
            'lng' : lng,
            'elevation_gain' : trail.elevation_gain,
            'difficulty_rating' : trail.difficulty_rating,
            'route_type' : trail.route_type,
        }]
        

    return jsonify(trails)

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
    features = crud.get_features()
    activities = crud.get_activities()
    
    
    reviews = crud.get_all_reviews_by_current_trail(trail_id)
    
    trail_images = crud.get_all_trail_images_for_current_trail(session['trail_id'])
    coords = eval(trail._geoloc)
    lat = coords['lat']
    lng = coords['lng']

    active_image = trail_images[2]
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
    
    features = crud.get_features()
    activities = crud.get_activities()
    
    trail_name = session['trail_name']
    trail = Trail.query.filter(Trail.name == trail_name).first()
    
    trail_id = trail.trail_id
    session['trail_id'] = trail_id
    
    
    user_id = session['user_id']
    
    review = request.form.get("new-review")
    reviews = crud.get_all_reviews_by_current_trail(trail_id)

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
        """######## Register a user and commit their info into the db ########"""

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
    """######## Render the login.html template ########"""
    
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def user_log_in():
    """######## Log a user in ########"""    
    
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
    # user_favorites = crud.get_all_favorites_by_user(session['user_id'])
    favorite_trails = crud.get_all_trail_names_for_favorited_trails(session['user_id'])
    
    reviews_list = []
    review_values = user_reviews.values()
    print(user_reviews)
    for review in review_values:
        reviews_list.append(review[1])
    username = user.username
    email = user.email
    first_name = user.fname
    last_name = user.lname
    
    user_info = {
        "user_reviews" : reviews_list,
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
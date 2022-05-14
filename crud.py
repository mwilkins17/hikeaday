"""CRUD operations."""

import re, datetime, json, requests, csv, os, model
from model import db, User, Favorite, Trail, Review, Images, connect_to_db
from flask import session, g, jsonify
from datetime import datetime
from geopy.geocoders import Nominatim
from functools import partial

IMAGE_API_KEY = os.environ['IMAGE_API_KEY']






#################################################################################
#                                                                               #
#                            User Functions                                     #
#                                                                               #
#################################################################################


def create_user(fname, lname, email, username, password):
    """Create a new instance of a user in the User class"""

    user = User(
                fname=fname,
                lname=lname, 
                email=email,
                username=username,
                password=password
                )
    
    return user

def get_users():
    """Show all users."""
    
    return User.query.all()



def get_user_by_id(username):
    """Gets a username from the database by ID"""
    
    user_id = User.query.get(User.user_id).where(User.username == username)
    return user_id



def get_user_by_username(username):
    """Checks the database for a username"""
    
    return User.query.filter(User.username == username).first()



def get_user_by_email(email):
    """Return a User by Email"""
    
    return User.query.filter(User.email == email).first()
    
    
#################################################################################

                            # Favorites Functions

#################################################################################

def create_favorite(user_id, trail_id):
    """Create a new instance of favorite in the Favorite class"""
    
    favorite = Favorite(user_id=user_id,
                        trail_id=trail_id)
    
    return favorite

def get_all_favorites_by_user(user_id):
    """Get all the favorites for the user in the Flask session"""
    # Favorite.query.filter(User.user_id == user_id).all()
    favorites = Favorite.query.filter(User.user_id == user_id).all()
    return favorites


def is_current_trail_favorited(user_id, trail_id):
    """Check the database to see if the current trail is favorited"""
    is_favorited = bool(db.session.query(Favorite.favorite_id).filter(Favorite.user_id == user_id,
                                                     Favorite.trail_id == trail_id))
    is_Favorited = db.session.query(Favorite.favorite_id
                                                 ).filter(
                                                     Favorite.user_id == user_id, Favorite.trail_id == trail_id).all()
    # db.session.query(Favorite).filter((Favorite.user_id == user_id) & (Favorite.trail_id == trail_id)).all()

    if is_Favorited:
        return True
    else:
        return False
    
def get_user_favorite_id_for_current_trail(user_id, trail_id):
    """Get the favorite ID from the database for the trail in the Flask session"""
    current_user_favorite_id = db.session.query(Favorite.favorite_id
                                                 ).filter(
                                                     Favorite.user_id == user_id, Favorite.trail_id == trail_id).all()
    
    if current_user_favorite_id:
        return current_user_favorite_id[0]
    else:
        return None


def update_favorite(user_id, trail_id):
    """Update the database if a trail is or is not favorited"""
    is_favorite = is_current_trail_favorited(user_id, trail_id)
    favorite_id = get_user_favorite_id_for_current_trail(user_id, trail_id)
    if is_favorite:
        favorite = db.session.get(Favorite, favorite_id)
        db.session.delete(favorite)
        session.modified = True
        db.session.commit()
        return False
        
    else:
        favorite = Favorite(
        user_id=user_id,
        trail_id=trail_id,
    )
        db.session.add(favorite)
        db.session.commit()
        return True

#################################################################################

                    # Coordinates/Geolocating Functions

#################################################################################

def add_state_coords_to_session():
    """Get the coords for a state and add the longitude and latitude to the session"""
    geolocator = Nominatim(user_agent="hikeaday")
    geocode = partial(geolocator.geocode, exactly_one=True)
    location = geolocator.geocode(f"{session['state_name']}, United States")
    session['state-lat'] = float(location.latitude)
    session['state-lng'] = float(location.longitude)






#################################################################################

                            # Trail Functions

#################################################################################


def create_trail(trail_id,
                name,
                area_name,
                city_name,
                state_name,
                country_name,
                _geoloc,
                popularity,
                length,
                elevation_gain,
                difficulty_rating,
                route_type,
                visitor_usage,
                avg_rating,
                num_reviews,
                features,
                activities
                ):
    """Create a new instance of trail in the Trail class"""
    
    trail=Trail(
        trail_id=trail_id,
        name=name,
        area_name=area_name,
        city_name=city_name,
        state_name=state_name,
        country_name=country_name,
        _geoloc=_geoloc,
        popularity=popularity,
        length=length,
        elevation_gain=elevation_gain,
        difficulty_rating=difficulty_rating,
        route_type=route_type,
        visitor_usage=visitor_usage,
        avg_rating=avg_rating,
        num_reviews=num_reviews,
        features=features,
        activities=activities,
    )
    db.session.add(trail)
    db.session.commit()
    return trail

def search_trails(search):
    response = Trail.query.filter(Trail.state_name == search).all()
    return (response)

def get_trail_name_by_trail_id(trail_id):
    trail_name = db.session.query(Trail).filter(Trail.trail_id == trail_id).all()
    
    return trail_name

def get_all_trail_names_for_favorited_trails(user_id):
    """Get all the favorites for the user in the Flask session"""

    favorites = Favorite.query.filter(User.user_id == user_id).all()

    trail_names_list = []
    for favorite in favorites:
        trails = db.session.query(Trail).filter(Trail.trail_id == favorite.trail_id).all()
        for trail in trails:
            if favorite.trail_id == trail.trail_id:
                
                date = str(favorite.created_at)
                create_date = date[:10]
                
                fav_info = {
                    'trail_name' : trail.name,
                    'trail_city' : trail.city_name,
                    'trail_state' : trail.state_name,
                    'created' : create_date
                }
                
                trail_names_list.append(fav_info)
    return trail_names_list

#################################################################################

                            # Image Functions

#################################################################################


################## Image Instantiating ##################

def add_trail_image(trail_id, image_url):
    """Add a trail image"""
    new_image = Images(
        image_url = image_url,
        trail_id = trail_id
    )
    db.session.add(new_image)
    db.session.commit()

def add_all_trail_images():
    all_trail_ids = db.session.query(Trail.trail_id).all()
    for trail_id in all_trail_ids:
        check_if_trail_images_are_populated(trail_id[0])

def add_user_image(user_id, image_url):
    """Add a user image"""
    new_image = Images(
        image_url = image_url,
        user_id = user_id
    )
    db.session.add(new_image)
    db.session.commit()

def add_user_trail_image(user_id, image_url, trail_id):
    """Add a user-submitted trail image"""
    new_image = Images(
        image_url = image_url,
        user_id = user_id, 
        trail_id = trail_id
    )
    db.session.add(new_image)
    db.session.commit()

def save_map_markers():
    trails_data = []

    all_trails = db.session.query(Trail).all()
    for trail in all_trails:
        coords = eval(trail._geoloc)
        lat = coords['lat']
        lng = coords['lng']
        image_url = db.session.query(Images.image_url).filter(Images.trail_id == trail.trail_id).first()

        elevation_gain = str(int(trail.elevation_gain))+ " " + 'feet'
        route_type = trail.route_type.title()
        trail_length = "{:.2f}".format(trail.length/5280)
        formatted_trail_length = str(trail_length) + " " + "miles"
        image_string = str(image_url)
        img = eval(image_string)

        trail_info = {
            "name": trail.name,
            "city" : trail.city_name,
            "area_name" : trail.area_name,
            'lat' : lat,
            'lng' : lng,
            'elevation_gain' : elevation_gain,
            'difficulty_rating' : trail.difficulty_rating,
            'route_type' : route_type,
            'length' : formatted_trail_length,
            "image_url" : img[0],
        }
        trails_data.append(trail_info)
    json_trails_data = json.dumps(trails_data)
    add_user_image(2, json_trails_data)




################## Image crud Functions ##################

def populate_trail_images(trail_id):
    """Populates the database with trail images from Bing images. 
                                See API documentaion here:
        https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/bing-image-search1 """

    trail_name = str(db.session.query(Trail.name).filter(Trail.trail_id == trail_id).first())
    area_name = str(db.session.query(Trail.area_name).filter(Trail.trail_id == trail_id).first())
    geolocation = str(db.session.query(Trail._geoloc).filter(Trail.trail_id == trail_id).first())
    state_name = str(db.session.query(Trail.state_name).filter(Trail.trail_id == trail_id).first())

    query = f'{trail_name} trail in {state_name}'

    url = "https://bing-image-search1.p.rapidapi.com/images/search"

    querystring = {"q":query,"count":"10","offset":"0","mkt":"en-US"}

    headers = {
        "X-RapidAPI-Host": "bing-image-search1.p.rapidapi.com",
        "X-RapidAPI-Key": IMAGE_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    
    if response:
        image_dict = response.json()
        list_of_dicts = image_dict['value']
        list_of_image_urls = []
        for dict in list_of_dicts:
            
            list_of_image_urls.append(dict.get('contentUrl'))

        for url in list_of_image_urls:
            add_trail_image(trail_id, url)
    

def check_if_trail_images_are_populated(trail_id):
    """Check the database to see if images have been populated
    for the trail already, and if not, adds images to trail details from Google Images"""
    image_check = db.session.query(Images).filter(Images.trail_id == trail_id).all()
    if not image_check:
        populate_trail_images(trail_id)

        
def get_all_trail_images_for_current_trail(trail_id):
    check_if_trail_images_are_populated(trail_id)
    images_list = db.session.query(Images.image_url).filter(Images.trail_id == trail_id).all()
    return(images_list)

    
    
    
#################################################################################

                            # Review Functions

#################################################################################

def create_review(user_id, trail_id, num_stars, review_text):
    """Instantiate a Review / Create a Review"""
    
    review=Review(
        user_id=user_id,
        trail_id=trail_id,
        num_stars=num_stars,
        review_text=review_text
    )
    db.session.add(review)
    db.session.commit()
    return review


def did_user_review(user_id, trail_id):
    """See if a user reviewed the current trail in the Flask session"""
    
    user_reviews_dict = get_all_current_user_reviews(user_id)
    all_trail_ids = set()
    for review in user_reviews_dict:
        all_trail_ids.add(review['trail_id'])
    if trail_id in all_trail_ids:
        return True
    else:
        return False
    
def get_all_current_user_reviews(user_id):
    """Get all the reviews for the user in the Flask session"""

    current_user_review_ids = db.session.query(
        Review.trail_id, 
        Review.review_id, 
        Review.review_text,
        Review.created_at,
        Review.user_id).filter(
            Review.user_id == user_id).all()
    
    reviews_list = []
    for review in current_user_review_ids:
        created_date = str(review[3])[:11]
        trail = db.session.query(Trail).filter(Trail.trail_id == review[0]).first()

        review_dict = {
            'review_id' : review[1],
            'trail_id' : review[0],
            'text' : review[2],
            'created_date' : created_date,
            'user_id' : review[4],
            'trail_name' : trail.name,
            'trail_city' : trail.city_name,
            'trail_state' : trail.state_name
                }
        reviews_list.append(review_dict)
    return reviews_list

def get_all_reviews_by_current_trail(trail_id):
    trail_reviews = db.session.query(Review.user_id, 
                                    Review.review_text,
                                    Review.created_at,
                                    Review.review_id).filter(
                                    Review.trail_id == trail_id).all()
                                 
    list_of_trail_reviews = []
    for review in trail_reviews:
        username = db.session.query(User.username).filter(User.user_id == review[0]).first()
        date = str(review[2])
        review_dict = {
            'user_id' : review[0],
            'review_text' : review[1],
            'created_at' : date[:10],
            'review_id' : review[3],
            'username' : username[0],
        }
        list_of_trail_reviews.append(review_dict)
    print(list_of_trail_reviews)
    return list_of_trail_reviews
    
def get_user_review_for_current_trail(user_id, trail_id):
    current_user_review_ids = db.session.query(Review.trail_id,
                                               Review.review_id,
                                               Review.review_text).filter(
                                                    Review.user_id == user_id).all()
    reviews_dict = {}
    for review in current_user_review_ids:
        reviewid = review[1]
        trailid = review[0]
        reviewtext = review[2]
        reviews_dict[trailid]=reviewtext
    if trail_id in reviews_dict:
        review = reviews_dict[trail_id]
        return review

def get_user_review_id_for_current_trail(user_id, trail_id):
    current_user_review_ids = db.session.query(Review.trail_id,
                                               Review.review_id,
                                               Review.review_text).filter(
                                                   Review.user_id == user_id).all()
    """Get the review ID for the current trail in the Flask session"""                                               
    reviews_dict = {}
    for review in current_user_review_ids:
        reviewid = review[1]
        trailid = review[0]
        reviews_dict[trailid]=reviewid
    if trail_id in reviews_dict:
        reviewid = reviews_dict[trail_id]
        return reviewid

def edit_review(edited_review, user_id, trail_id):
    """Edit the review for the current trail in the Flask session"""
    
    reviewid = get_user_review_id_for_current_trail(user_id, trail_id)
    query = db.session.query(Review).filter(Review.review_id == reviewid).first()
    query.review_text = edited_review
    session.modified = True
    db.session.commit()


def get_features(trail_id):
    features = db.session.query(Trail.features).filter(Trail.trail_id == trail_id).first()

    feature = features._asdict()
    features_list = feature["features"].strip('}{').split(',')
    if 'dogs' in features_list[0].lower():
        dogs_allowed = features_list[0].split('-')
        
        if dogs_allowed[1].lower() == "yes":
            formatted_dogs_allowed = "Dogs Allowed"
            features_list[0] = formatted_dogs_allowed
        else:
            formatted_dogs_allowed = "No Dogs"
            features_list[0] = formatted_dogs_allowed
    
    for i in range(len(features_list)):
        if features_list[i] == 'Kids':
            features_list[i]= 'Family-Friendly'
        if features_list[i] == 'Views':
            features_list[i]= 'Good Views'

    return features_list

def get_activities(trail_id):
    activities = db.session.query(Trail.activities).filter(Trail.trail_id == trail_id).first()

    activity = activities._asdict()
    activities_list = activity["activities"].strip('}{').split(',')
    dogs_allowed = activities_list[0].split('-')

    return activities_list
 
    

#################################################################################

                            # Database Functions

#################################################################################

def _populate_db():
    """Populate the database"""
    trails_list = []

    filepath = 'national_park_data.csv'
    input_file = csv.DictReader(open(filepath))

    for row in input_file:
        trails_list.append(row)        
    
    for trail in trails_list:
        new_trail = Trail(
            trail_id = trail.get('trail_id'),
            name = trail.get('name'),
            area_name = trail.get('area_name'),
            city_name = trail.get('city_name'),
            state_name = trail.get('state_name'),
            country_name = trail.get('country_name'),
            _geoloc = trail.get('_geoloc'),
            popularity = trail.get('popularity'),
            length = trail.get('length'),
            elevation_gain = trail.get('elevation_gain'),
            difficulty_rating = trail.get('difficulty_rating'),
            route_type = trail.get('route_type'),
            visitor_usage = trail.get('visitor_usage'),
            avg_rating = trail.get('avg_rating'),
            num_reviews = trail.get('num_reviews'),
            features = trail.get('features').strip('][').strip("'").replace("'", "").title().split(', '),
            activities = trail.get('activities').strip('][').strip("'").replace("'", "").title().split(', '),
        )
        db.session.add(new_trail)
        db.session.commit()

def _drop_db():
    os.system('pg_dump hikeaday > hikeaday.sql')
    os.system("dropdb hikeaday")
    os.system("createdb hikeaday")
    os.system('psql hikeaday < hikeaday.sql')
    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
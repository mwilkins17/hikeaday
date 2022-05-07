"""CRUD operations."""

import re, datetime, json, requests, csv, os, model
from model import db, User, Favorite, Trail, Review, Images, connect_to_db
from flask import session
from datetime import datetime

# Functions start here!

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
    print(is_Favorited)
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
    print(f'@@@@@@@@@@@@@@@@@{is_favorite}@@@@@@@@@@@@@@@@@@@')
    if is_favorite:
        # Favorite.query.filter(Favorite.favorite_id == favorite_id).delete()
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
        trail_name = db.session.query(Trail.name).filter(Trail.trail_id == favorite.trail_id).first()
        trail_names_list.append(trail_name._asdict())
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

################## Image crud Functions ##################

def populate_trail_images(trail_id):
    """Populates the database with trail images from Google images via the USearch API. 
                                See API documentaion here:
        https://rapidapi.com/contextualwebsearch/api/web-search?endpoint=apiendpoint_2799d2c8-3abb-4518-a544-48d2c32d6662 """
    
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
    trail_name = str(db.session.query(Trail.name).filter(Trail.trail_id == trail_id).first())
    area_name = str(db.session.query(Trail.area_name).filter(Trail.name == session['trail_name']).first())
    state_name = str(db.session.query(Trail.state_name).filter(Trail.name == session['trail_name']).first())
    querystring = {"q":f"{trail_name}","pageNumber":"1","pageSize":"1","autoCorrect":"true"}

    headers = {
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "b3e7a39b62mshf47ba523448c846p1cc65ajsn96fab1a929f5"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response:
        image_dict = response.json()
        print(image_dict)
        list_of_dicts = image_dict['value']
        list_of_image_urls = []
        for dict in list_of_dicts:
            list_of_image_urls.append(dict.get('url'))
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
    # trail_names_list.append(trail_name._asdict())
    
    
    
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
    if user_id:
        print(True if trail_id in user_reviews_dict.keys() else False)
    if trail_id in user_reviews_dict.keys():
        return True
    else:
        return False
    
def get_all_current_user_reviews(user_id):
    """Get all the reviews for the user in the Flask session"""
    
    user = User.query.filter(User.user_id == user_id).first()
    current_user_review_ids = db.session.query(
        Review.trail_id, 
        Review.review_id, 
        Review.review_text).filter(
            Review.user_id == user_id).all()
        
    reviews_dict = {}
    for review in current_user_review_ids:
        reviewid = review[0]
        trailid = review[1]
        reviewtext = review[2]
        reviews_dict[reviewid]=(trailid, reviewtext)
    return reviews_dict

def get_all_reviews_by_current_trail(trail_id):
    trail_reviews = db.session.query(Review.user_id, 
                                    Review.review_text).filter(
                                    Review.trail_id == trail_id).all()
                                    
    list_of_trail_reviews = []
    
    for review in trail_reviews:
        list_of_trail_reviews.append(review[1])
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


def get_features():
    trails_list = []

    filepath = 'national_park_data.csv'
    input_file = csv.DictReader(open(filepath))

    for row in input_file:
        trails_list.append(row)
    for trail in trails_list:
        features = trail.get('features').strip('][').strip("'").replace("'", "").title().split(', ')
        return features

def get_activities():
    trails_list = []

    filepath = 'national_park_data.csv'
    input_file = csv.DictReader(open(filepath))

    for row in input_file:
        trails_list.append(row)
    for trail in trails_list:
        activities = trail.get('activities').strip('][').strip("'").replace("'", "").title().split(', ')
        return activities
    

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
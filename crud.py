"""CRUD operations."""

import re
from model import db, User, Favorite, Trail, Review, connect_to_db
import json
import requests
import csv
import os
import model
from flask import session

# Functions start here!

#################################################################################
#                                                                               #
#                            User Queries                                       #
#                                                                               #
#################################################################################


def create_user(fname, lname, email, username, password):
    """Create and return a new user."""

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
    """Gets a username from the db by ID"""
    user_id = User.query.get(User.user_id).where(User.username == username)
    return user_id



def get_user_by_username(username):
    """Checks the db for a username"""
    
    return User.query.filter(User.username == username).first()



def get_user_by_email(email):
    """Return a User by Email"""
    
    return User.query.filter(User.email == email).first()
    
    
#################################################################################

                            # Favorite Queries

#################################################################################

def create_favorite(user_id, trail_id):
    
    favorite = Favorite(user_id=user_id,
                        trail_id=trail_id)
    
    return favorite


#################################################################################

                            # Trail Queries

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


def create_review(user_id, trail_id, num_stars, review_text):
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
    test = None
    user_reviews_dict = get_all_current_user_reviews(user_id)
    if user_id:
        print(True if trail_id in user_reviews_dict.keys() else False)
    if trail_id in user_reviews_dict.keys():
        return True
    else:
        return False
    
def get_all_current_user_reviews(user_id):
    #Get a user object#
    
    user = User.query.filter(User.user_id == user_id).first()
    current_user_review_ids = db.session.query(Review.trail_id, Review.review_id, Review.review_text).filter(Review.user_id == user_id).all()
    reviews_dict = {}
    for review in current_user_review_ids:
        reviewid = review[0]
        trailid = review[1]
        reviewtext = review[2]
        reviews_dict[reviewid]=(trailid, reviewtext)
    return reviews_dict

def get_all_reviews_by_current_trail(trail_id):
    trail_reviews = db.session.query(Review.user_id, Review.review_text).filter(Review.trail_id == trail_id).all()
    list_of_trail_reviews = []
    for review in trail_reviews:
        list_of_trail_reviews.append(review[1])
    return list_of_trail_reviews
    
def get_user_review_for_current_trail(user_id, trail_id):
    current_user_review_ids = db.session.query(Review.trail_id, Review.review_id, Review.review_text).filter(Review.user_id == user_id).all()
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
    current_user_review_ids = db.session.query(Review.trail_id, Review.review_id, Review.review_text).filter(Review.user_id == user_id).all()
    reviews_dict = {}
    for review in current_user_review_ids:
        reviewid = review[1]
        trailid = review[0]
        reviewtext = review[2]
        reviews_dict[trailid]=reviewid
    if trail_id in reviews_dict:
        reviewid = reviews_dict[trail_id]
        return reviewid

def edit_review(edited_review, user_id, trail_id):
    reviewid = get_user_review_id_for_current_trail(user_id, trail_id)
    query = db.session.query(Review).filter(Review.review_id == reviewid).first()
    query.review_text = edited_review
    session.modified = True
    db.session.commit()


def get_favorites_by_user():
    
    return Favorite.query.filter(User.user_id == Favorite.user_id).all()


def populate_db():

    trails_list = []

    filepath = 'national_park_data.csv'
    input_file = csv.DictReader(open(filepath))

    for row in input_file:
        trails_list.append(row)
    

        
    
    for trail in trails_list:
        def title_features():
            features = trail.get('features')
            features = features.strip('][').split(', ')
            for elem in features:
                elem = elem.title()
                print(elem)
            return features

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


def search_trails(search):
    response = Trail.query.filter(Trail.state_name == search).all()
    return (response)
        

def drop_db():
    os.system("dropdb hikeaday")
    os.system("createdb hikeaday")
    # os.system("python3 model.py db.create_all")
    model.db.create_all()
    populate_db()
    new_user = User(
        fname="Mason",
        lname="Wilkins",
        email="mwilkins17@gmail.com",
        username="maysun717",
        password="password"
    )
    new_user2 = User(
        fname="Bob",
        lname="Wilkins",
        email="bob@gmail.com",
        username="bob",
        password="password"
    )
    new_review1 = Review(
        user_id=1,
        trail_id = 10337353,
        num_stars = 3,
        review_text = "This is a review. and a good one"
    )
    
    new_review2 = Review(
        user_id=1,
        trail_id = 10041313,
        num_stars = 4,
        review_text = "This is the second review. YEAAAA"
    )
    new_review3 = Review(
        user_id=1,
        trail_id = 10004435,
        num_stars = 5,
        review_text = "This is the third review. Woooooooooooooot"
    )
    new_review4 = Review(
        user_id=1,
        trail_id = 10004435,
        num_stars = 5,
        review_text = "This is the third review. Woooooooooooooot"
    )
    
    db.session.add(new_user)
    db.session.add(new_user2)
    db.session.add(new_review1)
    db.session.add(new_review2)
    db.session.add(new_review3)
    db.session.commit()    


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
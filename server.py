from crypt import methods
from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for
from random import choice 
import http.client, json, requests
from model import connect_to_db, db, Trail, User, Favorite, Review
import crud


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
    results = crud.search_trails(search)

    return render_template('trails.html', results = results)


#   ----------------------------------------------------------------

#       RENDER TRAILS.HTMLTEMPLATE & DISPLAY TRAIL DETAILS,
#          TRAIL REVIEWS, AND (EVENTUALLY) TRAIL WEATHER

#   ----------------------------------------------------------------


@app.route("/trails/<trail_name>")
def trail_details(trail_name):
    """######## Get the details page of a trail ########"""
    
    
    session['trail_name'] = trail_name
    trail_name = session['trail_name']
    print(session['trail_name'])
    features = crud.get_features()
    activities = crud.get_activities()
    
    trail = Trail.query.filter(Trail.name == trail_name).first()
    
    results = crud.search_trails(trail_name)
    
    
    trail_id = trail.trail_id
    session['trail_id'] = trail_id
    
    username = session['username']

    user = User.query.filter(User.username == username).first()
    
    all_reviews = db.session.query(Review.review_text).filter(Review.trail_id == trail_id).all()
    
    
    reviews = crud.get_all_reviews_by_current_trail(trail_id)
    user_reviews_dict = crud.get_all_current_user_reviews(trail_id)
    
    
    if session['user_id']:
        user_id = session['user_id']
        user_review = db.session.query(Review.review_text).filter(Review.user_id == user_id, Review.trail_id.in_(user_reviews_dict.values()))
        print(user_reviews_dict.keys())
        print(user_review)
        print(all_reviews)
        reviewed = crud.did_user_review(user_id, trail_id)

        review_text = crud.get_user_review_for_current_trail(user_id, trail_id)

        return render_template("/trail_details.html", reviewed=reviewed, review_text=review_text, reviews=reviews, trail=trail, features=features, activities=activities)
    
    else:
        reviewed=False
        return render_template("/trail_details.html", reviewed=reviewed, trail=trail, reviews=reviews, features=features, activities=activities)
        
    # else:
    #     return redirect("/trails")
    
    
    # return render_template('trail_details.html', features=features, activities=activities, trail=trail, results=results)


@app.route("/trails/<trail_name>", methods=["POST"])
def submit_review(trail_name):
    
    features = crud.get_features()
    activities = crud.get_activities()
    
    trail_name = session['trail_name']
    trail = Trail.query.filter(Trail.name == trail_name).first()
    
    trail_id = trail.trail_id
    session['trail_id'] = trail_id
    
    username = session['username']
    session['username'] = username
    user = User.query.filter(User.username == username).first()
    
    user_id = session['user_id']
    
    review = request.form.get("new-review")
    reviews = crud.get_all_reviews_by_current_trail(trail_id)
    
    user_reviews_dict = crud.get_all_current_user_reviews(user_id)

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
                    return redirect(f"/trails/{trail_name}")
                
                
                return render_template("/trail_details.html", reviewed=reviewed, review_text=review_text, trail=trail, reviews=reviews, features=features, activities=activities)
        else:
            crud.create_review(user_id=user_id, trail_id=trail_id, num_stars=4, review_text=review)
            return redirect(f'/trails/{trail_name}')
    
    else:
        reviewed = False
        return render_template("/trail_details.html", reviewed=reviewed, trail=trail, reviews=reviews, features=features, activities=activities)
    

###############################################################################
#                                                                             #
#                      USER AUTHENTICATION ROUTES                             #
#                                                                             #
###############################################################################

@app.route("/sign-up")
def sign_up():
    
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
            
        elif password != password_repeat:
            flash("Password do not match")
            return redirect("/sign-up")

        else:
            user = crud.create_user(fname.title(), lname.title(), email, username, password)
            db.session.add(user)
            db.session.commit()

            flash("User created successfully; you may now log in")
            
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
        return render_template("base.html")
    
    return redirect("/")


@app.route("/logout")
def logout():
    """######## Log a user out and remove everything from session ########"""
    
    session['username'] = None
    session['user_id'] = None
    session['trail_id'] = None
    session['username'] = None
    
    flash("You have been logged out. See you next time!")
    return render_template("/base.html")


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
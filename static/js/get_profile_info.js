fetch('/profile-info')
    .then(response => response.json())
    .then(profileData => {
        document.getElementById("profile-info").innerHTML = 
        (`<div class="col-lg-8 col-md-auto text-center mx-auto">
            <div class="card mb-4">
                <div class="card-body">
                    <div class="row">
                        <div class="col-sm-3">
                            <p class="mb-0">Full Name</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">${profileData.fname} ${profileData.lname}</p>
                        </div>
                    </div>
                        <hr/>
                    <div class="row">
                        <div class="col-sm-3">
                            <p class="mb-0">Email</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">${profileData.email}</p>
                        </div>
                    </div>
                        <hr/>
                    <div class="row">
                        <div class="col-sm-3">
                            <p class="mb-0">Phone</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">${profileData.phone}</p>
                        </div>
                    </div>
                        <hr/>
                    <div class="row">
                        <div class="col-sm-3">
                            <p class="mb-0">Mobile</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">(098) 765-4321</p>
                        </div>
                    </div>
                        <hr/>
                </div>
            </div>
        </div>`)
    })



function getProfileInfo() {
    fetch('/profile-info')
    .then(response => response.json())
    .then(profileData => {

    document.getElementById("profile-info").innerHTML = 
        (`<div class="col-lg-8 col-md-auto text-center mx-auto">
            <div class="card mb-4">
                <div class="card-body">
                    <div class="row">
                        <div class="col-sm-3">
                            <p class="mb-0">Full Name</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">${profileData.fname} ${profileData.lname}</p>
                        </div>
                    </div>
                        <hr/>
                    <div class="row">
                        <div class="col-sm-3">
                            <p class="mb-0">Email</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">${profileData.email}</p>
                        </div>
                    </div>
                        <hr/>
                    <div class="row">
                        <div class="col-sm-3">
                            <p class="mb-0">Phone</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">${profileData.phone}</p>
                        </div>
                    </div>
                        <hr/>
                    <div class="row">
                        <div class="col-sm-3">
                            <p class="mb-0">Mobile</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">(098) 765-4321</p>
                        </div>
                    </div>
                        <hr/>
                </div>
            </div>
        </div>`)
        }
    // ^ for fetch
    )
//  ^ for .then
}
// ^ for end of function

document.getElementById("profile--info").addEventListener("click", getProfileInfo);

function getUserReviews() {
    fetch('/profile-info')
    .then(response => response.json())
    .then(profileData => {
    document.getElementById('profile-info').innerHTML = "";
    let reviews = profileData.user_reviews
    if (reviews) {
        for (let review of reviews) {
            document.getElementById("profile-info").insertAdjacentHTML("beforeend", 
            `<div class="overflow-auto p-3 bg-light" style="border-style: solid;">
                <div class="container">
                    <div class="row">
                        <div class='col-12 text-center'>
                            <a href="/trails/${review.trail_name}">${review.trail_name}</a> in ${review.trail_city}, ${review.trail_state}
                        </div>
                        <div class="col-12" style='text-align: center'>
                        Created On: ${review.created_date}<br/><br/>
                            <h5>${review.text}</h5>
                        </div>
                        <div class='row justify-content-around'>
                            <div class='col-4'>
                                
                            </div>
                            <div style="text-align:right" class='col-6'>
                            <div class="col-12" style="text-align:right">
                            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editReviewModal">
                                Edit Review  
                            </button>
                            <div class="modal fade" id="editReviewModal" tabindex="-1" role="dialog" aria-labelledby="editReviewModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-lg" role="document">
                                    <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="editReviewModalLabel">Edit Your Review</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="form-group">
                                            <form id="review--form">
                                                <div style="text-align:center; width:450px; margin-right: auto; margin-left: auto;">
                                                    <textarea id="edited--review" 
                                                    style="text-align: center; width: 450px; height: 300px" name="edit-review" type="text">${review.text}</textarea>
                                                </div><br>
                                                <script src="../static/js/editReview.js"></script>
                                                <div style="padding: 15px" class="row justify-content-between">
                                                    <div class="col-lg-auto">
                                                        <button id="delete--review" type="submit" class="btn btn-danger">
                                                            Delete Review
                                                        </button>
                                                    </div>
                                                    <div class="col-md-auto">
                                                        <button id="edit--review" type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save changes</button>
                                                        <button id="cancel--edit" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                                    </div>
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            `)
                }
            }
    else {
        document.getElementById('profile-info').innerHTML = '<div><h1>You have not made any reviews yet</h1></div>'
    }}
    // ^ for fetch
    );
//  ^ for .then
}
// ^ for end of function

document.getElementById("user--reviews").addEventListener("click", getUserReviews);

function getUserFavorites() {
    fetch('/profile-info')
    .then(response => response.json())
    .then(profileData => {
    document.getElementById('profile-info').innerHTML = "";
    let favorites = profileData.user_favorites
    if (favorites) {
        for (let favorite of favorites) {
            document.getElementById("profile-info").insertAdjacentHTML("beforeend",
             `<div class="overflow-auto p-3 bg-light" style="border-style: solid;">
             <a href="/trails/${favorite.name}">${favorite.name}</a>
             </div>`);
                }
            }
    else {
        document.getElementById('profile-info').innerHTML = '<div><h1>You have not made any favorites yet</h1></div>'
    }}
    // ^ for fetch
    );
//  ^ for .then
}
// ^ for end of function

document.getElementById("user--favorites").addEventListener("click", getUserFavorites);
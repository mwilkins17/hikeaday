fetch('/profile-info')
    .then(response => response.json())
    .then(profileData => {
        document.getElementById("profile-info").innerHTML = 
        (`<div class="col-lg-8 col-md-auto text-center mx-auto shadow p-3 mb-5 bg-white rounded" >
            <div class="card mb-4" style="border-style: solid;">
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
                            <p class="mb-0">Username</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">${profileData.username}</p>
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
        (`<div class="col-lg-8 col-md-auto text-center mx-auto shadow p-3 mb-5 bg-white rounded" >
            <div class="card mb-4" style="border-style: solid;">
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
                            <p class="mb-0">Username</p>
                        </div>
                        <div class="col-sm-9">
                            <p class="text-muted mb-0">${profileData.username}</p>
                        </div>
                    </div>
                        <hr/>
                </div>
            </div>
        </div>`)
        }
    )
}

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
            `<div class="overflow-auto rounded bg-light shadow p-3 mb-5 bg-white rounded" style="border-style: solid;">
                <div class="container">
                    <div class="row">
                        <div class='col-12 text-center'>
                            <div class="overflow-auto text-center">
                                <h3><a href="/trails/${review.trail_name}">${review.trail_name}</a></h3>
                                    <h5> ${review.trail_city}, ${review.trail_state}</h5>
                                        <p>Reviewed on ${review.created_date}</p><br>
                                <h5>${review.text}</h5>
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
    );
}

document.getElementById("user--reviews").addEventListener("click", getUserReviews);

function getUserFavorites() {
    fetch('/profile-info')
    .then(response => response.json())
    .then(profileData => {
    document.getElementById('profile-info').innerHTML = "";
    let favorites = profileData.favorites
    if (favorites) {
        for (let favorite of favorites) {
            console.log(favorite)
            document.getElementById("profile-info").insertAdjacentHTML("beforeend",
             `<div class="overflow-auto shadow p-3 mb-5 bg-white rounded text-center" style="border-style: solid;">
                <h3><a href="/trails/${favorite.trail_name}">${favorite.trail_name}</a></h3>
                    <h5> ${favorite.trail_city}, ${favorite.trail_state}</h5>
                <p>Favorited on ${favorite.created}</p>
             </div>`);
                }
            }
    else {
        document.getElementById('profile-info').innerHTML = '<div class="text-center"><h1>You have not favorited any trails yet</h1></div>'
    }}
    );
}

document.getElementById("user--favorites").addEventListener("click", getUserFavorites);


// For later:
/* <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editReviewModal">
                                Edit Review  
                            </button>
                            <div class="modal fade" id="editReviewModal" tabindex="-1" role="dialog" aria-labelledby="editReviewModalLabel" aria-hidden="true">
                                <div class="modal-dialog modal-lg" role="document">
                                    <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="editReviewModalLabel">Edit Your Review for ${review.trail_name}</h5>
                                        <span id="trail_name" style="display:none">${review.trail_name}</span>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="form-group">
                                            <form id="review--form">
                                                <div style="text-align:center; width:450px; margin-right: auto; margin-left: auto;">
                                                    <textarea id="edited--review" 
                                                    style="text-align: center; width: 450px; height: 300px" name="edit-review" type="text">${review.text}</textarea>
                                                </div><br>
                                                <div style="padding: 15px" class="row justify-content-between">
                                                    <div class="col-lg-auto">
                                                        <button id="delete--review" type="submit" class="btn btn-danger">
                                                            Delete Review
                                                        </button>
                                                    </div>
                                                    <div class="col-md-auto">
                                                        <button id="this--review" type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save changes</button>
                                                        <button id="cancel--edit" type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                                    </div>
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                            </div> */
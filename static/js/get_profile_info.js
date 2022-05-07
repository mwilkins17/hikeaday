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
                ${review}<br/><br/>
                <span style="align-text: right;">
                    <button class="btn btn-outline-primary">Edit Review</button>
                </span>
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
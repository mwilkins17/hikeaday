function LoginLogout() {

    const [isLoggedIn, setIsLoggedIn] = React.useState(true)

    function changeLogin() {
        setIsLoggedIn(prevState => !prevState)
    }

    let logged

    if (isLoggedIn === false) {
        logged = 'login'
    }
    else {
        logged = 'logout'
    }

    return (
        <div onClick={changeLogin}>
            <a class="nav-btn" id="rightnav login" href={"/" + logged} >{isLoggedIn ? "Login" : "Logout"}</a>
        </div>
    )
}

ReactDOM.render(<LoginLogout />, document.getElementById("login"))
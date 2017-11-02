function showHideMenu() {
    var navigationBar = document.getElementById("nav-icon");
    if (navigationBar.className === "top-nav") {
        navigationBar.className = "hide";
    } else {
        navigationBar.className = "top-nav";
    }
}

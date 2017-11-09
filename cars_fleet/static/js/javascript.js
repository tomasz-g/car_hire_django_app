/* show/hide navigation menu on small devices */
function showHideMenu() {
    var navigationBar = document.getElementById("nav-icon");
    if (navigationBar.className === "top-nav") {
        navigationBar.className = "hide";
    } else {
        navigationBar.className = "top-nav";
    }
}

/* add class 'çurrent' to header navigation menu button of current page */
$(document).ready(function() {
  $('nav.top-nav > a.current').removeClass('current');
  $('a[href="' + location.pathname + '"]').closest('nav.top-nav > a').addClass('current');
});

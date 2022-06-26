
function hide_navbar() {
  var burgerIco = document.querySelector('#navbar-burger');
  var navbarMenu = document.querySelector('#nav-links');
  navbarMenu.classList.toggle('hidden');
  window.addEventListener('scroll', window.scrollTo(0,0));
}

//burgerIco.addEventListener('click', function(){hide_navbar()});

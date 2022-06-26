function hide_show(id) {
  id.classList.toggle('hidden');
  window.addEventListener('scroll', window.scrollTo(0,0));
}

//user_img.addEventListener('click', function(){hide_show(menu_user)});
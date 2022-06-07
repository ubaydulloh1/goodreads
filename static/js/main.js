document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  
    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {
  
      // Add a click event on each of them
      $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {
  
          // Get the target from the "data-target" attribute
          const target = el.dataset.target;
          const $target = document.getElementById(target);
  
          // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
          el.classList.toggle('is-active');
          $target.classList.toggle('is-active');
  
        });
      });
    }
  
  });

  // Messages delete click
document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    const $notification = $delete.parentNode;

    $delete.addEventListener('click', () => {
      $notification.parentNode.removeChild($notification);
    });
  });
});


let review_edit_delete = document.querySelectorAll(".review__context__menu")
for (let i=0; i<=review_edit_delete.length; i++) {
  review_edit_delete[i].addEventListener("click", ()=>{
    console.log('DELETE CLiCKED!!!')
    review_edit_delete[i].classList.toggle("is-active")
  })
}



// Pagination JS code

    let = search__from = document.querySelector('.search__form')
    let p__link = document.getElementsByClassName('pagination__link')

    for(let i=0; i<=p__link.length; i++){
        p__link[i].addEventListener('click', (e) => {
            e.preventDefault();
            console.log(p__link[i], 'clicked!')
            page = e.target.dataset.page
            search__form.innerHTML += 
            `
                <input type='hidden' name='page' value='${page}' />
            `
            search__form.submit()
        })
    }

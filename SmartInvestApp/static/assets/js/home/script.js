let menu_toggle = document.querySelector('#header-logo')
let nav_link = document.querySelector('.nav-link')
console.log(menu_toggle)
console.log(nav_link)

menu_toggle.addEventListener('click', () => {

    nav_link.classList.toggle('active')

})
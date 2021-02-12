const $triggers = $('.sidemenu-trigger')
const $body = $('body')
const $pageOverlay = $('.page-overlay')


$triggers.each(function() {
  const $trigger = $(this)
  const target = $trigger.attr('data-target')
  const $menu = $(target)
  const $close = $menu.find('[data-action="close"]')

  // CSS classes indicating state of an element
  const active = 'active'
  const hidden = 'd-none'
  const menuOpen = 'sidemenu-open'

  function toggleMenu(event) {
    event.preventDefault()

    $body.toggleClass(menuOpen)
    $pageOverlay.toggleClass(hidden)
    $menu.toggleClass(active)
    $trigger.toggleClass(active)
  }

  $trigger.click(toggleMenu)
  $close.click(toggleMenu)
  $pageOverlay.click(toggleMenu)
})
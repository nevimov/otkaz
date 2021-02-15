
export function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}


/* JS analog to django.contrib.humanize.intcomma

   Examples:
   > humanize(123456789)
   '123 456 789'
   > humanize(12345, ',')
   '12,345'
   > humanize(1234.5)
   '1 234.5'
*/
export function humanizeNumber(num, sep) {
  sep = typeof sep === 'undefined' ? ' ' : sep
  const numParts = num.toString().split('.')
  let intPart = numParts[0]
  const fractPart = numParts.length > 1 ? '.' + numParts[1] : ''

  const regex = /(\d+)(\d{3})/
  while (regex.test(intPart)) {
    intPart = intPart.replace(regex, '$1' + sep + '$2')
  }

  return intPart + fractPart
}


// Return the value of the 'data-item-pk' attribute from a given element
// or one of its parents.
export function getPk(elem) {
  var $elem = $(elem)
  return $elem.closest('[data-item-pk]').data('item-pk')
}
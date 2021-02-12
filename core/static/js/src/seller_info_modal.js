const modal = document.getElementById("seller-info-modal")
const $modal = $(modal)
const $modalTitle = $(modal).find(".modal-title")
const $modalBody = $(modal).find(".modal-body")
const $modalTriggers = $(".seller-info-trigger")


function showSellerInfo(sellerId) {
  const seller = window.sellers[sellerId]
  $modalTitle.html(`${seller.public_name}`)

  let html = `
    <table class="seller-info-table">
      <tbody>
  `
  if (seller.legal_name) {
    html += `
      <tr>
        <td>Юридическое имя</td>
        <td>${seller.legal_name}</td>
      </tr>`
  }
  if (seller.OGRN) {
    html += `
      <tr>
        <td>ОГРН</td>
        <td>${seller.OGRN}</td>
      </tr>`
  }
  if (seller.INN) {
    html += `
      <tr>
        <td>ИНН</td>
        <td>${seller.INN}</td>
      </tr>`
  }
  if (seller.website) {
    html += `
      <tr>
        <td>Вебсайт</td>
        <td> <a href="${seller.website}">${seller.website}</a> </td>
      </tr>`
  }

  // List of the seller's contact phones
  html += `
      <tr>
        <td>Телефоны</td>
        <td>
  `
  seller.phones.forEach(phone => html += `
    <a href="tel:${phone.e164}">${phone.national}</a>
    <br>
  `)
  html += `
        </td>
      </tr>
    </tbody>
  </table>
  `

  // List of places owned by the seller
  html += `
    <div class="places">
      <h6 class="place-list-heading">Адреса</h6>
      <ul class="place-list">
  `
  seller.places.forEach(place => html += `
    <li class="place">
      <span class="place-type">${place.label}</span>:
      <span class="place-address">${place.address}</span>
    </li>
  `)
  html += `
    </ul>
  </div>
  `

  $modalBody.html(html)
  $modal.modal()
}


$modalTriggers.on("click", function() {
  const sellerId = $(this).attr("data-seller-pk")
  showSellerInfo(sellerId)
})
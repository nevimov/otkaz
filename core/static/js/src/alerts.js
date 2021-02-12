
export class Alert {

  constructor(opts) {
    // A string to insert inside <h5 class="modal-title"> ... </h5>
    const title = opts.title

    // A string to insert inside <div class="modal-body"> ... </div>
    const body = opts.body

    if (title === undefined || body === undefined) {
      throw "You need to pass the 'title' and 'body' options."
    }

    // A string to insert inside <div class="modal-footer"> ... </div>
    const footer = opts.footer || ''

    // Extra CSS classes (separated by whitespace) that should be added to
    // the alert modal.
    const cssClasses = opts.cssClasses || ''

    // Bootsrap modal options:
    // https://getbootstrap.com/docs/4.0/components/modal/#options
    const bsModalOpts = opts.bsModalOpts || {}
    bsModalOpts.show = false

    let alertHtml = `
      <div class="alert-modal modal ${cssClasses}" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">${title}</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">${body}</div>
    `
    if (footer) {
      alertHtml += `<div class="modal-footer">${footer}</div>`
    }
    alertHtml += `
          </div>
        </div>
      </div>
    `

    const $alert = $(alertHtml)
    $alert.prependTo('body')
    $alert.modal(bsModalOpts)
    this.$alert = $alert
  }

  toggle() {
    this.$alert.modal('toggle')
  }

  show() {
    this.$alert.modal('show')
  }

  hide() {
    this.$alert.modal('hide')
  }

  destroy() {
    this.$alert.modal('dispose')
  }

  // Manually readjust the modal's position if the height of a modal changes
  // while it is open (i.e. in case a scrollbar appears).
  readjust() {
    this.$alert.modal('handleUpdate')
  }

  get isDisplayed() {
    return !this.$alert.is(':hidden')
  }

}  // END Alert


export class SuccessAlert extends Alert {

  constructor(opts) {
    opts.cssClasses = opts.cssClasses || ''
    opts.cssClasses += ' success'
    super(opts)
  }
}

export class FailureAlert extends Alert {

  constructor(opts) {
    opts.cssClasses = opts.cssClasses || ''
    opts.cssClasses += ' failure'
    super(opts)
  }
}
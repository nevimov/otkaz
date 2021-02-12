import IMask from 'imask'

import { SuccessAlert, FailureAlert } from './alerts'


export class AjaxForm {

  constructor(selector, opts) {
    opts = opts || {}
    this.selector = selector
    this.$form = $(selector)
    this.form = this.$form.get(0)

    this.successMsg = opts.successMsg || {
      title: 'Успех!',
      body: 'Форма была успешно отправлена.'
    }
    this.serverErrorMsg = opts.serverErrorMsg || {
      title: 'Ошибка!',
      body: `При отправке формы произошла ошибка на стороне сервера.
             Пожалуйста, попробуйте позже либо свяжитесь с нами удобным для
             Вас способом.`
    }

    this.formGroupSelector = '.form-group'
    this.inputErrorsCls =  'errorlist'
    this.validInputCls = 'is-valid'
    this.invalidInputCls = 'is-invalid'

    // Array of arrays of the format: [pattern-or-string, replacement string]
    this.errorOverrides = opts.errorOverrides || []

    const submitSelector = opts.submitSelector || '[type="submit"]'
    this.$submitBtn = this.$form.find(submitSelector)
    this.submitDisabledCls = opts.submitDisabledCls || 'disabled'
    const submitAltText = opts.submitAltText || 'Подождите ...'
    this.submitAltHtml = opts.submitAltHtml || `
      <div class="spinner-border" role="status"></div>
      <span class="btn-text">${submitAltText}</span>
    `

    this.submitHandler = this.submitHandler.bind(this)
    this.postDoneHandler = this.postDoneHandler.bind(this)
    this.postFailHandler = this.postFailHandler.bind(this)
    this.postAlwaysHandler = this.postAlwaysHandler.bind(this)
    this.$form.on('submit', this.submitHandler)
  }

  submitHandler(event) {
    event.preventDefault()

    if (this.form.checkValidity() === false) {
      return
    }

    this.enterWaitingState()

    const postUrl = this.$form.attr('action')
    const postData = this.$form.serialize()

    $.post(postUrl, postData)
      .done(this.postDoneHandler)
      .fail(this.postFailHandler)
      .always(this.postAlwaysHandler)
  }

  postDoneHandler(data, textStatus, jqXHR) {
    this.resetInputValidation()
    const alert = new SuccessAlert({
      title: this.successMsg.title,
      body:  this.successMsg.body,
    })
    alert.show()
  }

  postFailHandler(jqXHR, error, textStatus) {
    if (jqXHR.status == 500) {
      const alert = new FailureAlert({
        title: this.serverErrorMsg.title,
        body:  this.serverErrorMsg.body,
      })
      alert.show()
    }

    else if (jqXHR.status == 400) {
      const formErrors = jqXHR.responseJSON.errors
      const errorOverrides = this.errorOverrides

      this.clearInputErrors()  // Prevents duplicate errors

      // Create a <ul> list of form errors and append it to the DOM.
      for (const inputName in formErrors) {
        let inputErrors = formErrors[inputName]

        let inputErrorsHtml = `<ul class="${this.inputErrorsCls}">`
        for (let i = 0; i < inputErrors.length; i++ ) {
          let error = inputErrors[i]

          // If an error matches a pattern, replace it with another error.
          // Both the pattern and the replacement are specified in
          // this.errorOverrides.
          for (let i = 0; i < errorOverrides.length; i++) {
            const pattern = errorOverrides[i][0]
            if (error === pattern || error.match(pattern)) {
              const replacement = errorOverrides[i][1]
              error = error.replace(pattern, replacement)
              break
            }

          }
          inputErrorsHtml += `<li>${error}</li>`
        }
        inputErrorsHtml += '</ul>'

        const $input = this.$form.find(`input[name="${inputName}"]`)
        const $formGroup = $input.parents(this.formGroupSelector)

        $input.removeClass(this.validInputCls)
        $input.addClass(this.invalidInputCls)
        $formGroup.after(inputErrorsHtml)
      }
    }

  }

  postAlwaysHandler(dataOrJqXHR, textStatus, errorOrJqXHR) {
    this.exitWaitingState()
  }

  enterWaitingState() {
    const $submitBtn = this.$submitBtn
    $submitBtn.data('originalHtml', $submitBtn.html())
    $submitBtn.attr("disabled", true)
    $submitBtn.addClass(this.submitDisabledCls)
    $submitBtn.html(this.submitAltHtml)
  }

  exitWaitingState() {
    const $submitBtn = this.$submitBtn
    const originalHtml = $submitBtn.data('originalHtml')
    $submitBtn.html(originalHtml)
    $submitBtn.attr("disabled", false)
    $submitBtn.removeClass(this.submitDisabledCls)
  }

  clearInputErrors() {
    // Remove all the form errors from the DOM
    const $inputErrors = this.$form.find('.' + this.inputErrorsCls)
    $inputErrors.remove()
  }

  resetInputValidation() {
    this.clearInputErrors()

    this.$form.find('input').removeClass(
      `${this.invalidInputCls} ${this.validInputCls}`
    )
  }

}  // END AjaxForm


export class ModalAjaxForm extends AjaxForm {

  constructor(selector, opts) {
    opts = opts || {}
    super(selector, opts)

    const modalSelector = opts.modalSelector || '.modal'  // The modal is searched among the form's parents
    const $modal = this.$form.parents(modalSelector)

    const modalOpts = opts.modalOpts || {}
    modalOpts.show = false

    this.$modal = $modal.modal(modalOpts)
  }

  postDoneHandler(data, textStatus, jqXHR) {
    super.postDoneHandler(data, textStatus, jqXHR)
    this.closeModal()
  }

  postFailHandler(jqXHR, error, textStatus) {
    super.postFailHandler(jqXHR, error, textStatus)

    if (jqXHR.status == 500) {
      this.closeModal()
    }
  }

  closeModal() {
    this.$modal.modal('hide')
  }
}


// *** Init AJAX forms ***
//

jQuery(function() {

  const AJAX_FORM = '.ajax-form'
  const MODAL = '.modal'

  const COMMON_FORM_OPTS = {
    errorOverrides: [
      // Django errors
      [/с таким Электронная почта/, "с таким email"], // UNIQUE constraint violation

      // imask.js errors
      [/^Enter a valid phone number .*/, 'Введите верный номер телефона.'],
    ]
  }

  $(AJAX_FORM).each(function() {
    const form = this
    const $form = $(form)
    const modal = $form.parents(MODAL)[0]

    let opts = {
      successMsg: {
        title: $form.find('.success-title').html(),
        body:  $form.find('.success-body').html(),
      },
    }
    $.extend(true, opts, COMMON_FORM_OPTS)

    if (modal) {
      new ModalAjaxForm(form, opts)
    }
    else {
      new AjaxForm(form, opts)
    }
  })


  // --- Apply input masks ---

  // Phone inputs

  const $phoneInputs = $('[type="tel"]')

  $phoneInputs.each(function() {
    const maskOpts = {
      mask: '+{7} (000) 000 00 00',
      lazy: false,
      placeholderChar: '_',
    }
    $(this).on("focus", () => IMask(this, maskOpts) )
  })

})
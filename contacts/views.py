from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template import loader
from django.views import generic

from .forms import CallbackForm, FeedbackForm

__all__ = ['EmailFormData', 'RequestCallback', 'RequestFeedback']


class EmailFormData(generic.CreateView):
    """
    Base class for views sending form-based emails.

    Meant to be subclassed. The child classes are required to set
    `email_recipients`, `email_subject_template`, `email_template_html` and
    `email_template_plain` class attributes.

    The `form_valid()` method should be extended to set `email_context`
    attribute. Its value is passed to the email templates as the context.
    """
    http_method_names = ["post"]
    email_from = settings.EMAIL_HOST_USER
    email_recipients = []
    email_context = {}
    email_subject_template = ''
    email_template_html = ''
    email_template_plain = ''

    def form_invalid(self, form):
        return JsonResponse(
            {"ok": False, "errors": form.errors},
            status=400,
        )

    def form_valid(self, form):
        context = self.email_context

        email_subject = loader.get_template(
            self.email_subject_template
        ).render(context)

        email_plain = loader.get_template(
            self.email_template_plain
        ).render(context)

        email_html = loader.get_template(
            self.email_template_html
        ).render(context)

        delivered_msg_count = send_mail(
            from_email=self.email_from,
            recipient_list=self.email_recipients,
            subject=email_subject,
            message=email_plain,
            html_message=email_html,
        )
        if delivered_msg_count == 0:
            return JsonResponse(
                {"ok": False,
                 "errors": ["Email notification was not delivered"]},
                status=500,
            )
        return JsonResponse({"ok": True})


class RequestCallback(EmailFormData):
    """
    Email a call-back request.
    """
    form_class = CallbackForm
    email_recipients = settings.CALLBACK_REQUEST_RECIPIENTS
    email_subject_template = 'contacts/callback_alert_subject.txt'
    email_template_plain = 'contacts/callback_alert.txt'
    email_template_html = 'contacts/callback_alert.html'

    def form_valid(self, form):
        form.save()
        self.email_context = {
            'name': form.cleaned_data['name'],
            'phone': form.cleaned_data['phone'],
            'comment': form.cleaned_data['comment'],
            'site': self.request.site,
        }
        return super().form_valid(form)


class RequestFeedback(EmailFormData):
    """
    Email a feedback message.
    """
    form_class = FeedbackForm
    email_recipients = settings.FEEDBACK_REQUEST_RECIPIENTS
    email_subject_template = 'contacts/feedback_alert_subject.txt'
    email_template_plain = 'contacts/feedback_alert.txt'
    email_template_html = 'contacts/feedback_alert.html'

    def form_valid(self, form):
        form.save()
        msg_type = form.cleaned_data['msg_type']
        self.email_context = {
            'msg_type': form.instance.MsgTypes(msg_type).label,
            'msg': form.cleaned_data['msg'],
            'email': form.cleaned_data['email'],
            'name': form.cleaned_data['name'],
            'site': self.request.site,
        }
        return super().form_valid(form)
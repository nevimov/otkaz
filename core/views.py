from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name='main.html'


class PiiAgreementView(TemplateView):
    template_name='pii_agreement.html'


class AboutView(TemplateView):
    template_name='about.html'
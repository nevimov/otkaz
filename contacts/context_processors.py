from .forms import CallbackForm, FeedbackForm


def contacts(request):
    return {
        'contacts': {
            'callback_form': CallbackForm(),
            'feedback_form': FeedbackForm(),
        },
    }

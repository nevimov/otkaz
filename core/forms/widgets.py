from django.forms.widgets import CheckboxSelectMultiple, Select

from django_filters.widgets import RangeWidget

BS_WIDGETS = 'widgets/bootstrap'


class BootstrapSelect(Select):
    """
    This widget is the same as django.forms.widgets.Select except that it uses
    a custom HTML template appropriate for use with the Bootstrap framework.
    """
    template_name = f'{BS_WIDGETS}/select.html'
    option_template_name = f'{BS_WIDGETS}/select_option.html'


class BootstrapRange(RangeWidget):
    """
    This widget is the same as django_filters.widgets.RangeWidge except for
    the following differences:

    * BootstrapRange uses a custom HTML template appropriate for use with the
      Bootstrap framework.

    * RangeWidget is composed from to widgets -- one sets the START of the
      range, and the other -- the END. It doesn't allow to pass different
      `attrs` to each widget. BootstrapRange alleviates this problem.
    """
    template_name = f'{BS_WIDGETS}/multiwidget.html'

    def __init__(self, attrs=None, attrs_0=None, attrs_1=None):
        super().__init__(attrs=attrs)
        if attrs_0:
            self.widgets[0].attrs.update(attrs_0)
        if attrs_1:
            self.widgets[1].attrs.update(attrs_1)


class BootstrapMultipleCheckbox(CheckboxSelectMultiple):
    """
    This widget is the same as django.forms.widgets.CheckboxSelectMultiple
    except that it uses a custom HTML template appropriate for use with the
    Bootstrap framework.
    """
    template_name = f'{BS_WIDGETS}/checkbox_multi_select.html'
    option_template_name = f'{BS_WIDGETS}/checkbox_option.html'
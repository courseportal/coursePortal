import django.newforms as forms
from string import Template
from django.utils.safestring import mark_safe

# class Input(Widget):
#     """
#     Base class for all <input> widgets (except type='checkbox' and
#     type='radio', which are special).
#     """
#     input_type = None # Subclasses must define this.

#     def _format_value(self, value):
#         if self.is_localized:
#             return formats.localize_input(value)
#         return value

#     def render(self, name, value, attrs=None):
#         if value is None:
#             value = ''
#         final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
#         if value != '':
#             # Only add the 'value' attribute if a value is non-empty.
#             final_attrs['value'] = force_text(self._format_value(value))
#         return format_html('<input{0} />', flatatt(final_attrs))

# class TextInput(Input):
#     input_type = 'text'

#     def __init__(self, attrs=None):
#         if attrs is not None:
#             self.input_type = attrs.pop('type', self.input_type)
#         super(TextInput, self).__init__(attrs)

class ColourChooserWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    tpl = Template(u"""<h1>There would be a colour widget here, for value $colour</h1>""")
    return mark_safe(tpl.substitute(colour=value))
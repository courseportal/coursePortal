from django import template
from knoatom.forms import BugReportForm
from web.forms.submission import ReportForm
import re

register = template.Library()

@register.tag(name="removenewline")
def do_remove(parser, token):
	r"""Finds all '\n' characters and replaces them with spaces (' ')."""
	nodelist = parser.parse(('endremovenewline',))
	parser.delete_first_token()
	return RemoveNode(nodelist)
	
class RemoveNode(template.Node):
	def __init__(self, nodelist):
		self.nodelist = nodelist
	def render(self, context):
		output = self.nodelist.render(context)
		return output.replace('\n', ' ')

@register.tag(name="get_form")
def get_form(parser, token):
	r"""
	This is the compilation function for the bug_form custom templatetag.
	
	This tag returns the form for the bug report form.  The tag takes no arguments except for a optional 'as' argument.
	
	Example:
	
		.. code:: html
		
			{% bug_form %}
			{% bug_form as form %}
			
		The first example will save the form as ``bug_form``
	
	"""
	try:
		tag_name, arg, as_var = token.contents.split(None, 2)
	except ValueError:
		try:
			tag_name, arg = token.contents.split_contents()
			as_var = ''
		except ValueError:
			raise template.TemplateSyntaxError("{} requires one argument and an optional ' as var' statement.".format(token.split_content()[0]))
	m = re.search(r'(?<=as )\w+', as_var)
	if not m:
		var_name = 'form'
	else:
		var_name = m.group(0)
	return FormNode(var_name, arg)
	
class FormNode(template.Node):
	r"""
	This is the render function for the get_form tag.
	
	"""
	def __init__(self, var_name, arg):
		self.var_name = var_name
		self.arg = arg
	def render(self, context):
		if self.arg == 'BugReportForm':
			context[self.var_name] = BugReportForm()
		elif self.arg == 'ReportForm':
			context[self.var_name] = ReportForm()
		else:
			raise template.TemplateSyntaxError("get_form requires a valid form class name as an argument.")
		return ''
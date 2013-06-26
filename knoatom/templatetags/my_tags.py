from django import template
from knoatom.forms import bugReportForm
import re

register = template.Library()

@register.tag(name="bug_form")
def do_bug_form(parser, token):
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
		tag_name, arg = token.contents.split(None, 1)
	except ValueError:
		try:
			tag_name = token.contents.split_contents()
			arg = ''
		except ValueError:
			raise template.TemplateSyntaxError("{} requires no arguments or just an 'as' argument.".format(token.split_content()[0]))
	m = re.search(r'(?<=as )\w+', arg)
	if not m:
		var_name = 'bug_form'
	else:
		var_name = m.group(0)
	return BugFormNode(var_name)
	
class BugFormNode(template.Node):
	r"""
	This is the render function for the bug_form tag.
	
	"""
	def __init__(self, var_name):
		self.var_name = var_name
	def render(self, context):
		context[self.var_name] = bugReportForm()
		return ''
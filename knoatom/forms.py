from django import forms


class BugReportForm(forms.Form):
	email = forms.EmailField(max_length=100, required=True)
	subject = forms.CharField(max_length=100)
	content = forms.CharField(widget=forms.Textarea, required=True)
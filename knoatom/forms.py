from django import forms


class bugReportForm(forms.Form):
    subject = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea, required=True)
    email = forms.EmailField(max_length=100, required=True)
    cc_myself = forms.BooleanField(required=False)
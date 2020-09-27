from django import forms
from .PttSpider.ptt_spider import PttUrl

class TaskForm(forms.Form):
    url = forms.CharField(max_length=100)

    def clean_url(self):
        url = self.cleaned_data.get('url')

        if not PttUrl.verify_url(url):
            raise forms.ValidationError('Url is not valid')

        return url
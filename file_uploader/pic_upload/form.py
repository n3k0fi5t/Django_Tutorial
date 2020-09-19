from django import forms

import os

class ImageUploadForm(forms.Form):
    title = forms.CharField(label='Picture title', max_length=30, empty_value='type here...')
    image = forms.ImageField(required=True)

    def clean_image(self):
        img = self.cleaned_data.get('image')
        suffix = os.path.splitext(img.name)[-1].lower()

        if suffix not in ['.gif', '.jpg', '.jpeg', '.png', '.bmp']:
            raise forms.ValidationError('Unsupported file format')

        if img.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Picture is too large')

        return img
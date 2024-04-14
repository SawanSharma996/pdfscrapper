from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()
    def clean_zip_file(self):
        file = self.cleaned_data.get('zip_file')
        if file:
            # Check the file extension
            extension = file.name.split('.')[-1].lower()
            if extension != 'zip':
                raise forms.ValidationError('Only ZIP files are allowed.')
            # Optionally, you can also check the MIME type
            # if file.content_type != 'application/zip':
            #     raise forms.ValidationError('Only ZIP files are allowed.')
        return file
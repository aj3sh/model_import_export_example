from django import forms

# Import form
class ImportForm(forms.Form):
	file = forms.FileField()
	file.widget.attrs.update({'accept': '.xlsx'})

	def clean_file(self):
		data = self.cleaned_data['file']
		if not data.name.endswith('.xlsx'):
			raise forms.ValidationError("Invalid file.")
		return data
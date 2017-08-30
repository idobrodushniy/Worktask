import django.forms as forms 
from django.core import validators
from market.models import(
	get_all_name_goods
	)
try:
	class Select_Form(forms.Form):
		select = forms.ChoiceField(label = 'Product:',
			choices = get_all_name_goods(),
			)

	class Int_Form(forms.Form):
		enter = forms.IntegerField(label = 'Enter quantity:',
			min_value = 1
			)

	class Float_Form(forms.Form):
		enter = forms.FloatField(label = 'Enter kg:',
			min_value = 0.1
			)

except:
	pass
from django import forms

class SearchForm(forms.Form):
	list_of_choices = [("day", "Day"), ("week", "Week"), ("month", "Month")]
	search_term = forms.CharField(label="Search term", max_length=100)
	timeframe = forms.ChoiceField(choices=list_of_choices)
	# See also with list comprehension -- eg, choices=[(x,x) for x in range(1, 32)]
	
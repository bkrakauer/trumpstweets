import requests
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from .forms import SearchForm
from matplotlib import pylab as plt
# import PIL, PIL.Image, StringIO

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    # return render(request, 'index.html', {'var': 'Barak'})
	# r = requests.get('http://httpbin.org/status/418')
	# print r.text
	# return HttpResponse('<pre>' + r.text + '</pre>')
	
	# Do this on an ordinary GET request...
	return render(request, 'index.html')
	

def show_plot(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			word = form.cleaned_data['search_term']
			timeframe = form.cleaned_data['timeframe']
			word = word.lower()
			df = pd.read_csv('tweetdb.csv')
			df.text = df.text.str.lower()  # do this in the db in the future
			df_searchterm = df[df.text.str.contains(word)]
			avgrts = sum(df.retweet_count) / len(df)
			rts = sum(df_searchterm.retweet_count) / len(df_searchterm) if len(df_searchterm) > 0 else 0
			plot = get_plot(df, df_searchterm, timeframe)
			script, div = components(plot)
			context = {'script': script, 'div': div, 'word': word, 'rts': rts, 'avgrts': avgrts, 'timeframe': timeframe}
			return render(request, 'graph.html', context)
		else:
			return render(request, 'index.html')
	else:
		return render(request, 'index.html')

def get_plot(df, subdf, timeframe):
	# This is a bit of a hack, and we'll want to add labels....
	# x = range(-1, 8)
	# y = []
	
	x = range (1, max(df[timeframe]))
	y = [len(subdf[subdf[timeframe] == i]) for i in x]
	
	#fix headings, presumably by string interpolation.
	p = figure(title="Tweets by %s" %timeframe, x_axis_label=timeframe, y_axis_label="Number of Tweets")
	p.line(x, y, legend="Tweets", line_width=2)
	return p
	
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


import requests
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    # return render(request, 'index.html', {'var': 'Barak'})
	# r = requests.get('http://httpbin.org/status/418')
	# print r.text
	# return HttpResponse('<pre>' + r.text + '</pre>')

	word = 'hillary'
	
	plot = get_plot(word.lower())

	script, div = components(plot)
	return render(request, 'graph.html', {'script' : script, 'div' : div, 'word' : word})
	
def get_plot(word):
	df = pd.read_csv('tweetdb.csv')
	df.text = df.text.str.lower()  # do this in the db in the future
	df = df[df.text.str.contains(word)]
	x = range(-1, 8)
	y = []
	
	for i in x:
		y.append(len(df[df.month == i]))
	
	p = figure(title="Tweets by Month", x_axis_label="Month", y_axis_label="Number of Tweets")
	p.line(x, y, legend="Tweets", line_width=2)
	#show(p)
	return p
	
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


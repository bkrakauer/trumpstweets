import requests
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from .forms import SearchForm
from matplotlib import pylab as plt
import PIL, PIL.Image, StringIO

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    # return render(request, 'index.html', {'var': 'Barak'})
	# r = requests.get('http://httpbin.org/status/418')
	# print r.text
	# return HttpResponse('<pre>' + r.text + '</pre>')
	
	# Do this on an ordinary GET request...
	return render(request, 'index.html')
	#word = 'hillary'
	# Now, fix the below to handle this on a POST request...
	

def show_plot(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			word = form.cleaned_data['search_term']
			#   bokeh code below:
			plot = get_plot(word.lower())
			script, div = components(plot)
			return render(request, 'graph.html', {'script' : script, 'div' : div, 'word' : word})
			#   matplotlib code below:
			"""
			t = plt.arange(0.0, 2.0, .01)
			s = plt.sin(2 * plt.pi * t)
			plt.plot(t, s, linewidth=1.)
			plt.title('simple graph!')
			# store image in a buffer
			buffer = StringIO.StringIO()
			canvas = plt.get_current_fig_manager().canvas
			canvas.draw()
			pilImage = PIL.Image.fromstring("RGB", canvas.width_height(), canvas.tostring_rgb())
			pilImage.save(buffer, "PNG")
			plt.close()
			return HttpResponse(buffer.getalue(), mimetype="image/png") 
			"""
	else:
		return render(request, 'index.html')

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


from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Generate a PDF file venue list
def venue_pdf(request):
	#Create a Bytestream buffer
	buf = io.BytesIO()

	#Create Canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

	#create a text objects
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica",14)

	#Designate the model
	venues = Venue.objects.all()

	#Create blank list
	lines = []

	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.web)
		lines.append(venue.phone)
		lines.append(venue.email_address)
		lines.append(" ")

	#loop
	for line in lines:
		textob.textLine(line)

	


	#Finish up
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)
	return FileResponse(buf, as_attachment=True, filename='venue.pdf')	

# Generate CSV File Venue List
def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'

	#create a CSV writer
	writer = csv.writer(response)

	#add columns headings
	writer.writerow(['Venue Name', 'Address','Zip Code','Phone','Web Address','Email'])

	#Designate the model
	venues = Venue.objects.all()

	#Loop thru and output
	for venue in venues:
		writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web, venue.email_address])

	return response

# Generate Text File Venue List
def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venues.txt'

	#Designate the model
	venues = Venue.objects.all()

	#Create blank list
	lines = []

	#Loop thru and output
	for venue in venues:
		lines.append(f'{venue.name}\n {venue.address}\n {venue.zip_code}\n {venue.phone}\n {venue.web}\n {venue.email_address}\n\n\n')

	# Write to TextFile
	response.writelines(lines)
	return response

# Delete a Venue
def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venues')

# Delete an Event
def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	event.delete()
	return redirect('list-events')

#update an event
def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	form = EventForm(request.POST or None, instance=event )
	if form.is_valid():
		form.save()
		return redirect('list-events')
	return render(request,'events/update_event.html',
	       {
		       'venue': event,
		       'form':form
		   })

#Add an event
def add_event(request):
	submitted = False
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_event?submitted=True')
	else:
		form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_event.html', {'form': form, 'submitted':submitted})


def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue )
	if form.is_valid():
		form.save()
		return redirect('list-venues')
	return render(request,'events/update_venue.html',
	       {
		       'venue': venue,
		       'form':form
		   })

def search_venues(request):	
	if request.method == "POST":
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)
		return render(request,'events/search_venues.html',
		{'searched':searched,
   		'venues':venues})
	else:
		return render(request,'events/search_venues.html',{})


def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	return render(request,'events/show_venue.html',
	       {'venue': venue})

def list_venues(request):
	venue_list = Venue.objects.all().order_by('name')
	return render(request,'events/venue.html',
	       {'venue_list': venue_list})

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'events/add_venue.html', {'form': form, 'submitted':submitted})

def all_events(request):
	event_list = Event.objects.all().order_by('event_date')
	return render(request,'events/event_list.html',
	       {'event_list': event_list})

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):	
	name = " RENAN "
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

#create calendar
	cal = HTMLCalendar().formatmonth(
			year,
			month_number
		)
#current year
	now = datetime.now()
	curren_year = now.year

#current time

	time = now.strftime('%I:%M %p')

	return render(request, 
		'events/home.html', {
		"name": name,
		"year": year,
		"month": month,
		"month_number": month_number,
		"cal" : cal,
		"current_year": curren_year,
		"time": time,
		})

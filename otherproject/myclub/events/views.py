from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime




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

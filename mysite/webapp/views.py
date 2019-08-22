from django.shortcuts import render ,redirect,render_to_response
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView ,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegisterForm, Editform
from django.contrib import messages
from .models import Booking
from django.http import HttpResponseRedirect
import datetime 
from django.views.generic.edit import UpdateView
from django.template import RequestContext
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import smart_text
from django.template.loader import render_to_string
from django_pandas.io import read_frame
import pandas as pd
import sqlite3
#from django_pandas.managers import DataFrameManager
#from datetime import datetime

# Create your views here.
#booking form
def index(request):

	if request.method == 'POST':
	 	form = RegisterForm(request.POST)
	 	if form.is_valid():
	 		name =form.cleaned_data['name']
	 	#	booking_type=form.cleaned_data['booking_type']
	 		startdate=form.cleaned_data['startdate']
	 		enddate=form.cleaned_data['enddate']
	 		reason=form.cleaned_data['reason']
	 		status=form.cleaned_data['status']
	 		destination=form.cleaned_data['destination']
	 		pickup=form.cleaned_data['pickup']
	 		
	 		if Booking.objects.filter(startdate=startdate).exists():
	 			messages.error(request,('Time already booked'))

	 		elif Booking.objects.filter(startdate__lte=enddate,enddate__gte=startdate).exists():
	 				messages.error(request,('time overlaps'))

	 		elif  enddate < startdate :
	 			messages.error(request,('incorrect enddate'))

	 		
	 		else:
	 			data=Booking(name=name,startdate=startdate,enddate=enddate,reason=reason,status=status,destination=destination,pickup=pickup)
	 			data.save()
	 			#email
	 			

	 			send_mail("CAR BOOKING",
	 				str(data.name +' ' +'has made a car booking '+' '+ 'going for ' +' '+data.reason + ' ' + 'at'+' '+data.destination+' '+'on'+' '+data.startdate.strftime("%H:%M  %d %b %Y")),
	 				#RegisterForm(),
	 			 #render_to_string('webapp/index.html', {'form':form }),
	 				settings.EMAIL_HOST_USER,
	 				['mariam.nakanyike@gmail.com'] ,
	 				fail_silently =True,)
	 			#messages.success(request,('Car Booked Successfully'))
	 			return redirect('display')	
	else:
	 	form = RegisterForm()
	return render(request,'webapp/index.html', {'form': form})
#booking details
def display(request):
	all_items_ = Booking.objects.all()
	return render(request,'webapp/display.html',{'all_items_':all_items_})
#booked request
def bookings(request):
	all_items_ = Booking.objects.all()
	cb = Booking.objects.filter(status="Booking")
	return render(request,'webapp/booked.html',{'cb':cb})
#returned request
	
def returned(request):
	all_items_ = Booking.objects.all()
	cd=Booking.objects.filter(status="Returned")
	return render(request,'webapp/return.html',{'cd':cd})

#modifying a booking
def delete(request,booking_id):
	obj = Booking.objects.get(pk =booking_id)
	obj.delete()
	return redirect('display')

#taken
def taken(request):
	

	st=Booking.objects.filter(startdate__date=datetime.date.today(),status='Booked').update(status='taken')
	
	item=Booking.objects.filter(status='taken')
	#print(currentDate)
	#item.save()
	
	
	return render (request,'webapp/taken.html',{'item':item})
def edit(request,booking_id):
	if request.POST:
		editform = Editform(request.POST)
		if editform.is_valid():
			item = Booking.objects.get(pk=booking_id)
			editform = Editform(request.POST,instance=item)
			editform.save()
			#print(item.name)
			send_mail("CAR Returned",
	 				str(item.name +' ' +'has returned the  car from' +' '+item.pickup + ' ' +'at'+' '+item.enddate.strftime("%H:%M  %d %b %Y")),
	 				#RegisterForm(),
	 			 #render_to_string('webapp/index.html', {'form':form }),
	 				settings.EMAIL_HOST_USER,
	 				['mariam.nakanyike@gmail.com'] ,
	 				fail_silently =True,)


			return redirect ('display')
	else:
		item = Booking.objects.get(pk =booking_id)
		editform = Editform(instance=item)
		return render(request,'webapp/update.html',{'form':editform})

#booked cars today
def booked(request):
	item = Booking.objects.filter(startdate__date=datetime.date.today(),status='Booking').update(status='Booked')
	bk = Booking.objects.filter(status='Booked')
	return render(request,'webapp/today.html',{'bk':bk})
#reports
def report(request):
	db_query = Booking.objects.all()
	#df=read_frame(db_query,fieldnames=['name','startdate','enddate','reason','status','destination','pickup'])
	a=pd.DataFrame(list(Booking.objects.all().values()))
	a= pd.DataFrame(list(Booking.objects.filter(name='name').values()))
	a = pd.DataFrame(list(Booking.objects.all().values('name','startdate','enddate','reason','status','destination','pickup')))
	b=a['name'].value_counts()
	c=a['status'].value_counts()
	print(c)
	return redirect('report')
	'''
	try:
		a =df['name'].value_counts().filter (status="booked")
		#b=df['']
		print(a)
	except Exception as e:
		print("Does not exit")
	
	return redirect('report')
	#ignore
	df = pd.DataFrame(list(BlogPost.objects.all().values()))
df = pd.DataFrame(list(BlogPost.objects.filter(date__gte=datetime.datetime(2012, 5, 1)).values()))

# limit which fields
df = pd.DataFrame(list(BlogPost.objects.all().values('author', 'date', 'slug')))
	'''
	'''special code
	def report(request):
	db_query = Booking.objects.all()
	df=read_frame(db_query,fieldnames=['name','startdate','enddate','reason','status','destination','pickup'])
	print (df)
	return render(request,'webapp/report.html',{'df':df})
	try:
		a =df['name'].value_counts().filter (status="booked")
		#b=df['']
		print(a)
	except Exception as e:
		print("Does not exit")
	
	return redirect('report')
	'''
		
	#df=read_frame(db_query,fieldnames=['name','startdate','enddate','reason','status','destination','pickup'])
	#print (df)

	#df = read_frame(Booking.objects.all())
	#return HttpResponse(db_query.to_html())


#time factor
'''
def nobooking(request):
	item = Booking.objects.filter(date__range=[startdate__date=startdate,enddate__date=enddate]).exists()
	messages.error(request,('Date already booked'))

	def index2(request):
    df = read_frame(Product.objects.all())
    return HttpResponse(df.to_html())
'''

'''
	 			if Booking.objects.filter(startdate__lte=enddate):
	 				messages.error(request,('Car will be in use'))
	 				'''
'''
	 			if Booking.objects.filter(startdate__lte=enddate,enddate__gte=startdate).exists():
	 				messages.error(request,('time overlaps'))
	 				#raise ValidationError  
	 				# or whatever
	 			#return redirect('index')
	 		

	 		EMAIL_BACKEND = ‘django.core.mail.backends.smtp.EmailBackend’
EMAIL_HOST = ‘smtp.gmail.com’
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ‘your_account@gmail.com’
EMAIL_HOST_PASSWORD = ‘your account’s password’

def returnemail(request):
	cd=Booking.objects.all.filter(status="Returned").exists()
	send_mail("CAR Returned",
	 				str(cd.name +' ' +'has made a car booking '+' '+ 'going for ' +' '+cd.reason + ' ' + 'at'+' '+cd.destination+' '+'on'+' '+cd.startdate.strftime("%H:%M  %d %b %Y")),
	 				#RegisterForm(),
	 			 #render_to_string('webapp/index.html', {'form':form }),
	 				settings.EMAIL_HOST_USER,
	 				['mariam.nakanyike@gmail.com'] ,
	 				fail_silently =True,)
from django.core.mail import send_mail
from django.conf import settings


def email(request):    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['receiver@gmail.com',]   
     send_mail( subject, message, email_from, recipient_list )    
     return redirect('redirect to a new page')

	 		elif Booking.objects.filter(startdate__range=(startdate, enddate)).exists():
	 				messages.error(request,('Car will be in use from that time'))
	 				
	 		
	 		elif Booking.objects.filter(startdate__lte=enddate,enddate__gte=startdate).exists():
	 				messages.error(request,('time overlaps'))


	 		elif Booking.objects.filter(startdate__lte=enddate).exists():
	 				messages.error(request,('time overlaps'))
			
	 				'''
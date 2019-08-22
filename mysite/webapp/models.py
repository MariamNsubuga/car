from django.db import models
from django.forms import ModelForm
# Create your models here.
class Booking(models.Model):
	'''
	BOOKING_TYPE_LIST =[
			('Onstation','Onstation'),
			('Outstation','Outstation'),
Status_CHOICES
	]
	'''
	Status_CHOICES=[
	('Booking','Booking'),
	('Returned','Returned'),
	]
	name = models.CharField('name', max_length=120)
	#booking_type=models.CharField('booking_type',max_length=120,choices=BOOKING_TYPE_LIST,default="null")
	
	#booking_type=models.CharField('booking_type',max_length=120)
	startdate = models.DateTimeField('startdate')   
	enddate=models.DateTimeField('enddate')
	reason=models.CharField('reason',max_length=120)
	status=models.CharField('status',max_length=120,choices=Status_CHOICES)
	destination=models.CharField('destination',max_length=120)
	pickup=models.CharField('pickup',max_length=120)
	

def __str__(self):
	return self
'''	
class BookingType(models.Model):
	booking_type=models.CharField(max_length=120)

	def  __str__(self):
		return self.booking_type
	'''
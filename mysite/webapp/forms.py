from django import forms
from django.forms import ModelForm
from .models import *
from datetime import datetime
from bootstrap_datepicker_plus import  DateTimePickerInput

class RegisterForm(forms.Form):
	Status_CHOICES=[
	('Booking','Booking'),
	('Returned','Returned'),
	]
	model = Booking
	fields = ['name','startdate','enddate','reason','status','destination','pickup']
	widgets = {'startdate':DateTimePickerInput(),'enddate':DateTimePickerInput(),}
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	startdate=forms.DateTimeField(widget=DateTimePickerInput())
	enddate=forms.DateTimeField(widget=DateTimePickerInput())
	reason = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	#status = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True,forms.Select(choices=Status_CHOICES))
	status = forms.CharField(widget=forms.Select(choices=Status_CHOICES), required=True)
	destination = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	pickup = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

class Editform(ModelForm):
	class Meta:
		model = Booking
		fields=['id','name','startdate','enddate','reason','status','destination','pickup']

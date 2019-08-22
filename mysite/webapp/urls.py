from django.conf.urls import url
from . import views
from django.urls import path


urlpatterns = [
path('',views.index,name='index'),
path('display/',views.display,name='display'),
path('booked/',views.bookings,name='bookings'),
path('return/',views.returned,name='booking'),
path('delete/<booking_id>',views.delete,name='delete'),
path('taken/',views.taken,name='taken'),
path('edit/<booking_id>',views.edit,name='edit'),
path('today/',views.booked,name='today'),
path('report/',views.report,name='report'),

#path('edit')


#path('booking/',views.bookings,name='bookings'),
]

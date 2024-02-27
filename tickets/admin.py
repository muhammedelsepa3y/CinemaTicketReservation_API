from django.contrib import admin

# Register your models here.

from .models import Guest
admin.site.register(Guest)
from .models import Movie
admin.site.register(Movie)
from .models import Reservation
admin.site.register(Reservation)

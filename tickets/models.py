from django.db import models

# from tickets.util.object import PersonType


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie= models.CharField(max_length=10)
    date = models.DateField()
    def __str__(self):
        return self.movie
    
class Guest(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name='reservations')
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE,related_name='reservations')
    seat = models.CharField(max_length=10)
    def __str__(self):
        return self.seat
    










     # number=models.IntegerField(
    #     choices=PersonType.choices,
    # )
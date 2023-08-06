from django.db import models

# Create your models here.
# Rooms                  4.000000
# House_Type             0.000000
# Number_of_bedrooms     4.000000
# Bathrooms              2.000000
# Number_of_Car_spots    4.000000
# Landsize               0.041538
# BuildingArea           0.223823
House_Type = [
    ('h', 'house,cottage,villa, semi,terrace'),
    ('u', 'duplex'),
    ('t', 'townhouse'),
]
class Deployed_data(models.Model):
    rooms=models.IntegerField(default=0)
    House_Type =models.CharField(max_length=100,choices=House_Type,default="select housetype")
    number_of_bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    number_of_car_spots = models.IntegerField(default=0)
    landsize = models.FloatField(default=0.0)
    building_area=models.FloatField(default=0.0)

class Pickle(models.Model):
    pickle_file=models.FileField(upload_to="naga/")

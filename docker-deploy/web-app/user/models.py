
from datetime import datetime, timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models

TypeOfVehicle = {
        ('SUV','SUV'),
        ('Sedan','Sedan'),
        ('Sports Car','Sports Car'),
    }
# Create your models here.
class User(models.Model):
    gender = {
        ('male','male'),
        ('female','female'),
        ('unknown','unknown'),
    }
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=64,choices=gender, default="unknown")
    is_driver = models.BooleanField(default=False,null=True,blank=True)
    full_name = models.CharField(max_length=32,null=True,blank=True)
    vehicle_type = models.CharField(max_length=64,choices=TypeOfVehicle,default="Sedan")
    plate_num = models.CharField(max_length=16,null=True,blank=True)
    max_passenger = models.IntegerField(validators=[
            MinValueValidator(1),MaxValueValidator(10)
        ],null=True,blank=True)
    special_vehicle_info = models.CharField(max_length=128,null=True,blank=True,default="None")
    def __str__(self):
        return self.username
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    destination = models.CharField(max_length=128)
    arrival_time = models.DateTimeField()
    passenger_number = models.IntegerField(validators=[
        MinValueValidator(1),MaxValueValidator(10)
    ])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', blank=True, null=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver', blank=True,null=True)
    is_shared = models.BooleanField(default=False)
    sharer = models.ManyToManyField(User, related_name="sharer", blank=True)
    is_comfirmed=models.BooleanField(default=False)
    special_request = models.CharField(max_length=128, blank=True, default='None')
    special_vehicle_type = models.CharField(max_length=128, blank=True, default='')
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


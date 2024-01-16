from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model

class SystemUsers(AbstractUser):
    role = (
        ('DOCTOR', 'DOCTOR'),
        ('PATIENT', 'PATIENT')
    )
    sex = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    )
    
    user_role = models.CharField(max_length=100, choices=role, null=True)
    age = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    gender = models.CharField(max_length=100, choices=sex)
    approved = models.BooleanField(null=True, default=False)

class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

#class TemporaryAppointment(models.Model):
    #date = models.DateTimeField(null= True)
    #datee = models.DateField(null= True)
    #time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null= True)
    #doctor = models.CharField(null= True,max_length=100)
    #patient = models.CharField(null=True ,max_length=100)
    #approved = models.BooleanField(default=False)  # New field for approval status

    #def __str__(self):
        #return f"{self.patient}'s Temporary Appointment on {self.date} at {self.time}"
    


#class Appointment(models.Model):
    #date = models.DateTimeField(auto_now_add=True)
    #time = models.TimeField(null=True)
    #doctor = models.CharField( null= True, max_length=100)
    #patient = models.CharField(null=True ,max_length=100)
    #approved = models.BooleanField(default=False)
    # Add other fields as needed

class Appointmentt(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(null=True)
    doctor = models.CharField( null= True, max_length=100)
    patient = models.CharField(null=True ,max_length=100)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.patient}'s Appointment on {self.date} at {self.time} ({'Approved' if self.approved else 'Pending'})"
    
class NewTimeSlot(models.Model):
    id = models.AutoField(primary_key=True, default='1')
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

class NewTemporaryAppointment(models.Model):
    date = models.DateTimeField(null= True)
    datee = models.DateTimeField(auto_now_add=True, editable=False,null=True)
    time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null= True)
    doctor = models.CharField(null= True,max_length=100)
    patient = models.CharField(null=True ,max_length=100)
    approved = models.BooleanField(default=False)  # New field for approval status

    def __str__(self):
        return f"{self.user.username}'s Temporary Appointment on {self.date} at {self.time}"
    
class NewAppointmentt(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(null=True)
    doctor = models.CharField( null= True, max_length=100)
    patient = models.CharField(null=True ,max_length=100)
    approved = models.BooleanField(default=False)
    hii = models.CharField(max_length=100, null = True)
    


class Ex(models.Model):
    name = models.CharField(max_length=100)


class TimeSlotSecond(models.Model):
    time = models.TimeField()

    def __str__(self):
        return str(self.time)

class TemporarySecond(models.Model):
    datee = models.DateField(null= True)
    time = models.TimeField( null= True)
    doctor = models.CharField(null= True,max_length=100)
    patient = models.CharField(null=True ,max_length=100)
    approved = models.BooleanField(default=False)  # New field for approval status

    def __str__(self):
        return f"{self.patient}'s Temporary Appointment on {self.datee} at {self.time}"
    
class AppointmentSecond(models.Model):
    
    date = models.DateField(null= True)
    time = models.TimeField(null=True)
    doctor = models.CharField( null= True, max_length=100)
    patient = models.CharField(null=True ,max_length=100)
    approved = models.BooleanField(default=False)
    hii = models.CharField(max_length=100, null = True)
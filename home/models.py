from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.IntegerField()

    PATIENT = 1
    DOCTOR = 2
    MANAGEMENT =3
    
    ROLE_CHOICES = (
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (MANAGEMENT, 'Management'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    def __str__(self):
        return f"{self.user}'s Profile"
    
class Doctor(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    Ortho = 'ORTHOPEDIC'
    IntMed = 'INTERNAL MEDICINE'
    Derm = 'DERMATOLOGY'
    Pedia = 'PEDIATRICS'
    Gen = 'GENREAL SURGERY'

    specializations = (
        (Ortho,"Orthopedic"),
        (IntMed,"Internal Medicine"),
        (Derm,"Dermatology"),
        (Pedia,"Pediatrics"),
        (Gen,"General Surgery"),
    )
    specialist = models.CharField(choices=specializations,max_length=20)
    experience = models.PositiveIntegerField()

class Patient(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=255)
    mobile_no = models.IntegerField()
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"
    

class Record(models.Model):
    name = models.ForeignKey(Patient,on_delete=models.CASCADE)
    record_pdf = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"{self.name} file"
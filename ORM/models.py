from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Custom Field in User
class User(AbstractUser):
    phone = models.CharField(max_length=12)


class ResetUuid(models.Model):
    UUID = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry = models.DateTimeField()
    expiry_flag = models.BooleanField(default=False)


# Patient Side
class PatientRegister(models.Model):
    GENDER_CHOICES = [("MALE", "MALE"), ("FEMALE", "FEMALE")]

    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=50, unique=True)
    phone_no = models.CharField(max_length=12)
    disease = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DoctorRegister(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    specialist = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    phone_no = models.CharField(max_length=12)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} {self.specialist}"


class DoctorList(models.Model):
    doctor = models.ForeignKey(DoctorRegister, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.doctor)


class DateBooking(models.Model):
    doctor_assigned = models.ForeignKey(
        DoctorList, on_delete=models.SET_NULL, null=True
    )
    date_book = models.DateField()

    def __str__(self):
        return f"{self.date_book} with {self.doctor_assigned}"


class SlotBooking(models.Model):
    date_assigned = models.ForeignKey(DateBooking, on_delete=models.SET_NULL, null=True)
    slot = models.TimeField()

    def __str__(self):
        return f"{self.slot} on {self.date_assigned}"


# For Doctor Side
class Appointees(models.Model):
    patient = models.ForeignKey(PatientRegister, on_delete=models.SET_NULL, null=True)


class ContactUser(models.Model):
    appointee = models.ForeignKey(Appointees, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.appointee


class Medication(models.Model):
    MEDICINE_CHOICES = [
        ("Med 1", "Medicine 1"),
        ("Med 2", "Medicine 2"),
        ("Med 3", "Medicine 3"),
        ("Med 4", "Medicine 4"),
        ("Med 5", "Medicine 5"),
        ("Med 6", "Medicine 6"),
    ]

    DOSE_CHOICES = [
        (1, "1 dose"),
        (2, "2 doses"),
        (3, "3 doses"),
    ]

    DAYS_CHOICES = [
        ("1 Day", "1 Day"),
        ("2 Days", "2 Days"),
        ("3 Days", "3 Days"),
        ("4 Days", "4 Days"),
        ("5 Days", "5 Days"),
        ("6 Days", "6 Days"),
        ("7 Days", "7 Days"),
    ]

    prescription = models.CharField(max_length=50, choices=MEDICINE_CHOICES)
    prescription_dose = models.IntegerField(choices=DOSE_CHOICES)
    prescription_days = models.CharField(max_length=50, choices=DAYS_CHOICES)

    def __str__(self):
        return f"{self.prescription} - {self.prescription_dose} doses for {self.prescription_days}"


class SuggestedMedicine(models.Model):
    prescribed = models.ForeignKey(Medication, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(PatientRegister, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorRegister, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient} prescribed {self.prescribed} by {self.doctor}"

from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.CharField(max_length=10, unique=True)
    
   
        
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()
    Gender_choices = [
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    ]
    
    gender = models.CharField(max_length=20,choices=Gender_choices)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_visit = models.DateField()
  
    symptoms = models.TextField()
    doctor_assigned = models.CharField(max_length=100)
    def __str__(self):
      return self.patient_name 
  
    def save(self,*args,**kwargs):
        if not self.patient_id:
              
        
            last_patient=Patient.objects.order_by('-id').first()
        
            if last_patient:
                number = int (last_patient.patient_id[1:])
                new_number=number +1
                
            else:
                new_number = 1

            self.patient_id = f'P{new_number:03d}'

        super().save(*args, **kwargs) 
class Doctor(models.Model):
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    doctor_id = models.CharField(max_length=10, unique=True)
    doctor_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    profile_image = models.ImageField(upload_to='doctors/', blank=True, null=True)

    def __str__(self):
        return self.doctor_name
    
              
            
            

            
    
       
class patient_booking(models.Model):
    TIME_SLOTS = [     ('', 'Select Time Slot'),
        ('10:00', '10:00 AM'),
        ('11:00 AM', '11:00 AM'),
        ('12:00 PM', '12:00 PM'),
        ('01:00 PM', '01:00 PM'),
        ('02:00 PM', '02:00 PM'),
        ('03:00 PM', '03:00 PM'),
    ]

    patient_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    appointment_date = models.DateField()
    reason_for_visit = models.TextField()
    doctor = models.ForeignKey(
    Doctor,
    on_delete=models.CASCADE
)
    
    def __str__(self):
      return self.patient_name 
  




class DoctorSchedule(models.Model):

    DAYS = [
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    day = models.CharField(
        max_length=20,
        choices=DAYS
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.doctor_name} - {self.day}"    
    
    
class UserRegistration(models.Model):
    
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Receptionist', 'Receptionist'),
        ('Doctor', 'Doctor'),
    ]

    full_name = models.CharField(max_length=100)

    username = models.CharField(max_length=50, unique=True)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=128)

    confirm_password = models.CharField(max_length=128)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Receptionist'
    )

    def __str__(self):
        return self.full_name    
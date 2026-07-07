from django import forms
from .models import Patient
from .models import patient_booking
from .models import Doctor

class PatientForm(forms.ModelForm):
    class Meta():
        model=Patient
        fields='__all__'
        
        
        widgets = {
            'date_of_visit': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'gender': forms.RadioSelect(),
        }
        
    def clean_patient_name(self):
       patient_name = self.cleaned_data['patient_name']
    
       if len(patient_name.strip()) < 3 :
        raise forms.ValidationError("Name must contain at least 3 characters.")
    
       return patient_name
   
    def clean_age(self):
        age = self.cleaned_data['age']
        
        if age < 0 :
            raise forms.ValidationError("age must not be negative")
        
        return age
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone Number should contain only digits")
            
        
        if len(phone_number) < 10 :
            raise forms.ValidationError("Phone no. must be 10 digits")
        
        return phone_number
   
         
        
class bookingForm(forms.ModelForm):
    class Meta():
        model=patient_booking
        fields='__all__'
        
        
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'})
        }
        
        
class Add_doctor(forms.ModelForm):
    class Meta():
        model=Doctor
        fields='__all__'
        

            
       
        
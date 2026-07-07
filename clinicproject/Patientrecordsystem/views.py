from django.shortcuts import render
from .forms import PatientForm
from django.shortcuts import redirect
from .models import Patient,UserRegistration
from django .db.models import Q
from .forms import bookingForm
from .models import patient_booking
from datetime import date
from django.contrib import messages
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from .forms import Add_doctor
from .models import Doctor
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def get_base_template(request):
    
    role = request.session.get("role")

    if role == "Admin":
        return "base.html"

    elif role == "Receptionist":
        return "base_reception.html"

    elif role == "Doctor":
        return "base_doctor.html"

    return "base.html"
def home_fun(request):
    
    base_template = get_base_template(request)
        
    
    
    total_patients = Patient.objects.count()
    return render(request,'home.html',{'total_patients': total_patients,"base_template": base_template})

def add_doctor_fun(request):
    
    base_template = get_base_template(request)
    if request.method=='POST':
        form= Add_doctor(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_doctor')
            
    else:
        form = Add_doctor()   
        
    return render(
        request,
        'add_doctor.html',
        {'form': form,"base_template": base_template}
    )     
    

    
def add_patient_fun(request):
    base_template = get_base_template(request)
    
    
    
    if request.method == 'POST':
        print("POST REQUEST")
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,"Patient added successfully.")
            return redirect('add_patient')
        else: 
            
           print(form.errors)

    else:
        form = PatientForm()

    return render(
        request,
        'add_patient.html',
        {'f': form,"base_template": base_template}
    ) 
 
def generate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_records.csv"'

    writer = csv.writer(response)
    writer.writerow(['Patient_name', 'Age', 'Gender','address','date_of_visit','symptoms','dr assigned'])

    patients = Patient.objects.all()
    for patient in patients:
        writer.writerow([patient.patient_name,patient.age,patient.gender,patient.address,patient.date_of_visit,patient.symptoms,patient.doctor_assigned])

    return response   
        
   


def about_fun(request):
    base_template = get_base_template(request)
    return render(request, 'about.html',{"base_template": base_template})
def contact_fun(request):
    base_template = get_base_template(request)
    return render(request, 'contact.html',{"base_template": base_template})

    
def book_appointment_fun(request):
    base_template = get_base_template(request)
    return render(
        request,
        'book_appointment.html',{"base_template": base_template}
    )
 

def patient_books_fun(request):
    base_template = get_base_template(request)
    
    
    #ap = Patient.objects.filter(
    #date_of_visit=date.today())
    st = patient_booking.objects.filter(
    appointment_date=date.today()
)

    total_patients_t = patient_booking.objects.count()
    
    
    

    return render(request,'patient_books.html',{
        'patient': st,
        'total_patients_t': total_patients_t,"base_template": base_template})
    
       
    
def appointment_fun(request):
    base_template = get_base_template(request)
    
    doctors = Doctor.objects.all()
    if request.method=='POST':
        
       form = bookingForm(request.POST)
       if form.is_valid():
           form.save()
           
           
           messages.success(request,"Appointment booked successfully.")
           return redirect('/appointment_form/')
           
           
    else:
        form=bookingForm()       
    return render(
        request,
        'appointment_form.html',
        {'f': form,"doctors": doctors,"base_template": base_template}
    )    
  

def manage_patient_fun(request):
    base_template = get_base_template(request)
  
    
    
    search = request.GET.get('search')
    if search:
        patients = Patient.objects.filter (
            Q(patient_name__icontains=search) |
            Q(patient_id__icontains=search)).order_by('-id')
    
    else:    
        patients = Patient.objects.all().order_by('-id')

    #patients = Patient.objects.all()
    #patients = Patient.objects.all().order_by('-id')

    paginator = Paginator(patients, 10)  # Har page par 10 patients

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    

    total_patients = Patient.objects.count()

    return render(
        request,
        'manage_patient.html',
        {
             'page_obj': page_obj,
            'total_patients': total_patients,
            'patients': patients,"base_template": base_template
        }
    )


def update_patient_fun(request, id):
    base_template = get_base_template(request)

    patient = Patient.objects.get(id=id)

    if request.method == 'POST':

        form = PatientForm(
            request.POST,
            instance=patient
        )

        if form.is_valid():
            form.save()
            return redirect('/manage_patient/')

    else:

        form = PatientForm(
            instance=patient
        )

        return render(
        request,
        'update_patient.html',
        {'f': form,"base_template": base_template}
    )
def delete_patient_fun(request, pk):
    base_template = get_base_template(request)
        
    patient = Patient.objects.get(pk=pk)

    if request.method == 'POST':
        
        
          
        patient.delete()
        return redirect('/manage_patient/')
            
            
    return render(request,'delete_patient.html',{'patient': patient,"base_template": base_template})




def register_fun(request):
    base_template = get_base_template(request)
    if request.method=="POST":
        nm = request.POST["full_name"]
        usernm = request.POST["username"]
        em = request.POST["email"]
        password = request.POST["password"]
        c_pass = request.POST["confirm_password"]
     
        role= request.POST["role"]
        password = make_password(password)
        UserRegistration.objects.create(full_name = nm ,username = usernm,
                        email = em, password = password ,
                        confirm_password = c_pass, role = role )
        send_mail(subject='Welcome My Man',
         message=(
        f'Hello {nm},\n\n'
        'Your account has been created successfully.\n'
        f'Username: {usernm}\n'
        f'Role: {role}\n\n'
        'Thank you.'
    ),
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[em],
    fail_silently=False,
)       
        return redirect('/login/')
        
    return render(request,'register.html',{"base_template": base_template})
        
    
def login_fun(request):
    base_template = get_base_template(request)
    if request.method == "POST":
        usn = request.POST['username']
        pas = request.POST['password']
        #try:
        user = UserRegistration.objects.get(username=usn)
        if check_password (pas , user.password):
           request.session["user_id"] = user.id
           request.session["username"] = user.username
           request.session["role"] = user.role
           request.session["email"] = user.email
           

           if user.role == "Admin":
                return redirect("admin")

           elif user.role == "Doctor":
                return redirect("doctor")

           else:
                return redirect('/reception/')

        else:

            return render(request,"login.html",
                          {"msg":"Invalid Username or Password"})

    
            
            
        #except:
            #pass
    return render(
        request,
        'login.html',{"base_template": base_template})
    
def admin_fun(request):
    base_template = get_base_template(request)
    
    if "user_id" not in request.session:
        
       
        return redirect("login")
    username = request.session["username"]
    return render(request, "home.html",{"username":username,"base_template": base_template})    


def doctor_fun(request):
    base_template = get_base_template(request)
    
    email = request.session.get("email")

    doctor = Doctor.objects.get(email=email)

    today = date.today()

    appointments = patient_booking.objects.filter(
        doctor=doctor,
        appointment_date=today
    )

    context = {
        "doctor": doctor,
        "appointments": appointments,
        "total": appointments.count(),
        "base_template": base_template
    }

    return render(request, "doctor.html", context)



def reception_fun(request):
    base_template = get_base_template(request)

    total_patients = Patient.objects.count()

    total_doctors = Doctor.objects.count()

    appointments = patient_booking.objects.filter(
        appointment_date=date.today()
    )

    context = {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "today_appointments": appointments.count(),
        "appointments": appointments,
        "base_template": base_template
    }

    return render(request, "reception.html", context)



def logout_fun(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("login")
    
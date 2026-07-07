from django.urls import path 
from .import views
urlpatterns = [
    path('',views.login_fun),
    path('home/',views.home_fun),
    path('add_patient/',views.add_patient_fun, name= 'add_patient'),
    
    path('about/',views.about_fun),
    path('contact/',views.contact_fun),
    path('add_doctor/',views.add_doctor_fun,name = 'add_doctor'),
    path('register/', views.register_fun),
    path('login/', views.login_fun,name ='login'),
    
path(
    'book_appointment/',
    views.book_appointment_fun,name='book_appointments'
),
path('generate_csv/', views.generate_csv, name='generate_csv'),
path(
    'appointment_form/',
    views.appointment_fun,name='book_appointment'
),

    path(
    'manage_patient/',
    views.manage_patient_fun,
    name='manage_patient'
),

   path(
    'update_patient/<int:id>/',
    views.update_patient_fun,
    name='update_patient'
),
   path('delete_patient/<int:pk>/',
    views.delete_patient_fun),
   
   
   path('patient_books/',views.patient_books_fun),
   path("admin_dashboard/", views.admin_fun, name="admin"),
   
    path("doctor/", views.doctor_fun, name="doctor"),

    path("reception/", views.reception_fun, name="reception"),
    path("logout/",views.logout_fun,name="logout"),
   
]

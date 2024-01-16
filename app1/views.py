
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from . forms import SystemUserCreationForm,TemporaryAppointmentForm,SystemUserUpdateForm,TimeSlotSecondForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import *
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.mail import send_mail 

# Create your views here.
def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def  aboutpage(request):
    return render(request, 'about.html')

def profile (request):
    return render(request, 'profile.html')

def userregistration(request):
    if request.method == 'POST':
        form = SystemUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.approved = False  # New users are not approved by default
            user.save()
            messages.success(request, 'User has been registered.')
            return redirect(home)
        
    else:
        form = SystemUserCreationForm()

    return render(request, 'reg.html', {'form':form})

def userlogin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, password=password, username=username)
        if user:
            login(request,user)
            messages.success(request, "user has loged in successfully")
            return redirect(home)
        else:
            messages.success(request, "no such user exist")
            return redirect(userlogin)
    return render(request, 'login.html')

def user_approval_view(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect to home if not a superuser

    users_to_approve = SystemUsers.objects.filter(approved=False)
    print(users_to_approve)

    if request.method == 'POST':
        # Handle form submission to approve or reject users
        selected_users = request.POST.getlist('selected_users')
        approve_action = 'approve' in request.POST
        reject_action = 'reject' in request.POST

        if approve_action:
            SystemUsers.objects.filter(username__in=selected_users).update(approved=True)
        elif reject_action:
            # Delete selected users (or handle rejection as needed)
            SystemUsers.objects.filter(username__in=selected_users).delete()

        return redirect('user_approval')  # Redirect to the correct URL pattern name

    return render(request, 'user_approval.html', {'users_to_approve': users_to_approve})
def alldetails(request):
    s = SystemUsers.objects.all()
    return render(request, 'header.html', {'s':s})

def onedetails(request, username):
    print("hii")
    print(username)
    a = SystemUsers.objects.get(username=username)
    print(a)
    return render(request, 'header.html', {'a':a})


def logoutpage(request):
      logout(request)
      messages.success(request, "user hass been logout")
      return redirect(home)

def doctorlist(request):
    dlist = SystemUsers.objects.filter(user_role = 'DOCTOR')
    return render(request, 'doctors_list.html' , {'dlist':dlist})




def book_appointment(request, username):
    print('hi')
    doctor = SystemUsers.objects.get(username=username)
    print(doctor)
    
    if request.method == 'POST':
        form = TemporaryAppointmentForm(request.POST)
        
        if form.is_valid():
            print('inside')
            temporary_appointment = form.save(commit=False)
            temporary_appointment.doctor = doctor
            temporary_appointment.patient = request.user
            temporary_appointment.save()
            
            # Add any additional logic or redirects you need
            return redirect(home)  # Replace 'hoii' with the actual URL or view name
        
    else:
        form = TemporaryAppointmentForm()  # Fix: Use TemporaryAppointmentForm instead of AppointmentForm

    return render(request, 'appointment.html', {'form': form, 'doctor': doctor})

@login_required
def appointment_pending(request):
    if request.user.user_role == 'DOCTOR':  # Check if the user is a doctor
        appointments = TemporarySecond.objects.filter(approved=False)
        return render(request, 'appointment_pending.html', {'appointments': appointments})
    else:
        # Redirect or handle the case where the user is not a doctor
        return redirect('home')  # Adjust 'home' to the actual URL name for the home page
    

@login_required
def approve_appointment(request, id):
    if request.user.user_role == 'DOCTOR' :  # Check if the user is a doctor
        temporary_appointment = get_object_or_404(TemporarySecond, id=id)
        temporay_patient = temporary_appointment.patient
        patient_details = SystemUsers.objects.get(username=temporay_patient)
        patient_mail = patient_details.email
       
        if not temporary_appointment.approved:
            subject = " Doctor Appointment Confirmation "
            message = f"{temporay_patient} your appointment has approved on {temporary_appointment.datee} at {temporary_appointment.time} with Dr.{temporary_appointment.doctor}"
            from_email = settings.EMAIL_HOST_USER
            to_mail = [patient_mail]
            appointment = AppointmentSecond(
                
                date=temporary_appointment.datee,
                time=temporary_appointment.time,
                doctor=temporary_appointment.doctor,
                patient=temporary_appointment.patient,
                approved=True
            )
            appointment.save()
            messages.success(request, "you request to appointment")
            send_mail(subject, message, from_email, to_mail)
            temporary_appointment.delete()

        return redirect(appointment_pending)
    else:
        # Redirect or handle the case where the user is not a doctor
        return redirect(home)  # Adjust 'home' to the actual URL name for the home page
    

def reject_appointment(request, id):
    if request.user.user_role == 'DOCTOR' :  # Check if the user is a doctor
        temporary_appointment = get_object_or_404(TemporarySecond, id=id)
        temporay_patient = temporary_appointment.patient
        patient_details = SystemUsers.objects.get(username=temporay_patient)
        patient_mail = patient_details.email
       
        if not temporary_appointment.approved:
            subject = " Doctor Appointment Confirmation "
            message = f"{temporay_patient} your appointment has reject on {temporary_appointment.datee} at {temporary_appointment.time} with Dr.{temporary_appointment.doctor}. Try again with new time and date"
            from_email = settings.EMAIL_HOST_USER
            to_mail = [patient_mail]
            
            messages.success(request, "you request to appointment")
            send_mail(subject, message, from_email, to_mail)
            temporary_appointment.delete()

        return redirect(appointment_pending)
    else:
        # Redirect or handle the case where the user is not a doctor
        return redirect(home)  # Adjust 'home' to the actual URL name for the home page



def user_list(request):
    doctors = SystemUsers.objects.filter(user_role='DOCTOR')
    patients = SystemUsers.objects.filter(user_role='PATIENT') 
    return render(request, 'user_list.html', {'doctors': doctors, 'patients': patients})

def update_user(request, username):
    user = get_object_or_404(SystemUsers, username=username)
    if request.method == 'POST':
        form = SystemUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            # Save the updated user instance (without updating the password)
            user = form.save(commit=False)
            user.password1 = None
            user.password2 = None
            user.save()

            print("User updated successfully!")
            return redirect(user_list)
        else:
            print("Form is invalid:", form.errors)
    else:
        form = SystemUserUpdateForm(instance=user)
    return render(request, 'update_user.html', {'form': form})


def delete_user(request, username):
    user = get_object_or_404(SystemUsers, username=username)
    if request.method == 'POST':
        user.delete()
        return redirect(user_list)
    return render(request, 'delete_user.html', {'user': user})



def manage_time_slots(request):
    time_slots = TimeSlotSecond.objects.all()
    print("hii")
    # Add logic to handle form submission for adding/editing time slots
    return render(request, 'manage_time_slots.html', {'time_slots': time_slots})

# Superuser view to manage appointments

def manage_appointments(request):  
    appointments = AppointmentSecond.objects.all()
    # Add logic to handle appointment management
    print(appointments)
    return render(request, 'manage_appointments.html', {'appointments': appointments})

# Patient view to view and schedule appointments
def view_and_schedule_appointments(request):
    time_slots = TimeSlotSecond.objects.filter(is_available=True)
    return render(request, 'view_and_schedule_appointments.html', {'time_slots': time_slots})

def add_time_slot(request):
    if request.method == 'POST':
        form = TimeSlotSecondForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(manage_time_slots)  # Redirect to a page showing all time slots
    else:
        form = TimeSlotSecondForm()

    return render(request, 'add_time_slot.html', {'form': form})


def edit_time_slot(request, time_slot_id):
    time_slot = get_object_or_404(TimeSlotSecond, id=time_slot_id)

    if request.method == 'POST':
        form = TimeSlotSecondForm(request.POST, instance=time_slot)
        if form.is_valid():
            form.save()
            return redirect('time_slot_list')  # Redirect to a page showing all time slots
    else:
        form = TimeSlotSecondForm(instance=time_slot)

    return render(request, 'add_time_slot.html', {'form': form, 'time_slot': time_slot})



def delete_time_slot(request, time_slot_id):
    time_slot = get_object_or_404(TimeSlotSecond, id=time_slot_id)
    time_slot.delete()
    return redirect(manage_time_slots)
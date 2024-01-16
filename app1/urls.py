from django.urls import path
from . import views

urlpatterns = [
    path('hi', views.home, name='hom'),
    path('contact', views.contact, name='cont'),
    path('aboutpage', views.aboutpage, name='about'),
    path('', views.userregistration, name='reg'),
    path('logg', views.userlogin, name='log'),
    path('alldetails', views.alldetails,),
    path('onedetails/<str:username>', views.onedetails, name='one'),
    path('logut', views.logoutpage, name='logout'),
    path('prifile', views.profile, name='prof'),
    path('user-approval/', views.user_approval_view, name='user_approval'),
    path('doctorlist', views.doctorlist, name='book_doctor'),
    path('book-appointment/<str:username>/', views.book_appointment, name='book_appointment'),
    path('appointment_pending', views.appointment_pending, name='approve'),
    path('approve_appointment/<str:id>', views.approve_appointment, name='approve_appointment'),
    path('rejectappointment/<int:id>', views.reject_appointment, name='reject_appointment'),
    path('user_lisst', views.user_list, name="userlist"),
    path('user_update/<str:username>', views.update_user, name="userupdate"),
    path('user_delete/<str:username>', views.delete_user, name="userdelete"),
    path('add_time_slote',views.add_time_slot, name='add_time'),
    path('manage_time', views.manage_time_slots, name='manage_time_slots'),
    path('edit_time/<int:time_slot_id>', views.edit_time_slot, name='edit_time_slot'),
    path('delete_time/<int:time_slot_id>', views.delete_time_slot, name='delete_time_slot'),
    path('appointment_manage', views.manage_appointments, name='manage_appointment')

]
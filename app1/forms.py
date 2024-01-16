from django import forms
#from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SystemUsers
from .models import AppointmentSecond,TemporarySecond,TimeSlotSecond


class SystemUserCreationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=SystemUsers.sex, required=False)
    age = forms.IntegerField(required=True)
    number = forms.IntegerField(required=True)
    user_role = forms.ChoiceField(choices=SystemUsers.role , required=True)

    class Meta(UserCreationForm.Meta):
        model = SystemUsers
        fields = ['username','user_role','first_name','last_name','email', 'age','gender','number'] 

class DateInput(forms.DateInput):
    input_type = 'date'

class TemporaryAppointmentForm(forms.ModelForm):
    time_slots = [(str(slot), str(slot)) for slot in TimeSlotSecond.objects.all()]
    time = forms.ChoiceField(choices=time_slots, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = TemporarySecond
        fields = ['datee', 'time', ]

        widgets = {
        'datee': DateInput(),
    }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = AppointmentSecond
        fields = ['date', 'time']
        


class SystemUserUpdateForm(UserCreationForm): 
    class Meta(UserCreationForm.Meta):
        model = SystemUsers
        fields = ['username', 'first_name','last_name','age','email', 'number','user_role']

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', [])
        super().__init__(*args, **kwargs)

        
        for field_name in exclude_fields:
            if field_name in self.fields:
                self.fields.pop(field_name)

        # Make 'password1' and 'password2' non-required
        self.fields['password1'].required = False
        self.fields['password2'].required = False


class TimeSlotSecondForm(forms.ModelForm):
    class Meta:
        model = TimeSlotSecond
        fields = ['time']
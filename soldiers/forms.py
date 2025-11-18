from django import forms
from .models import Soldier
from users.models import User

class SoldierCreateForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False, max_length=15)
    
    class Meta:
        model = Soldier
        fields = ('soldier_id', 'rank', 'unit', 'joining_date', 'assigned_trainer')
    
    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user
        
        # Limit assigned_trainer choices based on user role
        if current_user.role == 'trainer':
            self.fields['assigned_trainer'].queryset = User.objects.filter(id=current_user.id)
            self.fields['assigned_trainer'].initial = current_user
        else:  # admin
            self.fields['assigned_trainer'].queryset = User.objects.filter(role='trainer')
        
        # Add Tailwind classes to form fields
        for field_name, field in self.fields.items():
            if isinstance(field, forms.DateField):
                field.widget.attrs.update({
                    'class': 'input input-bordered w-full bg-army-olive border-army-drab text-white datepicker',
                    'type': 'date'
                })
            else:
                field.widget.attrs.update({
                    'class': 'input input-bordered w-full bg-army-olive border-army-drab text-white'
                })
    
    def save(self, commit=True):
        # First create the user
        user_data = {
            'username': self.cleaned_data['soldier_id'].lower(),
            'email': self.cleaned_data['email'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'phone': self.cleaned_data.get('phone', ''),
            'role': 'soldier',
        }
        
        # Create user with default password (soldier123)
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='soldier123',  # Default password
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            phone=user_data['phone'],
            role=user_data['role']
        )
        
        # Then create the soldier profile
        soldier = super().save(commit=False)
        soldier.user = user
        
        if commit:
            soldier.save()
        
        return soldier

class SoldierEditForm(forms.ModelForm):
    # User fields for editing
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False, max_length=15)
    
    class Meta:
        model = Soldier
        fields = ('soldier_id', 'rank', 'unit', 'joining_date', 'assigned_trainer')
    
    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user
        
        # Limit assigned_trainer choices based on user role
        if current_user.role == 'trainer':
            self.fields['assigned_trainer'].queryset = User.objects.filter(id=current_user.id)
        else:  # admin
            self.fields['assigned_trainer'].queryset = User.objects.filter(role='trainer')
        
        # Add Tailwind classes to form fields
        for field_name, field in self.fields.items():
            if isinstance(field, forms.DateField):
                field.widget.attrs.update({
                    'class': 'input input-bordered w-full bg-army-olive border-army-drab text-white datepicker',
                    'type': 'date'
                })
            else:
                field.widget.attrs.update({
                    'class': 'input input-bordered w-full bg-army-olive border-army-drab text-white'
                })
        
        # Set initial values for user fields
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = self.instance.user.phone
    
    def save(self, commit=True):
        soldier = super().save(commit=False)
        
        # Update user information
        if soldier.user:
            soldier.user.first_name = self.cleaned_data['first_name']
            soldier.user.last_name = self.cleaned_data['last_name']
            soldier.user.email = self.cleaned_data['email']
            soldier.user.phone = self.cleaned_data.get('phone', '')
            soldier.user.save()
        
        if commit:
            soldier.save()
        
        return soldier
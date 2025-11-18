from django import forms
from .models import FitnessRecord

class FitnessRecordForm(forms.ModelForm):
    class Meta:
        model = FitnessRecord
        fields = ('soldier', 'date', 'pushups', 'running_distance', 'running_time', 
                 'bmi', 'shooting_accuracy', 'remarks')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user
        
        # Limit soldier choices based on user role
        from soldiers.models import Soldier
        if current_user.role == 'trainer':
            self.fields['soldier'].queryset = Soldier.objects.filter(assigned_trainer=current_user)
        # Admin can see all soldiers (default)
        
        # Add Tailwind classes to form fields
        for field_name, field in self.fields.items():
            if isinstance(field, forms.DateField):
                field.widget.attrs.update({
                    'class': 'input input-bordered w-full bg-army-olive border-army-drab text-white',
                    'type': 'date'
                })
            elif isinstance(field, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'textarea textarea-bordered w-full bg-army-olive border-army-drab text-white',
                    'rows': 3
                })
            else:
                field.widget.attrs.update({
                    'class': 'input input-bordered w-full bg-army-olive border-army-drab text-white'
                })
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        soldier = cleaned_data.get('soldier')
        
        # Check for duplicate records (same soldier and date)
        if date and soldier:
            existing_record = FitnessRecord.objects.filter(
                soldier=soldier, 
                date=date
            )
            if self.instance:
                existing_record = existing_record.exclude(id=self.instance.id)
            
            if existing_record.exists():
                raise forms.ValidationError(
                    f'A fitness record already exists for {soldier.user.get_full_name()} on {date}.'
                )
        
        # Validate BMI range
        bmi = cleaned_data.get('bmi')
        if bmi and (bmi < 10 or bmi > 50):
            raise forms.ValidationError('BMI must be between 10 and 50.')
        
        # Validate shooting accuracy
        shooting_accuracy = cleaned_data.get('shooting_accuracy')
        if shooting_accuracy and (shooting_accuracy < 0 or shooting_accuracy > 100):
            raise forms.ValidationError('Shooting accuracy must be between 0 and 100.')
        
        return cleaned_data
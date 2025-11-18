from django import forms
from .models import AcademicRecord

class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ('soldier', 'exam_name', 'subject', 'marks', 'total_marks', 'remarks')
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user
        
        # All teachers and admins can see all soldiers for academic records
        from soldiers.models import Soldier
        self.fields['soldier'].queryset = Soldier.objects.all().select_related('user')
        
        # Add Tailwind classes to form fields
        for field_name, field in self.fields.items():
            if isinstance(field, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'textarea textarea-bordered w-full bg-army-olive border-army-drab text-white',
                    'rows': 3
                })
            elif isinstance(field, forms.ChoiceField):
                field.widget.attrs.update({
                    'class': 'select select-bordered w-full bg-army-olive border-army-drab text-white'
                })
            else:
                field.widget.attrs.update({
                    'class': 'input input-bordered w-full bg-army-olive border-army-drab text-white'
                })
    
    def clean(self):
        cleaned_data = super().clean()
        marks = cleaned_data.get('marks')
        total_marks = cleaned_data.get('total_marks')
        
        # Validate marks
        if marks and total_marks:
            if marks > total_marks:
                raise forms.ValidationError('Marks obtained cannot be greater than total marks.')
            
            if marks < 0:
                raise forms.ValidationError('Marks cannot be negative.')
            
            if total_marks <= 0:
                raise forms.ValidationError('Total marks must be greater than zero.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Calculate percentage
        if instance.marks and instance.total_marks:
            instance.percentage = (instance.marks / instance.total_marks) * 100
        
        if commit:
            instance.save()
        
        return instance
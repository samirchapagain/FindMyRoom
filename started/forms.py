from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['title', 'room_type', 'location', 'price', 'contact_phone', 'contact_email', 'beds', 'baths', 'area_m2', 'description', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., A new room in Birtamode', 'class': 'form-control', 'required': True}),
            'room_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter address', 'class': 'form-control', 'required': True}),
            'price': forms.NumberInput(attrs={'placeholder': 'e.g., 5000', 'class': 'form-control', 'required': True}),
            'contact_phone': forms.TextInput(attrs={'placeholder': '+977 9000000000', 'class': 'form-control', 'required': True}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'form-control', 'required': True}),
            'beds': forms.NumberInput(attrs={'min': '1', 'max': '10', 'class': 'form-control', 'value': '1'}),
            'baths': forms.NumberInput(attrs={'min': '1', 'max': '10', 'class': 'form-control', 'value': '1'}),
            'area_m2': forms.NumberInput(attrs={'min': '10', 'max': '1000', 'class': 'form-control', 'value': '25'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your property...', 'class': 'form-control', 'required': True}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['beds'].initial = 1
            self.fields['baths'].initial = 1
            self.fields['area_m2'].initial = 25
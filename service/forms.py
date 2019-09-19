from django import forms
from .models import Services


class AddForm(forms.ModelForm):	
    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        self.fields['cold_water'].initial = '0'
        self.fields['hot_water'].initial = '0'


    class Meta:
        model = Services
        fields = ('cold_water','hot_water', 'electricity', 'gaz',)

        labels = {'cold_water': ('Холодная вода'),
        		  'hot_water': ('Горячая вода'),
                  'electricity': ('Электричество'),
                  'gaz': ('Газ'),
                  }
        

from django import forms
from .models import Services


class AddForm(forms.ModelForm):

    class Meta:
        model = Services
        fields = ('cold_water', 'hot_water', 'electricity', 'gaz',)
        labels = {'cold_water': ('Холодная вода'),
                  'hot_water': ('Горячая вода'),
                  'electricity': ('Электричество'),
                  'gaz': ('Газ'),
                  }
        

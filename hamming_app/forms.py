from django import forms
from .models import Hamming

class FormularioHamming(forms.ModelForm):
    archivo = forms.FileField()
    algoritmo_hamming = forms.CharField()
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Tekniku

class MembroForm(forms.ModelForm):
    class Meta:
        model = Tekniku
        fields = ['id_tekniku', 'naran', 'enderesu', 'email', 'no_tlf']
        labels = {
            'id_tekniku': 'ID Membro',
            'naran': 'Naran',
            'enderesu': 'Enderesu',
            'email': 'Email',
            'no_tlf': 'No. Telefone',
        }
        widgets = {
            'id_tekniku': forms.TextInput(attrs={'class': 'form-control rounded-pill shadow-sm'}),
            'naran': forms.TextInput(attrs={'class': 'form-control rounded-pill shadow-sm'}),
            'enderesu': forms.TextInput(attrs={'class': 'form-control rounded-pill shadow-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill shadow-sm'}),
            'no_tlf': forms.TextInput(attrs={'class': 'form-control rounded-pill shadow-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('id_tekniku', css_class='col-md-6 mb-3'),
                Column('naran', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('enderesu', css_class='col-md-12 mb-3'),
            ),
            Row(
                Column('email', css_class='col-md-6 mb-3'),
                Column('no_tlf', css_class='col-md-6 mb-3'),
            ),
            Submit('submit', '💾 Save', css_class='btn btn-success rounded-pill px-4')
        )

from django import forms
import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Author


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Digite uma data entre agora e 4 semanas (padrão 3)..")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Data inválida - renovação no passado'))

        # Verifique se uma data está no intervalo permitido (+4 semanas a partir de hoje).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data inválida - renovação com mais de 4 semanas de antecedência'))

        # Remember to always return the cleaned data.
        return data


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

import datetime

from django import forms
from django.core.exceptions import ValidationError


def validate_date(date: datetime.date):
    now = datetime.date.today()
    if date >= now:
        raise ValidationError('Data powinna być w przeszłości!', code='date_in_future')


class MovieForm(forms.Form):
    tmdb_id = forms.CharField(max_length=50, required=False, label='TMDB ID')
    title = forms.CharField(max_length=255, label='Tytuł')
    overview = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    release_date = forms.DateField(label='Data produkcji', widget=forms.DateInput(attrs={"type": "date"}),
                                   validators=[validate_date])
    cast = forms.CharField(max_length=255, label='Obsada')
    genres = forms.CharField(max_length=255, label="Gatunki (rozdzielone '|')")
    director = forms.CharField(max_length=255, label='Reżyser')
    keywords = forms.CharField(max_length=1000, label='Słowa kluczowe')

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = f'Pole {field.label} jest wymagane'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'
            visible.field.widget.attrs['style'] = 'background-color: inherit!important'


class MovieCollectionForm(forms.Form):
    name = forms.CharField(max_length=255, label='Nazwa kolekcji', error_messages={
        'max_length': 'Maksymalna długość nazwy kolekcji to 255'
    })

    def __init__(self, *args, **kwargs):
        super(MovieCollectionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = f'Pole {field.label} jest wymagane'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'
            visible.field.widget.attrs['style'] = 'background-color: inherit!important'

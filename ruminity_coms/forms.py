import value as value
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxLengthValidator

from .models import Topic, Subtopic, Entry, Publication


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class SubtopicForm(forms.ModelForm):
    class Meta:
        model = Subtopic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['text', 'description']
        labels = {'text':'Назва твору', 'description':'Текст твору'}
        text = forms.CharField()

    def clean(self):
        super(PublicationForm, self).clean()
        #text = self.cleaned_data.get('text')
        description = self.cleaned_data.get('description')

        if len(description) > 10000:
            self._errors['description'] = self.error_class([
                f'Максимальна кількість символів: 10 000. Ваша кількість символів: {len(description)}'])

        return self.cleaned_data



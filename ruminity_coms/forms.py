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


def check_name(text):
    if text[0].lower() != 'k':
        print(f"TTTTTTTTTTTTTTTTTTTTTTTT{text}")
        raise forms.ValidationError('Name should start with k')



class PublicationForm(forms.ModelForm):
    # def clean(self):
    #     # Get the user submitted names from the cleaned_data dictionary
    #     cleaned_data = super().clean()
    #     text = cleaned_data.get("text")
    #
    #     if text[0].lower() != text[0].lower():
    #         # If not, raise an error
    #         raise ValidationError("The first letters of the names do not match")
    #
    #     return cleaned_data

    class Meta:
        model = Publication
        fields = ['text', 'description']
        #labels = {'text':'Назва твору', 'description':'Текст твору'}
        #text = forms.CharField()
        #description = forms.CharField(widget=forms.Textarea(attrs={'max_length': 30}))
        #text = forms.CharField(validators=[check_name])
        text = forms.CharField()
        # description = forms.CharField(widget=forms.Textarea(attrs={'max_length': 30}))

    def clean(self):
        # data from the form is fetched using super function
        super(PublicationForm, self).clean()
        #text = self.cleaned_data.get('text')
        description = self.cleaned_data.get('description')

        # conditions to be met for the username length
        if len(description) > 10000:
            self._errors['description'] = self.error_class([
                f'Максимальна кількість символів: 10 000. Ваша кількість символів: {len(description)}'])

        # if len(text) < 10:
        #     self._errors['text'] = self.error_class([
        #         'Post Should Contain a minimum of 10 characters'])

        # return any errors if found
        return self.cleaned_data



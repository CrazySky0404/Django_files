from django import forms

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
        widgets = {'description': forms.Textarea(attrs={'rows': 15, 'cols': 10}),}
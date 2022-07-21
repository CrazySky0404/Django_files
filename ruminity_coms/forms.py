from django import forms

from .models import Topic, Subtopic


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
from django import forms

from .models import Topic, Subtopic, Entry, Publication, Comment
from mptt.forms import TreeNodeChoiceField


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


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('name', 'parent', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }
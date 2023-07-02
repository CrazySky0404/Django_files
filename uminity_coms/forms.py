"""
This module provides forms for the Django web framework.

It imports the necessary modules and classes required for defining forms.
"""

from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import (
    Topic,
    Subtopic,
    Publication,
    PublicationComment,
    CompetitionComment,
    SubtopicComment,
)


class TopicForm(forms.ModelForm):
    """
    A form class for creating or updating a Topic model object.
    """

    class Meta:
        """
        Metadata options for the TopicForm class.
        """

        model = Topic
        fields = ["text"]
        labels = {"text": ""}


class SubtopicForm(forms.ModelForm):
    """
    A form class for creating or updating a Subtopic model object.
    """

    class Meta:
        """
        Metadata options for the SubtopicForm class.
        """

        model = Subtopic
        fields = ["text", "description"]
        labels = {"text": "", "description": ""}


class PublicationForm(forms.ModelForm):
    """
    A form class for creating or updating a Publication model object.
    """

    class Meta:
        """
        Metadata options for the PublicationForm class.
        """

        model = Publication
        fields = ["text", "description"]
        labels = {"text": "Назва твору", "description": "Текст твору"}
        text = forms.CharField()

    def clean(self):
        super().clean()
        description = self.cleaned_data.get("description")

        if len(description) > 10000:
            self._errors["description"] = self.error_class(
                [f"Максимальна кількість символів: 10 000. Ваша кількість символів: {len(description)}"]
            )

        return self.cleaned_data


class NewCommentForm(forms.ModelForm):
    """
    A form class for creating a new comment on a publication.
    """

    parent = TreeNodeChoiceField(queryset=PublicationComment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["parent"].widget.attrs.update({"class": "d-none"})
        self.fields["parent"].label = ""
        self.fields["parent"].required = False

    class Meta:
        """
        Initializes the NewCommentForm instance.
        """

        model = PublicationComment
        fields = ("name", "parent", "text")
        widgets = {
            "name": forms.TextInput(attrs={"class": "col-sm-12"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
        }


class CommentFormForum(forms.ModelForm):
    """
    A form class for creating a comment in a forum.
    """

    parent = TreeNodeChoiceField(queryset=SubtopicComment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["parent"].widget.attrs.update({"class": "d-none"})
        self.fields["parent"].label = ""
        self.fields["parent"].required = False

    class Meta:
        """
        Initializes the CommentFormForum instance.
        """

        model = SubtopicComment
        fields = ("name", "parent", "text")
        widgets = {
            "name": forms.TextInput(attrs={"class": "col-sm-12"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
        }


class CommentFormStory(forms.ModelForm):
    """
    A form class for creating a comment in a story.
    """

    parent = TreeNodeChoiceField(queryset=CompetitionComment.objects.all())

    def __init__(self, *args, **kwargs):
        """
        Initializes the CommentFormStory instance.
        """
        super().__init__(*args, **kwargs)

        self.fields["parent"].widget.attrs.update({"class": "d-none"})
        self.fields["parent"].label = ""
        self.fields["parent"].required = False

    class Meta:
        """
        Metadata options for the CommentFormStory class.
        """

        model = CompetitionComment
        fields = ("name", "parent", "text")
        widgets = {
            "name": forms.TextInput(attrs={"class": "col-sm-12"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
        }

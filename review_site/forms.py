from django import forms
from .models import Company, Feedback, Review


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.instance.user = user


class CompanyFormUpdate(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ["user", "image", "cat", "name"]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["mark", "comment"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.instance.user = user

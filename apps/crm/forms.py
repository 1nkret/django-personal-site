from django import forms
from .models import Tag, Project, MainPageSettings


class ProjectForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ["title", "description", "repo_link", "image", "tags"]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "color"]
        widgets = {
            "color": forms.TextInput(attrs={"type": "color"}),
        }


class MainPageSettingsForm(forms.ModelForm):
    class Meta:
        model = MainPageSettings
        fields = ['title', 'subtitle', 'about_me', 'contact_email',
                  'contact_github', 'contact_linkedin', 'contact_telegram']

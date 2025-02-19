from django import forms
from .models import Tag, Project, MainPageSettings, MainPageProjects


class ProjectForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    rating_overall = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )
    rating_difficulty = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )
    rating_usefulness = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )

    class Meta:
        model = Project
        fields = [
            "title", "description", "repo_link",
            "image", "tags", "start_date",
            "end_date", "rating_overall",
            "rating_difficulty", "rating_usefulness"
        ]


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


class MainPageProjectsForm(forms.ModelForm):
    class Meta:
        model = MainPageProjects
        fields = ['projects']

    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
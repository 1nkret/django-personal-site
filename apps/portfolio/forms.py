from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'repo_link', 'image', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),  
        }

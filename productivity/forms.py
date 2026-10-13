from django import forms
from .models import EmployeeProfile

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = [
            "employee_id", "age", "experience_years", "attendance", "working_hours",
            "tasks_completed", "task_delay_count", "training_hours", "meeting_hours",
            "project_count", "performance_score", "job_satisfaction",
        ]
        widgets = {
            "employee_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. EMP-1001"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 18, "max": 70}),
            "experience_years": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 50}),
            "attendance": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100, "step": "0.1"}),
            "working_hours": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 24, "step": "0.5"}),
            "tasks_completed": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "task_delay_count": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "training_hours": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.5"}),
            "meeting_hours": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 24, "step": "0.5"}),
            "project_count": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "performance_score": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100, "step": "0.1"}),
            "job_satisfaction": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 10}),
        }

    def clean_attendance(self):
        value = self.cleaned_data["attendance"]
        if not 0 <= value <= 100:
            raise forms.ValidationError("Attendance must be between 0 and 100.")
        return value

    def clean_performance_score(self):
        value = self.cleaned_data["performance_score"]
        if not 0 <= value <= 100:
            raise forms.ValidationError("Performance score must be between 0 and 100.")
        return value

    def clean_job_satisfaction(self):
        value = self.cleaned_data["job_satisfaction"]
        if not 1 <= value <= 10:
            raise forms.ValidationError("Job satisfaction must be between 1 and 10.")
        return value

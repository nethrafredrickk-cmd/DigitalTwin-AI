from django.db import models
class EmployeeProfile(models.Model):
    employee_id=models.CharField(max_length=40,unique=True)
    age=models.PositiveSmallIntegerField(default=30)
    experience_years=models.PositiveSmallIntegerField(default=5)
    attendance=models.FloatField(default=90)
    working_hours=models.FloatField(default=8)
    tasks_completed=models.PositiveSmallIntegerField(default=20)
    task_delay_count=models.PositiveSmallIntegerField(default=2)
    training_hours=models.FloatField(default=5)
    meeting_hours=models.FloatField(default=1)
    project_count=models.PositiveSmallIntegerField(default=3)
    performance_score=models.FloatField(default=75)
    job_satisfaction=models.PositiveSmallIntegerField(default=7)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.employee_id
class PredictionHistory(models.Model):
    employee=models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE,related_name="predictions")
    productivity_level=models.CharField(max_length=20)
    model_name=models.CharField(max_length=100)
    score=models.FloatField(null=True,blank=True)
    is_trained_model=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

from django.test import TestCase
from django.urls import reverse
from .ml import predict

class PeopleTwinSmokeTests(TestCase):
    def test_dashboard_loads(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Employee Productivity Twin")

    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_employee_form_loads(self):
        self.assertEqual(self.client.get(reverse("employee_create")).status_code, 200)

    def test_fallback_predictor_returns_known_label(self):
        sample = {"age": 30, "experience_years": 5, "attendance": 90,
                  "working_hours": 8, "tasks_completed": 22, "task_delay_count": 3,
                  "training_hours": 6, "meeting_hours": 1, "project_count": 3,
                  "performance_score": 75, "job_satisfaction": 7}
        result = predict(sample)
        self.assertIn(result["level"], {"High", "Moderate", "Low"})
        self.assertIn("trained", result)

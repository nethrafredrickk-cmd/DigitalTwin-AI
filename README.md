# PeopleTwin AI — Employee Productivity Digital Twin
## Full-stack Django case-study implementation

This project is designed to open in VS Code and uses the requested technology stack.

### Technology stack and where each part is used
- **Python** — application logic in `productivity/views.py` and `productivity/ml.py`.
- **Pandas + NumPy** — CSV reading, numeric conversion, missing/non-finite value handling, and metric table output in `productivity/ml.py`.
- **Scikit-learn** — preprocessing pipelines, training, held-out evaluation, and inference in `productivity/ml.py`.
- **Django** — URL routing, validated forms, templates, server-side logic, and JSON endpoints.
- **HTML + CSS + JavaScript + Bootstrap** — templates in `productivity/templates/productivity/`, styles in `productivity/static/productivity/app.css`, and interactive sliders in `simulation.html`.
- **SQLite** — default local database configured in `config/settings.py`; schema is defined in `productivity/models.py`.

## Pages and code map
| Feature | What it does | Where to look |
|---|---|---|
| Overview dashboard | Employee count, prediction totals, recent profiles/history | `templates/productivity/dashboard.html`, `views.py` |
| Employee management | Search, create, edit employee profiles | `models.py`, `forms.py`, `employees.html`, `employee_form.html` |
| Productivity predictor | Validates inputs, predicts a class, saves prediction history | `ml.py`, `views.py`, `predict.html` |
| What-if simulation | Changes scenario sliders and compares illustrative scores | `templates/productivity/simulation.html` |
| Model analytics | Uploads CSV, trains models, displays metrics | `ml.py`, `views.py`, `models.html` |
| JSON API | Health status and prediction endpoint | `productivity/urls.py`, `views.py` |
| Shared design | Navigation, Bootstrap loading, reusable page shell | `base.html`, `app.css` |

## Run in VS Code on Windows
1. Install Python 3.10+ and the Python extension in VS Code.
2. Extract this ZIP, then use **File → Open Folder** to open `PeopleTwin_AI_Django_Demo`.
3. Open **Terminal → New Terminal** and run:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations productivity
python manage.py migrate
python manage.py runserver
```

4. Open `http://127.0.0.1:8000/` in your browser. Stop the server with `Ctrl+C`.

If PowerShell blocks environment activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or invoke `.venv\Scripts\python.exe` directly.

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations productivity
python manage.py migrate
python manage.py runserver
```

## Train a real model from your CSV
Open **Model Analytics** and upload `06_employee_productivity_digital_twin.csv`.

Expected columns:
- Features: `Age`, `Experience_Years`, `Attendance`, `Working_Hours`, `Tasks_Completed`, `Task_Delay_Count`, `Training_Hours`, `Meeting_Hours`, `Project_Count`, `Performance_Score`, `Job_Satisfaction`
- Target: `Productivity_Level`, using labels `High`, `Moderate`, `Low`
- `Employee_ID` is an identifier and is deliberately excluded from the model features.

The pipeline reads the CSV, checks required columns and class labels, converts feature columns to numeric values, handles missing numeric features through median imputation, and makes a stratified 80/20 train/test split. It trains **Logistic Regression**, **Decision Tree**, and **Random Forest**. It reports accuracy, macro precision, macro recall, and macro F1. The classifier with the highest macro F1 on that held-out split is saved as `artifacts/productivity_pipeline.joblib`; metrics are saved to `artifacts/model_metrics.csv`.

**Important:** until a CSV has been uploaded and training completed, the predictor uses a labelled illustrative rule. That fallback is not machine learning, and its scores are not model accuracy. Do not claim an algorithm is best until the actual dataset has been evaluated. For stronger evaluation, use cross-validation, inspect confusion matrices and class-wise recall, and check for data leakage and class imbalance.

## API endpoints
- `GET /api/health/` — basic health check.
- `POST /api/predict/` — JSON prediction endpoint. Send fields named `employee_id`, `age`, `experience_years`, `attendance`, `working_hours`, `tasks_completed`, `task_delay_count`, `training_hours`, `meeting_hours`, `project_count`, `performance_score`, `job_satisfaction`.

Example body:
```json
{
  "employee_id": "EMP-2001", "age": 30, "experience_years": 5,
  "attendance": 92, "working_hours": 8, "tasks_completed": 24,
  "task_delay_count": 2, "training_hours": 6, "meeting_hours": 1,
  "project_count": 3, "performance_score": 80, "job_satisfaction": 8
}
```

For external API clients, account for Django CSRF protection or define a deliberate API authentication policy before deployment.

## Important limitations and deployment checklist
This is a local case-study application, not a hardened production HR system. `DEBUG=True` and the development secret key are only for local use. Before deployment, set secrets through environment variables, disable debug mode, configure allowed hosts and HTTPS, add authentication/authorization, and establish privacy, audit, retention, and model-monitoring practices. Do not use prototype outputs as the sole basis for consequential employment decisions; validate the model and apply human oversight.

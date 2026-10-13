from pathlib import Path
import json
import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from .forms import EmployeeProfileForm
from .models import EmployeeProfile,PredictionHistory
from .ml import predict,train
def dashboard(request):
    levels={x:PredictionHistory.objects.filter(productivity_level__iexact=x).count() for x in ["High","Moderate","Low"]}
    return render(request,"productivity/dashboard.html",{"employees":EmployeeProfile.objects.order_by("-created_at")[:8],"history":PredictionHistory.objects.select_related("employee").order_by("-created_at")[:8],"total":EmployeeProfile.objects.count(),"levels":levels})
def employees(request):
    q=request.GET.get("q","").strip(); rows=EmployeeProfile.objects.order_by("-created_at")
    if q: rows=rows.filter(employee_id__icontains=q)
    return render(request,"productivity/employees.html",{"employees":rows,"query":q})
def employee_form(request,pk=None):
    obj=get_object_or_404(EmployeeProfile,pk=pk) if pk else None
    form=EmployeeProfileForm(request.POST or None,instance=obj)
    if request.method=="POST" and form.is_valid():
        form.save(); messages.success(request,"Employee profile saved."); return redirect("employees")
    return render(request,"productivity/employee_form.html",{"form":form,"editing":bool(obj)})
def predict_view(request):
    form=EmployeeProfileForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        employee_id = form.cleaned_data["employee_id"]
        emp, _created = EmployeeProfile.objects.update_or_create(
            employee_id=employee_id,
            defaults={key: value for key, value in form.cleaned_data.items() if key != "employee_id"},
        )
        result=predict(form.cleaned_data)
        PredictionHistory.objects.create(employee=emp,productivity_level=result["level"],model_name=result["model_name"],score=result["score"],is_trained_model=result["trained"])
        return render(request,"productivity/predict.html",{"form":form,"result":result,"employee":emp})
    return render(request,"productivity/predict.html",{"form":form})
def simulate(request): return render(request,"productivity/simulation.html")
def models(request):
    p=Path(settings.BASE_DIR)/"artifacts"/"model_metrics.csv"
    rows=pd.read_csv(p).to_dict("records") if p.exists() else []
    return render(request,"productivity/models.html",{"metrics":rows,"trained":(Path(settings.BASE_DIR)/"artifacts"/"productivity_pipeline.joblib").exists()})
@require_POST
def train_models(request):
    f=request.FILES.get("dataset")
    if not f: messages.error(request,"Select a CSV first."); return redirect("models")
    try:
        p=Path(settings.BASE_DIR)/"uploaded_dataset.csv"; p.write_bytes(f.read())
        rows,best=train(p)
        messages.success(request,f"Training complete. Best macro F1: {best['model']} ({best['f1_macro']:.3f}).")
    except Exception as e: messages.error(request,"Training failed: "+str(e))
    return redirect("models")
@require_POST
def predict_api(request):
    try:
        data=json.loads(request.body.decode()); form=EmployeeProfileForm(data)
        if not form.is_valid(): return JsonResponse({"error":"Invalid input","details":form.errors.get_json_data()},status=400)
        return JsonResponse(predict(form.cleaned_data))
    except Exception as e: return JsonResponse({"error":str(e)},status=400)
def health(request): return JsonResponse({"status":"ok","application":"PeopleTwin AI","mode":"demo"})

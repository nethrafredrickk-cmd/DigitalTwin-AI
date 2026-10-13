from pathlib import Path
import joblib, pandas as pd, numpy as np
from django.conf import settings
FEATURES=["Age","Experience_Years","Attendance","Working_Hours","Tasks_Completed","Task_Delay_Count","Training_Hours","Meeting_Hours","Project_Count","Performance_Score","Job_Satisfaction"]
MODEL=Path(settings.BASE_DIR)/"artifacts"/"productivity_pipeline.joblib"
def frame(d):
    frame = pd.DataFrame([{"Age":d["age"],"Experience_Years":d["experience_years"],"Attendance":d["attendance"],"Working_Hours":d["working_hours"],"Tasks_Completed":d["tasks_completed"],"Task_Delay_Count":d["task_delay_count"],"Training_Hours":d["training_hours"],"Meeting_Hours":d["meeting_hours"],"Project_Count":d["project_count"],"Performance_Score":d["performance_score"],"Job_Satisfaction":d["job_satisfaction"]}],columns=FEATURES)
    return frame.replace([np.inf, -np.inf], np.nan)
def predict(d):
    if MODEL.exists():
        label=str(joblib.load(MODEL).predict(frame(d))[0]).title()
        return {"level":label,"score":None,"model_name":"Trained Scikit-learn pipeline","trained":True,"message":"Prediction from saved model; validate before real-world use."}
    score=0.28*d["attendance"]+0.24*min(d["tasks_completed"]/30,1)*100+0.2*d["performance_score"]+d["job_satisfaction"]+0.06*min(d["training_hours"]/15,1)*100+0.05*min(d["experience_years"]/15,1)*100-0.3*d["task_delay_count"]-0.4*max(0,d["meeting_hours"]-3)
    score=round(max(0,min(100,score)),1)
    level="High" if score>=76 else "Moderate" if score>=55 else "Low"
    return {"level":level,"score":score,"model_name":"Illustrative demo scoring rule","trained":False,"message":"Not a trained ML prediction. Upload your CSV in Model Analytics to train models."}
def train(csv_path):
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    df=pd.read_csv(csv_path); target="Productivity_Level"
    missing=[c for c in FEATURES+[target] if c not in df.columns]
    if missing: raise ValueError("Missing columns: "+", ".join(missing))
    X=df[FEATURES].apply(pd.to_numeric,errors="coerce").replace([np.inf, -np.inf], np.nan)
    y=df[target].astype(str).str.strip().str.title()
    allowed={"High", "Moderate", "Low"}
    if len(df) < 15: raise ValueError("Please provide at least 15 rows; more data is recommended.")
    if y.isna().any() or y.eq("").any(): raise ValueError("Productivity_Level contains blank labels.")
    if not set(y.unique()).issubset(allowed): raise ValueError("Productivity_Level must contain only High, Moderate, and Low.")
    if y.nunique() < 2 or y.value_counts().min() < 2: raise ValueError("Each target class needs at least two rows, and at least two classes must be present.")
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
    candidates={"Logistic Regression":Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler()),("model",LogisticRegression(max_iter=2000,class_weight="balanced"))]),"Decision Tree":Pipeline([("imputer",SimpleImputer(strategy="median")),("model",DecisionTreeClassifier(random_state=42,class_weight="balanced"))]),"Random Forest":Pipeline([("imputer",SimpleImputer(strategy="median")),("model",RandomForestClassifier(n_estimators=250,random_state=42,class_weight="balanced"))])}
    out=Path(settings.BASE_DIR)/"artifacts"; out.mkdir(exist_ok=True)
    rows=[]
    for name,m in candidates.items():
        m.fit(Xtr,ytr); p=m.predict(Xte)
        row={"model":name,"accuracy":round(accuracy_score(yte,p),4),"precision_macro":round(precision_score(yte,p,average="macro",zero_division=0),4),"recall_macro":round(recall_score(yte,p,average="macro",zero_division=0),4),"f1_macro":round(f1_score(yte,p,average="macro",zero_division=0),4)}
        rows.append(row); joblib.dump(m,out/(name.lower().replace(" ","_")+".joblib"))
    best=max(rows,key=lambda r:r["f1_macro"]); joblib.dump(joblib.load(out/(best["model"].lower().replace(" ","_")+".joblib")),MODEL)
    pd.DataFrame(rows).to_csv(out/"model_metrics.csv",index=False)
    return rows,best

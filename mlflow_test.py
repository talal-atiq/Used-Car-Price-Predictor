import os
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
import mlflow.xgboost
import math
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
from sklearn.linear_model import ElasticNet

# ✅ Path to your models and test data
MODEL_DIR = "models"

# ✅ Load test data
X_test = pd.read_csv(os.path.join(MODEL_DIR, "X_test.csv"))
y_test = pd.read_csv(os.path.join(MODEL_DIR, "y_test.csv"))

# ✅ Load saved models
lr = joblib.load(os.path.join(MODEL_DIR, "linear_regression_model.pkl"))
rf = joblib.load(os.path.join(MODEL_DIR, "random_forest_model.pkl"))
xgb = joblib.load(os.path.join(MODEL_DIR, "xgboost_model.pkl"))
en = joblib.load(os.path.join(MODEL_DIR, "elasticnet_model.pkl"))

# ✅ Define helper to evaluate and log each model
def evaluate_and_log(model, model_name):
    with mlflow.start_run(run_name=model_name):
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        rmse = math.sqrt(mse)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        print(f"\n📊 {model_name} Metrics")
        print(f"  MSE:  {mse:.2f}")
        print(f"  RMSE: {rmse:.2f}")
        print(f"  MAE:  {mae:.2f}")
        print(f"  R2:   {r2:.4f}")

        # Log metrics to MLflow
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # Log model
        if isinstance(model, XGBRegressor):
            mlflow.xgboost.log_model(model, model_name)
        elif isinstance(model, ElasticNet):
            mlflow.sklearn.log_model(model, model_name)
        else:
            mlflow.sklearn.log_model(model, model_name)

# ✅ Evaluate and log each model
evaluate_and_log(lr, "LinearRegression")
evaluate_and_log(rf, "RandomForest")
evaluate_and_log(xgb, "XGBoost")
evaluate_and_log(en, "ElasticNet")

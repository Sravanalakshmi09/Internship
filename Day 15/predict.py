import joblib
import numpy as np

model = joblib.load("model/signalsense_logistic_randomsearch_model.pkl")

scaler = joblib.load("model/signalsense_scaler.pkl")


def predict_data(temperature, humidity, battery):

    data=np.array([[temperature,humidity,battery]])

    data=scaler.transform(data)

    result=model.predict(data)[0]

    if result==0:

        return "Normal"

    else:

        return "Anomaly"
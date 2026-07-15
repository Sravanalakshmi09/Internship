from flask import Flask, render_template, request, redirect

from predict import predict_data

from database import *

app = Flask(__name__)

create_table()


@app.route("/")
def home():

    history = get_history()

    total = len(history)

    normal = len([x for x in history if x[5] == "Normal"])

    anomaly = len([x for x in history if x[5] == "Anomaly"])

    return render_template(
        "index.html",
        total=total,
        normal=normal,
        anomaly=anomaly
    )


@app.route("/predict", methods=["GET","POST"])
def predict():

    prediction = None

    if request.method=="POST":

        device_id=request.form["device_id"].strip()
        temperature=float(request.form["temperature"])
        humidity=float(request.form["humidity"])
        battery=float(request.form["battery"])

        prediction=predict_data(
            temperature,
            humidity,
            battery
        )

        insert_history(
            device_id,
            temperature,
            humidity,
            battery,
            prediction
        )

    return render_template(
        "predict.html",
        prediction=prediction
    )


@app.route("/history")
def history():

    history=get_history()

    return render_template(
        "history.html",
        history=history
    )


@app.route("/delete/<int:id>")
def delete(id):

    delete_history(id)

    return redirect("/history")


if __name__=="__main__":

    app.run(debug=True)
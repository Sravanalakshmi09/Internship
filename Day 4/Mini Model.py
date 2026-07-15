print("THIS IS A NEW CODE")
# ==============================================
# SignalSense - IoT Sensor Anomaly Detection
# Corrected Version
# Dataset: synthetic_iot_dataset.csv
# ==============================================

import pandas as pd
import matplotlib.pyplot as plt
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# ==============================================
# Load Dataset
# ==============================================

df = pd.read_csv("synthetic_iot_dataset.csv")

print("\nFirst 5 Records")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns)

# ==============================================
# TASK 1
# Charts
# ==============================================

# Bar Chart
plt.figure(figsize=(6,4))
df["Anomaly"].value_counts().plot(kind="bar", color=["green","red"])
plt.title("Anomaly Distribution")
plt.xlabel("Anomaly")
plt.ylabel("Count")
plt.savefig("chart_bar.png")
plt.show()

# Scatter Plot
plt.figure(figsize=(6,4))
plt.scatter(df["Temperature"], df["Humidity"], color="blue")
plt.title("Temperature vs Humidity")
plt.xlabel("Temperature")
plt.ylabel("Humidity")
plt.savefig("chart_scatter.png")
plt.show()

# Histogram
plt.figure(figsize=(6,4))
plt.hist(df["Temperature"], bins=10, color="orange")
plt.title("Temperature Distribution")
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.savefig("chart_histogram.png")
plt.show()

# Line Chart
plt.figure(figsize=(6,4))
plt.plot(df["Temperature"], marker="o")
plt.title("Temperature Trend")
plt.xlabel("Index")
plt.ylabel("Temperature")
plt.savefig("chart_line.png")
plt.show()

print("\nTask 1 Completed")

# ==============================================
# TASK 2
# Custom Styled Chart
# ==============================================

avg = df.groupby("Anomaly")["Temperature"].mean()

plt.figure(figsize=(6,4))

plt.bar(
    ["Normal","Anomaly"],
    avg.values,
    color=["green","red"]
)

plt.title("Average Temperature by Class")
plt.xlabel("Sensor Status")
plt.ylabel("Average Temperature")

plt.axhline(
    avg.mean(),
    color="black",
    linestyle="--",
    label="Overall Mean"
)

plt.legend()
plt.savefig("custom_chart.png")
plt.show()

print("Task 2 Completed")

# ==============================================
# Features and Target
# ==============================================

X = df[["Temperature","Humidity","Battery_Level"]]
y = df["Anomaly"]

# ==============================================
# TASK 3
# Train Test Split Explorer
# ==============================================

print("\n========== TASK 3 ==========")

best_accuracy = 0
best_split = 0

for split in [0.1,0.2,0.3]:

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=split,
        random_state=42
    )

    model = LogisticRegression(max_iter=1000)

    model.fit(X_train,y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test,prediction)

    print("\nSplit :",split)
    print("Training Size :",len(X_train))
    print("Testing Size :",len(X_test))
    print("Accuracy :",round(accuracy,4))

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_split = split

print("\nBest Split =",best_split)

# ==============================================
# TASK 4
# Logistic Regression
# ==============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=best_split,
    random_state=42
)

model = LogisticRegression(max_iter=1000)

model.fit(X_train,y_train)

prediction = model.predict(X_test)

print("\n========== TASK 4 ==========")
print("Model Accuracy :",round(accuracy_score(y_test,prediction),4))

new_sensor = pd.DataFrame( [[48, 66, 90]],
    columns=["Temperature", "Humidity", "Battery_Level"])

new_prediction = model.predict(new_sensor)

print("Prediction for New Sensor =",new_prediction[0])

# ==============================================
# TASK 5
# Feature Comparison
# ==============================================

print("\n========== TASK 5 ==========")

features = list(X.columns)

best_feature = ""
best_score = 0

for feature in features:

    X_single = df[[feature]]

    # Use different variable names
    X_train_single, X_test_single, y_train_single, y_test_single = train_test_split(
        X_single,
        y,
        test_size=0.2,
        random_state=42
    )

    m = LogisticRegression(max_iter=1000)

    m.fit(X_train_single, y_train_single)

    pred = m.predict(X_test_single)

    score = accuracy_score(y_test_single, pred)

    print(feature, ":", round(score, 4))

    if score > best_score:
        best_score = score
        best_feature = feature

print("\nBest Feature :", best_feature)

# ==============================================
# TASK 6
# Predicted vs Actual Plot
# ==============================================

print("\n========== TASK 6 ==========")

# Recreate the original test split
X_train_plot, X_test_plot, y_train_plot, y_test_plot = train_test_split(
    X,
    y,
    test_size=best_split,
    random_state=42
)

test_prediction = model.predict(X_test_plot)

plt.figure(figsize=(6,5))

plt.scatter(y_test_plot, test_prediction, color="blue")

plt.plot([0,1],[0,1], color="red")

plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Predicted vs Actual")

plt.savefig("prediction_plot.png")
plt.show()

print("Task 6 Completed")
# ==============================================
# TASK 7
# Save and Load Model
# ==============================================

pickle.dump(model,open("signalsense_model.pkl","wb"))

loaded_model = pickle.load(open("signalsense_model.pkl","rb"))

test_samples = [

    [35,48,60],

    [50,68,90],

    [28,41,30]

]

print("\n========== TASK 7 ==========")

for sample in test_samples:

    result = loaded_model.predict([sample])

    print("Input:",sample," Prediction:",result[0])

print("\nModel Saved Successfully")

# ==============================================
# TASK 8
# Mini Project Summary
# ==============================================

print("\n=================================")
print("PROJECT NAME")
print("SignalSense - IoT Sensor Anomaly Detection Dashboard")

print("\nDATASET")
print("synthetic_iot_dataset.csv")

print("\nFEATURES")
for column in X.columns:
    print("-",column)

print("\nTARGET")
print("Anomaly (0 = Normal, 1 = Anomaly)")

print("\nPROJECT QUESTION")
print("Can Machine Learning Detect IoT Sensor Anomalies?")
print("=================================")

# ==============================================
# Visual Demo
# ==============================================

cm = confusion_matrix(y_test_plot, test_prediction)

plt.figure(figsize=(5,5))

plt.imshow(cm, cmap="Blues")

plt.title("Confusion Matrix")

plt.colorbar()

plt.xticks([0,1],["Normal","Anomaly"])
plt.yticks([0,1],["Normal","Anomaly"])

plt.xlabel("Predicted")
plt.ylabel("Actual")

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, str(cm[i,j]), ha="center", va="center")

plt.savefig("confusion_matrix.png")
plt.show()

print("\nProject Completed Successfully!")
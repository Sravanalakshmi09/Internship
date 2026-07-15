# ============================================================
# SignalSense - IoT Sensor Anomaly Detection Dashboard
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# ============================================================
# Load Dataset
# ============================================================

from pathlib import Path
import pandas as pd

script_dir = Path(__file__).resolve().parent
csv_path = script_dir / "synthetic_iot_dataset.csv"

df = pd.read_csv(csv_path)

print("\nDataset Loaded Successfully\n")

# ============================================================
# Dataset Information
# ============================================================

print("First 5 Rows")
print(df.head())

print("\nShape")
print(df.shape)

print("\nColumns")
print(df.columns)

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows :", df.duplicated().sum())

print("\nStatistical Summary")
print(df.describe())

# ============================================================
# Value Counts
# ============================================================

print("\nTarget Value Counts")
print(df["Anomaly"].value_counts())

# ============================================================
# Encode Device_ID
# ============================================================

encoder = LabelEncoder()
df["Device_ID"] = encoder.fit_transform(df["Device_ID"])

# ============================================================
# Features and Target
# ============================================================

X = df.drop("Anomaly", axis=1)
y = df["Anomaly"]

# ============================================================
# Train Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ============================================================
# Random Forest Model
# ============================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ============================================================
# Prediction
# ============================================================

y_pred = model.predict(X_test)

# ============================================================
# Accuracy
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy")
print(accuracy)

print("\nClassification Report")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

# ============================================================
# Save Model
# ============================================================

pickle.dump(model, open("model.pkl", "wb"))

print("\nModel Saved Successfully")

# ============================================================
# Predict 3 New Cases
# ============================================================

loaded_model = pickle.load(open("model.pkl", "rb"))

sample1 = [[701, 30.5, 45.3, 80]]
sample2 = [[702, 65.0, 52.0, 5]]
sample3 = [[703, 28.0, 48.0, 70]]

print("\nPrediction 1 :", loaded_model.predict(sample1))
print("Prediction 2 :", loaded_model.predict(sample2))
print("Prediction 3 :", loaded_model.predict(sample3))

# ============================================================
# Histogram
# ============================================================

df.hist(figsize=(10,8))
plt.tight_layout()
plt.savefig("histogram.png")
plt.show()

# ============================================================
# Target Distribution
# ============================================================

plt.figure(figsize=(6,4))
sns.countplot(x="Anomaly", data=df)
plt.title("Anomaly Distribution")
plt.savefig("target_distribution.png")
plt.show()

# ============================================================
# Correlation Heatmap
# ============================================================

plt.figure(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("heatmap.png")
plt.show()

# ============================================================
# Feature Importance
# ============================================================

importance = pd.Series(
    model.feature_importances_,
    index=X.columns
)

importance.sort_values().plot(
    kind="barh",
    figsize=(8,5)
)

plt.title("Feature Importance")
plt.savefig("feature_importance.png")
plt.show()

print("\nProject Completed Successfully")
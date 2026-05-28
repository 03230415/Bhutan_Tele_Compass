# =========================================================
# 1. IMPORT LIBRARIES (needed tools)
# =========================================================
import pandas as pd


# =========================================================
# 2. LOAD EXCEL DATASET
# =========================================================
# replace with your actual file name
df = pd.read_excel(r"C:\Users\LENOVO IDEAPAD\Desktop\internship\Project\project\working-in-progress\draft 4 (Responses) (2).xlsx")


# =========================================================
# 3. REMOVE EMPTY COLUMNS
# =========================================================
df = df.dropna(axis=1, how='all')


# =========================================================
# 4. CLEAN COLUMN NAMES (remove hidden spaces/newlines)
# =========================================================
df = df.rename(columns=lambda x: x.replace('\n', ' ').strip())


# =========================================================
# 5. RENAME COLUMNS (make dataset easier to work with)
# =========================================================
df = df.rename(columns={
    "1. usage of service":      "usage_of_service",
    "2. age":                   "age",
    "3. gender":                "gender",
    "4. occupation":            "occupation",
    "5. placement":             "placement",
    "6. used service":          "used_service",
    "7. average time spent Include all internet usage for work, study, social media, entertainment, or communication.": "average_time_spent",
    "8. main purposes":         "purpose",
    "9. reliability":           "reliability",
    "10. factor of choice":     "factor_of_choice",
    "11. satisfaction level":   "satisfaction_level",
    "11. satisfaction with quality":                "quality",
    "11. satisfaction with Data package plan":      "data_package",
    "11.satisfaction with monthly average spending":"spendings",
    "12. overall satisfaction": "overall_satisfaction",
    "13. issue":                "issue",
    "14. changed service":      "changed_service",
    "14. changed company":      "changed_company",
    "7. average time spent (Include all internet usage for work, study, social media, entertainment, or communication.)": "average_time_spent"
})


# =========================================================
# 6. HANDLE MISSING VALUES (overall satisfaction)
# =========================================================
# option A — drop rows with missing target values
df = df.dropna(subset=["overall_satisfaction"])

# convert satisfaction to integer (needed for ML model)
df["overall_satisfaction"] = df["overall_satisfaction"].astype(int)


# =========================================================
# 7. CHECK MISSING VALUES IN ALL COLUMNS
# =========================================================
print(df.isnull().sum())


# =========================================================
# 8. BASIC DATA CLEANING (remove bad rows)
# =========================================================
df = df.dropna(subset=["used_service", "quality", "occupation"])
df = df.drop_duplicates()


# =========================================================
# 9. TEXT NORMALIZATION (standardizing text values)
# =========================================================
df["gender"]      = df["gender"].str.strip().str.lower()
df["occupation"]  = df["occupation"].str.strip().str.lower()
df["used_service"]= df["used_service"].str.strip().str.lower()
df["placement"]   = df["placement"].str.strip().str.lower()
df["purpose"]     = df["purpose"].str.strip().str.lower()
df["usage_of_service"] = df["usage_of_service"].str.strip().str.lower()


# fix inconsistency in occupation labels
df["occupation"] = df["occupation"].replace("university student", "student")


# =========================================================
# 10. DATA INSPECTION (check structure)
# =========================================================
print(df.head())        # preview data
print(df.shape)         # rows and columns
print(df.columns)       # column names


# =========================================================
# 11. CHECK UNIQUE VALUES (detect inconsistencies)
# =========================================================
print(df["gender"].unique())
print(df["occupation"].unique())
print(df["used_service"].unique())

print("\n--- After Cleaning ---")
print(df.shape)
print(df.dtypes)


# =========================================================
# 12. LABEL ENCODING (convert text → numbers for ML)
# =========================================================
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

text_columns = [
    "usage_of_service",
    "age",
    "gender",
    "occupation",
    "placement",
    "used_service",
    "average_time_spent",
    "purpose",
    "factor_of_choice",
    "satisfaction_level",
    "quality",
    "data_package",
    "spendings",
    "issue",
    "changed_service",
    "changed_company"
]

for col in text_columns:
    df[col] = le.fit_transform(df[col].astype(str))


# =========================================================
# 13. FINAL CHECK AFTER ENCODING
# =========================================================
print(df.dtypes)
print(df.head())


# =========================================================
# 14. MACHINE LEARNING IMPORTS
# =========================================================
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# =========================================================
# 15. FEATURE SELECTION (X = inputs for model)
# =========================================================
X = df[[
    "usage_of_service",
    "age",
    "gender",
    "occupation",
    "placement",
    "used_service",
    "average_time_spent",
    "purpose",
    "reliability",
    "factor_of_choice",
    "satisfaction_level",
    "quality",
    "data_package",
    "spendings",
    "issue",
    "changed_service",
    "changed_company"
]]


# =========================================================
# 16. TARGET VARIABLE PREPARATION (y = what we predict)
# =========================================================
# convert satisfaction into categories (low, medium, high)
def group_satisfaction(val):
    if val <= 2:
        return "low"
    elif val == 3:
        return "medium"
    else:
        return "high"

df["overall_satisfaction"] = df["overall_satisfaction"].apply(group_satisfaction)

le2 = LabelEncoder()
y = le2.fit_transform(df["overall_satisfaction"])


# =========================================================
# 17. TRAIN-TEST SPLIT (split data for training/testing)
# =========================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================================================
# 18. TRAIN MACHINE LEARNING MODEL
# =========================================================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# =========================================================
# 19. MODEL PREDICTION + ACCURACY
# =========================================================
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\n--- Detailed Report ---")
print(classification_report(y_test, predictions, zero_division=0))


# =========================================================
# 20. CROSS VALIDATION (model stability check)
# =========================================================
scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validation Average Accuracy: {scores.mean() * 100:.2f}%")
print(f"Each fold: {[f'{s*100:.1f}%' for s in scores]}")


# =========================================================
# 21. FEATURE IMPORTANCE VISUALIZATION
# =========================================================
import matplotlib.pyplot as plt

importances = pd.Series(model.feature_importances_, index=X.columns)
importances = importances.sort_values(ascending=True)

plt.figure(figsize=(10, 7))
importances.plot(kind="barh", color="teal")
plt.title("Which factors affect customer satisfaction the most?")
plt.xlabel("Importance Score")
plt.tight_layout()

plt.savefig("feature_importance.png")
plt.show()

print("\nChart saved as feature_importance.png")


# =========================================================
# END SUMMARY (what your pipeline does)
# =========================================================
# ✔ Data loading
# ✔ Cleaning + renaming
# ✔ Missing value handling
# ✔ Encoding categorical data
# ✔ Training ML model
# ✔ Evaluation
# ✔ Feature importance visualization
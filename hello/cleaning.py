import pandas as pd
# 2. LOAD EXCEL DATASET into DataFrame store in df
df = pd.read_excel(r"C:\Users\LENOVO IDEAPAD\Desktop\internship\Project\project\working-in-progress\draft 4 (Responses) (2).xlsx")
# =========================================================
# 3. REMOVE EMPTY COLUMNS
# keep the data with full columns only
df = df.dropna(axis=1, how='all')
# =========================================================
# 4. CLEAN COLUMN NAMES - make names consistent(remove hidden spaces/line breaks)
df = df.rename(columns=lambda x: x.replace('\n', ' ').strip())
# =========================================================
# 5. RENAME COLUMNS (make dataset easier to work with) - •	ML models need simple, consistent feature names - •	Makes coding easier later 
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
# drop rows with missing target values
# "overall_satisfaction(users satisfaction prediction model) - target y"
df = df.dropna(subset=["overall_satisfaction"])
# convert satisfaction to integer (needed for ML model) - forcing the column into integer format.
df["overall_satisfaction"] = df["overall_satisfaction"].astype(int)
# =========================================================
# 7. CHECK MISSING VALUES 
print(df.isnull().sum())
# =========================================================
# 8. BASIC DATA CLEANING (remove bad rows)
# improtant features for model
df = df.dropna(subset=["used_service", "quality", "occupation"])
df = df.drop_duplicates()
# =========================================================
# 9. TEXT NORMALIZATION (standardizing text values)
# •	Removes spaces •	Makes lowercase •	Standardizes text 
df["gender"]      = df["gender"].str.strip().str.lower()
df["occupation"]  = df["occupation"].str.strip().str.lower()
df["used_service"]= df["used_service"].str.strip().str.lower()
df["placement"]   = df["placement"].str.strip().str.lower()
df["purpose"]     = df["purpose"].str.strip().str.lower()
df["usage_of_service"] = df["usage_of_service"].str.strip().str.lower()
# replacing uni std to only std - merging
df["occupation"] = df["occupation"].replace("university student", "student")
# =========================================================
# 10. check structure
# •	Debugging step 
print(df.head())        # preview data
print(df.shape)         # rows and columns
print(df.columns)       # column names
# =========================================================
# 11. CHECK UNIQUE VALUES (check distinct values)
print(df["gender"].unique())
print(df["occupation"].unique())
print(df["used_service"].unique())
# to make output readable - creates a line "--after cleaning--"
print("\n--- After Cleaning ---")
print(df.shape) #dataset size after cleaning
print(df.dtypes) #data types
# =========================================================
# 12. LABEL ENCODING (convert text → numbers for ML)
from sklearn.preprocessing import LabelEncoder
# Converts text → numbers
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
print(df.dtypes) #ensure everything in numeric
print(df.head())
# =========================================================
# 14. MACHINE LEARNING IMPORTS
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
# =========================================================
# 15. FEATURE SELECTION (X = inputs for model)
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
# convert satisfaction into categories (low, medium, high)
def group_satisfaction(val):
    if val <= 2:
        return "low"
    elif val == 3:
        return "medium"
    else:
        return "high"
df["overall_satisfaction"] = df["overall_satisfaction"].apply(group_satisfaction)
# conerting labels to numbers
le2 = LabelEncoder()
y = le2.fit_transform(df["overall_satisfaction"])
# =========================================================
# 17. TRAIN-TEST SPLIT (split data for training/testing)
# X- inputfeatures, y- target variable
# testsize = 20% and training=80%
# random satte 42 = 42*3group = 126 responses
# “If a user uses BT + has high usage + is a student → satisfaction is usually high”
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# =========================================================
# 18. TRAIN MACHINE LEARNING MODEL
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# =========================================================
# 19. MODEL PREDICTION + ACCURACY
# Ask model to make predictions
# Compare predictions with real answers
# Measure how good the model is
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
# Accuracy: 82.54% - accuracy format 
print(f"\nAccuracy: {accuracy * 100:.2f}%")
print("\n--- Detailed Report ---")
# This gives a FULL breakdown of performance.
# ✔ Precision - When model says “high”, how often is it correct?
# ✔ Recall - Out of all actual “high” cases, how many did it catch?
# ✔ F1-score - Balanced score between precision + recall
print(classification_report(y_test, predictions, zero_division=0))
# =========================================================
# 20. CROSS VALIDATION (model stability check)
# Instead of testing your model once, you are testing it 5cv(parts - accuracies from each) times in different ways.
scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validation Average Accuracy: {scores.mean() * 100:.2f}%")
print(f"Each fold: {[f'{s*100:.1f}%' for s in scores]}")
# =========================================================
# 21. FEATURE IMPORTANCE VISUALIZATION
# 👉 This is used to draw graphs.
import matplotlib.pyplot as plt
# Each number means: How much that feature influenced the model’s decisions
importances = pd.Series(model.feature_importances_, index=X.columns)
# 👉 Orders from least important → most important
importances = importances.sort_values(ascending=True)
# graph size
plt.figure(figsize=(10, 7))
importances.plot(kind="barh", color="teal")
plt.title("Which factors affect customer satisfaction the most?")
plt.xlabel("Importance Score")
plt.tight_layout()
# 👉 Saves graph as a file 
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


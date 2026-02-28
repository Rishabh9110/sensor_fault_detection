import pandas as pd
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyClassifier

# 15 Fast Models (Full dataset pe heavy models lagaye toh PC crash ho jayega, isliye yahi best hain)
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier, PassiveAggressiveClassifier, SGDClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import xgboost as xgb
import lightgbm as lgb
import warnings

warnings.filterwarnings('ignore')

print("🔥 EXTREME MODE ACTIVATED: Loading FULL Dataset (60,000+ rows)...")
print("⚠️ Please be patient. This might take 15-30 minutes depending on your PC's RAM/CPU.")

# Yahan se limit hata di gayi hai! Poora data load hoga.
df = pd.read_csv('data/aps_failure_training_set.csv', na_values="na")

print("🧹 Preprocessing Full Data...")
X = df.drop('class', axis=1)
y = df['class'].map({'neg': 0, 'pos': 1})

# Missing values fill kar rahe hain
numeric_cols = X.select_dtypes(include=['number'])
X = numeric_cols.fillna(numeric_cols.median()).fillna(0)

# 80% Training, 20% Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fast Models List
fast_models = [
    RandomForestClassifier, xgb.XGBClassifier, lgb.LGBMClassifier,
    DecisionTreeClassifier, LogisticRegression, ExtraTreesClassifier,
    AdaBoostClassifier, GradientBoostingClassifier, GaussianNB,
    BernoulliNB, KNeighborsClassifier, RidgeClassifier,
    PassiveAggressiveClassifier, LinearDiscriminantAnalysis, SGDClassifier
]

print("🚀 Running LazyPredict on FULL DATASET. Grab a cup of coffee ☕...")
clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None, classifiers=fast_models)
models, predictions = clf.fit(X_train, X_test, y_train, y_test)

print("\n" + "="*60)
print("🏆 ULTIMATE LAZYPREDICT LEADERBOARD (FULL DATA) 🏆")
print("="*60)
print(models[['Accuracy', 'ROC AUC', 'F1 Score']]) 
print("="*60)
print("✅ DONE! In numbers ko app.py mein update kar do!")
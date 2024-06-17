import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer, StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import  accuracy_score, precision_score, recall_score, f1_score
import warnings

warnings.filterwarnings("ignore")


def no_preparation(X_train, X_val):
    return X_train, X_val


def standardization(X_train, X_val):
    std = StandardScaler()
    X_train_std = std.fit_transform(X_train)
    X_val_std = std.transform(X_val)
    return X_train_std, X_val_std


def normalization(X_train, X_val):
    norm = Normalizer()
    X_train_norm = norm.fit_transform(X_train)
    X_val_norm = norm.transform(X_val)
    return X_train_norm, X_val_norm




def classify(X_train, X_val, y_train, y_val, models):
    preparation_methods = [no_preparation, normalization, standardization]

    results = []

    for i in range(len(preparation_methods)):
        X_train_processed, X_val_processed = preparation_methods[i](X_train, X_val)

        for model, model_name in models:
            model.fit(X_train_processed, y_train)
            y_pred = model.predict(X_val_processed)
            accuracy = accuracy_score(y_val, y_pred)
            precision = precision_score(y_val, y_pred, average='weighted', zero_division=1)
            recall = recall_score(y_val, y_pred, average='weighted', zero_division=1)
            f1 = f1_score(y_val, y_pred, average='weighted', zero_division=1)
            results.append([model_name + " " + preparation_methods[i].__name__, "%.3f" % accuracy, "%.3f" % precision,
                            "%.3f" % recall, "%.3f" % f1])
    return pd.DataFrame(results,
                        columns=["Model", "Accuracy", "Precision", "Recall", "F1-Score"])


data_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/glass/glass.data'
column_names = ['Id', 'RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe', 'Type']
data = pd.read_csv(data_url, names=column_names)

X = data.drop(['Id', 'Type'], axis=1)
y = data['Type']

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=50)

preparation_methods = [no_preparation, normalization, standardization]

models = [
            (DecisionTreeClassifier(random_state=50, max_depth=5, min_samples_split=2),
             "DecisionTreeClassifier {max_depth=5; min_samples_split=2}"),
            (DecisionTreeClassifier(random_state=50, max_depth=8, min_samples_split=5),
             "DecisionTreeClassifier {max_depth=8; min_samples_split=5}"),
            (DecisionTreeClassifier(random_state=50, max_depth=None, min_samples_split=20),
             "DecisionTreeClassifier {max_depth=None; min_samples_split=20}"),

            (GaussianNB(var_smoothing=1e-6), "GaussianNB {var_smoothing=1e-9}"),
            (GaussianNB(var_smoothing=1e-3), "GaussianNB {var_smoothing=1e-6}"),
            (GaussianNB(var_smoothing=1e-1), "GaussianNB {var_smoothing=1e-1}")
        ]
print(data)
print(data.describe())
df = classify(X_train, X_val, y_train, y_val, models)
df.to_csv("classifier_res.csv", index=False)


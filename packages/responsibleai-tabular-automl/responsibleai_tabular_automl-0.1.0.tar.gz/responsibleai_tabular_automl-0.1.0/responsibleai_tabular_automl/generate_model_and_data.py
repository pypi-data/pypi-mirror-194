# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.

import pandas as pd
import shap
import sklearn
from ml_wrappers.model.predictions_wrapper import (
    PredictionsModelWrapperClassification,
    PredictionsModelWrapperRegression,
)
from sklearn.datasets import fetch_california_housing, load_iris
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def get_wrapped_model_and_data_binary_classification():
    X, y = shap.datasets.adult()
    y = [1 if r else 0 for r in y]

    X, y = sklearn.utils.resample(
        X, y, n_samples=1000, random_state=7, stratify=y
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.01, random_state=7, stratify=y
    )
    categorical_features = [
        "Workclass",
        "Education-Num",
        "Marital Status",
        "Occupation",
        "Relationship",
        "Race",
        "Sex",
        "Country",
    ]

    knn = sklearn.neighbors.KNeighborsClassifier()
    knn.fit(X_train, y_train)

    all_data = pd.concat([X_test, X_train])
    model_predict_output = knn.predict(all_data)
    model_predict_proba_output = knn.predict_proba(all_data)
    knn_wrapper = PredictionsModelWrapperClassification(
        all_data, model_predict_output, model_predict_proba_output
    )
    print(knn.classes_)

    X_train["Income"] = y_train
    X_test["Income"] = y_test
    classes = knn.classes_
    target_column_name = "Income"
    task_type = "classification"

    return (
        knn_wrapper,
        X_train,
        X_test,
        categorical_features,
        target_column_name,
        classes,
        task_type,
    )


def get_wrapped_model_and_data_regression():
    housing = fetch_california_housing()
    X_train, X_test, y_train, y_test = train_test_split(
        housing.data,
        housing.target,
        train_size=500,
        test_size=50,
        random_state=7,
    )
    X_train = pd.DataFrame(X_train, columns=housing.feature_names)
    X_test = pd.DataFrame(X_test, columns=housing.feature_names)

    rfc = RandomForestRegressor(n_estimators=10, max_depth=4, random_state=777)
    model = rfc.fit(X_train, y_train)

    all_data = pd.concat([X_test, X_train])
    model_predict_output = model.predict(all_data)
    model_wrapper = PredictionsModelWrapperRegression(
        all_data, model_predict_output
    )

    X_train["target"] = y_train
    X_test["target"] = y_test
    categorical_features = []
    target_column_name = "target"
    classes = None
    task_type = "regression"

    return (
        X_train,
        X_test,
        model_wrapper,
        categorical_features,
        target_column_name,
        classes,
        task_type,
    )


def get_wrapped_model_and_data_multiclass_classification():
    # Import Iris dataset
    iris = load_iris()
    # Split data into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=0
    )
    feature_names = [name.replace(" (cm)", "") for name in iris.feature_names]
    X_train = pd.DataFrame(X_train, columns=feature_names)
    X_test = pd.DataFrame(X_test, columns=feature_names)

    knn = sklearn.neighbors.KNeighborsClassifier()
    knn.fit(X_train, y_train)

    all_data = pd.concat([X_test, X_train])
    model_predict_output = knn.predict(all_data)
    model_predict_proba_output = knn.predict_proba(all_data)
    knn_wrapper = PredictionsModelWrapperClassification(
        all_data, model_predict_output, model_predict_proba_output
    )

    X_train["target"] = y_train
    X_test["target"] = y_test
    categorical_features = []
    target_column_name = "target"
    classes = knn.classes_
    task_type = "classification"
    print(classes)

    return (
        knn_wrapper,
        X_train,
        X_test,
        categorical_features,
        target_column_name,
        classes,
        task_type,
    )


if __name__ == "__main__":
    get_wrapped_model_and_data_binary_classification()
    get_wrapped_model_and_data_regression()
    get_wrapped_model_and_data_multiclass_classification()

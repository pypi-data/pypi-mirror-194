# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.

"""Module for computing and uploading RAI insights for AutoML models."""

from typing import Optional
import pandas as pd
import json
import numpy as np
import warnings
from ml_wrappers.model.predictions_wrapper import (
    PredictionsModelWrapperClassification,
    PredictionsModelWrapperRegression,
)

from azureml.core.runconfig import RunConfiguration
from azureml.core.run import Run
from responsibleai import RAIInsights
from responsibleai.serialization_utilities import serialize_json_safe
from pathlib import Path
from azureml.core import ScriptRunConfig


def _compute_and_upload_rai_insights_internal(
    current_run: Run, automl_child_run: Run
):
    automl_child_run.download_files("outputs/rai")

    metadata = None
    with open("outputs/rai/metadata.json", "r") as fp:
        metadata = json.load(fp)

    train = pd.read_parquet("outputs/rai/train.df.parquet")
    test = pd.read_parquet("outputs/rai/test.df.parquet")
    train_predictions = pd.read_parquet(
        "outputs/rai/predictions.npy.parquet"
    ).values
    test_predictions = pd.read_parquet(
        "outputs/rai/predictions_test.npy.parquet"
    ).values

    if metadata["task_type"] == "classification":
        train_prediction_probabilities = pd.read_parquet(
            "outputs/rai/prediction_probabilities.npy.parquet"
        ).values
        test_prediction_probabilities = pd.read_parquet(
            "outputs/rai/prediction_test_probabilities.npy.parquet"
        ).values
    else:
        train_prediction_probabilities = None
        test_prediction_probabilities = None

    target_column_name = metadata["target_column"]
    task_type = metadata["task_type"]
    classes = metadata["classes"]

    categorical_features = (
        metadata["feature_type_summary"]["Categorical"]
        + metadata["feature_type_summary"]["CategoricalHash"]
    )
    dropped_features = (
        metadata["feature_type_summary"]["Hashes"]
        + metadata["feature_type_summary"]["AllNan"]
        + metadata["feature_type_summary"]["Ignore"]
    )
    datetime_features = metadata["feature_type_summary"]["DateTime"]
    text_features = metadata["feature_type_summary"]["Text"]

    X_test = test.drop(columns=[target_column_name])
    X_train = train.drop(columns=[target_column_name])
    if len(dropped_features) > 0:
        X_test = X_test.drop(columns=dropped_features)
        X_train = X_train.drop(columns=dropped_features)
    all_data = pd.concat([X_test, X_train])
    model_predict_output = np.concatenate(
        (test_predictions, train_predictions)
    )

    if metadata["task_type"] == "classification":
        model_predict_proba_output = np.concatenate(
            (test_prediction_probabilities, train_prediction_probabilities)
        )
        model_wrapper = PredictionsModelWrapperClassification(
            all_data, model_predict_output, model_predict_proba_output
        )
    else:
        model_wrapper = PredictionsModelWrapperRegression(
            all_data, model_predict_output
        )

    train = train.drop(columns=dropped_features)
    test = test.drop(columns=dropped_features)
    if len(text_features) == 0 and len(datetime_features) == 0:
        rai_insights = RAIInsights(
            model=model_wrapper,
            train=train,
            test=test,
            target_column=target_column_name,
            categorical_features=categorical_features,
            task_type=task_type,
            classes=classes,
        )
        rai_insights.explainer.add()
        rai_insights.compute()
        rai_insights.save("dashboard")
        current_run.upload_folder("dashboard", "dashboard")

        rai_data = rai_insights.get_data()
        rai_dict = serialize_json_safe(rai_data)
        ux_json_path = Path("ux_json")
        ux_json_path.mkdir(parents=True, exist_ok=True)
        json_filename = ux_json_path / "dashboard.json"
        with open(json_filename, "w") as json_file:
            json.dump(rai_dict, json_file)
        current_run.upload_folder("ux_json", "ux_json")
    else:
        warnings.warn(
            "Currently RAI is not supported for " "text and datetime features"
        )

    current_run.complete()


def _create_project_folder(
    automl_parent_run_id: str, automl_child_run_id: str
):
    import os
    import shutil

    project_folder = "./automl_experiment_submit_folder"

    os.makedirs(project_folder, exist_ok=True)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    rai_script_path = os.path.join(dir_path, "automl_inference_run.py")
    shutil.copy(rai_script_path, project_folder)

    # shutil.copy("automl_inference_run.py", project_folder)

    script_file_name = os.path.join(project_folder, "automl_inference_run.py")

    # Open the sample script for modification
    with open(script_file_name, "r") as cefr:
        content = cefr.read()

    print(content)
    print(automl_parent_run_id)
    print(automl_child_run_id)
    content = content.replace("<<automl_parent_run_id>>", automl_parent_run_id)

    content = content.replace("<<automl_child_run_id>>", automl_child_run_id)

    print(content)
    # Write sample file into your script folder.
    with open(script_file_name, "w") as cefw:
        cefw.write(content)

    return project_folder


def _create_run_configuration(automl_child_run_id, ws):
    automl_run = ws.get_run(automl_child_run_id)
    run_configuration = RunConfiguration()
    run_configuration.environment = automl_run.get_environment()
    run_configuration.target = "local"
    run_configuration.script = "automl_inference_run.py"
    print(run_configuration)
    return run_configuration


def compute_and_upload_rai_insights(
    automl_parent_run_id: Optional[str] = None,
    automl_child_run_id: Optional[str] = None,
):
    print("The automl child run-id is: " + str(automl_child_run_id))
    print("The automl parent run-id is: " + str(automl_parent_run_id))

    rai_run = Run.get_context()
    print("The current run-id is: " + rai_run.id)

    project_folder = _create_project_folder(
        automl_parent_run_id, automl_child_run_id
    )
    run_configuration = _create_run_configuration(
        automl_child_run_id, rai_run.experiment.workspace
    )

    src = ScriptRunConfig(
        source_directory=project_folder, run_config=run_configuration
    )
    automl_inference_run = rai_run.experiment.submit(config=src)
    automl_inference_run.wait_for_completion()

    automl_run = rai_run.experiment.workspace.get_run(automl_child_run_id)
    _compute_and_upload_rai_insights_internal(rai_run, automl_run)


# compute_and_upload_rai_insights("<<parent_run_id>>", "<<child_run_id>>")

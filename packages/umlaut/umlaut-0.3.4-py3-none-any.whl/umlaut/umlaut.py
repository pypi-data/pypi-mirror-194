import datetime as dt
import os
from contextlib import suppress
from typing import Any

import mlflow
import pandas as pd


class PyfuncWrapper(mlflow.pyfunc.PythonModel):
    """Reusable MLflow pyfunc wrapper"""

    def __init__(self, model):
        """Map variables from model to wrapper
        :model class: The class object of the model to be wrapped and saved in MLflow
        :figures dict: A dictionary of {'<filename>': Plotly graph object} to be logged
        for model performance visualization"""
        self.model = model
        try:
            self.figures: dict = model.figures
        except Exception:
            self.figures = None

    def predict(self, context, model_input: dict):
        """The wrapped model class must have a `run` method which returns a dictionary"""
        return self.model.run(model_input)


class Umlaut:
    """A class for abstracting training and running models in MLflow"""

    def __init__(
        self,
        folder_name: str = None,
        tracking_server: str = None,
    ):
        super().__init__()
        self.DB_USERNAME = os.environ.get("DB_USERNAME")
        self.DB_PASSWORD = os.environ.get("DB_PASSWORD")
        self.DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_PORT = os.environ.get("DB_PORT")

        self.folder_name = folder_name or str(dt.datetime.now())
        self.artifact_location = None

        mlflow.set_tracking_uri(
            f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOSTNAME}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def track_model(
        self,
        model,
        model_name: str = None,
        run_name: str = "Track",
        code_path: list = None,
    ):
        """
        Tracks a new version of the initiated model and pushes it to MLflow.
        :param object model: model to be created or updated
        :param list code_path: A list of local filesystem paths to Python file dependencies (or directories containing
                               file dependencies). These files are prepended to the system path before the model is loaded.
        """
        from mlflow.tracking import MlflowClient

        self.model = model
        self.model_name = model_name
        self.run_name = run_name

        mlf_client = MlflowClient()
        experiment = mlf_client.get_experiment_by_name(f"{self.model_name}")
        try:
            experiment_id = experiment.experiment_id or mlf_client.create_experiment(
                f"{self.model_name}", artifact_location=self.artifact_location
            )
        except AttributeError:
            experiment_id = mlf_client.create_experiment(
                f"{self.model_name}", artifact_location=self.artifact_location
            )

        with mlflow.start_run(experiment_id=experiment_id, run_name=self.run_name):
            self.model = PyfuncWrapper(self.model)
            mlflow.pyfunc.log_model(
                artifact_path="model",
                python_model=self.model,
                code_path=code_path,
                registered_model_name=f"{self.model_name}",
            )

            with suppress(Exception):
                if self.model.figures:
                    """The model `figures: dict` variable is used for logging Plotly performance plots.
                    All figures must be saved as html files.
                    Format: {"<plot_name>.html": plotly.express plot}
                    """
                    for figure_name in self.model.figures:
                        figure = self.model.figures.get(figure_name)
                        mlflow.log_figure(figure, figure_name)

    def run_model(
        self,
        model_name: str = "Default",
        input_config: dict = None,
        result_keys: list = None,
        stage: str = "Production",
        nested_run: bool = False,
    ) -> Any:
        """Runs the registered model with specified inputs.
        :param str model_name: the saved name of the model
        :param dict input_config: input parameters specific to the model
        :param list result_keys: list of items to be stored in results.txt
        :param str stage: stage of the model to be queried
        :param bool nested_run: whether to include a nested model
        :return Any: the result from the model with varying type {dict, list, tuple, or pd.Dataframe}
        """
        import datetime as dt

        from mlflow.tracking import MlflowClient

        mlf_client = MlflowClient()
        experiment_id = mlf_client.get_experiment_by_name(f"{model_name}").experiment_id
        self.model = mlflow.pyfunc.load_model(f"models:/{model_name}/{stage}")
        with mlflow.start_run(
                experiment_id=experiment_id, run_name="Run", nested=nested_run
            ):
            result = self.model.predict(data=input_config)

            mlflow.log_params(
                {
                    "timestamp": dt.datetime.now(),
                    "input_dict": input_config,
                    "model_id": str(self.model.metadata.model_uuid),
                    "model_run_id": str(self.model.metadata.run_id),
                    "model_created": str(self.model.metadata.utc_time_created),
                }
            )
            with suppress():
                if isinstance(result, bool):
                    mlflow.log_metric(key="result", value=1 if result else 0)
                elif isinstance(result, (int, float)):
                    mlflow.log_metric(key="result", value=result)

            with suppress(TypeError):
                if result_keys:
                    """Drop any keys not in result_keys"""
                    result = {k: result[k] for k in result_keys if k in result}

            try:
                log_result: dict = {}
                if isinstance(result, list):
                    log_result = {"result": result}
                elif isinstance(result, (dict, bool)):
                    log_result = result
                elif isinstance(result, tuple):
                    log_result = {y: x for x, y in result}
                elif isinstance(result, pd.DataFrame):
                    log_result = result.to_json(orient="records")
                mlflow.log_text(str(log_result), "results.json")
                with suppress(AttributeError, mlflow.exceptions.MlflowException):
                    """Only log numeric metrics"""
                    mlflow.log_metrics(log_result)
            except AttributeError as e:
                mlflow.log_text(str({"Error": e}), "results.json")

        return result

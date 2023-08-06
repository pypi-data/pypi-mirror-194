# Umlaut

A simpler way to work with MLflow. Umlaut simplifies model deployment and operational analytics for data teams. Centralize critical business logic and track all uses in a single location. Umlaut is built on top of [MLflow](https://bit.ly/3eHJsx3) and offers a simple Python class to assist with tracking and running models. Umlaut is designed to be used by data teams of all sizes and is a great tool for small teams without dedicated data scientists.

Umlaut provides a simple Python class to assist with saving and running models in MLflow. The class has two methods:

- `track_model`: Converts a data science model or block of business logic into an MLflow compatible `model`
- `run_model`: Runs a previously trained `model` and saves audit metadata


### Umlaut offers
- simple commands to track and run models
- history of all inputs and results for model runs
- model lifecycle management
- access to multiple versions of the same model
- a user interface with `MLflow`
- model audit history tracking (roadmap)
- auto-deployed models that can be queried through an API (roadmap)

### Installing Umlaut
`pip install umlaut`

___
## MLflow Setup
[MLflow](https://bit.ly/3eHJsx3) is a powerful machine learning library created by Databricks for data science teams. It offers an extensive API for tracking and running models, but the learning curve can be a deterrent for small teams without dedicated data scientists. Umlaut strips away much of the complexity of MLflow while maintaining the immense value of tracking and running your models in a single location. 

MLflow has two requirements:
1) A model artifact storage location
- This can be a local directory or a cloud storage URI. More info in the MLflow [docs](https://mlflow.org/docs/latest/tracking.html#artifact-stores).
2) A model registry
- The model registry is where model changes and run data are stored. More info in the MLflow [docs](https://mlflow.org/docs/latest/tracking.html#backend-stores).

An `mlflow server` must be running in order to work with Umlaut. The command to start an MLflow server with local artifact storage and a Postgres model registry is as follows:

`mlflow server --backend-store-uri postgresql+psycopg2://admin:password@localhost:5432/database --default-artifact-root "mlruns/"`

Once the server is running you can navigate to the MLflow UI and begin interacting with models.

____
## Core Functionality
Umlaut offers a simple Python class to assist with saving and running business logic in MLflow. The class has two methods:

- `track_model`: Converts a data science model or block of business logic into an MLflow compatible `model`
- `run_model`: Runs a previously trained `model` and saves audit metadata

### Deploying models with Umlaut
Custom `models` can be deployed simply by running `track_model()`. Ensure that the model code block is in a Python `Class` and follow the example below.

```
class ExampleModel():
    """Example business logic that can be wrapped into a model.
       The class must contain a 'run' method with the input config
       mapped to the corresponding model parameters."""

    def business_logic(self, revenue: int) -> bool:
        return revenue > 5

    def run(self, model_input: dict) -> bool:
        return self.business_logic(revenue=model_input.get("revenue"))


if __name__ == "__main__":
    """Saves the model to MLflow in an experiment run"""
    from umlaut import Umlaut

    Umlaut().track_model(
        model=ExampleModel(),
        model_name="Revenue Forecast",
    )
```

This will push the latest changes of `ExampleModel()` to MLflow as a new model version. Navigate to the MLflow server where you can find details for the example "Quarterly Revenue" model.


### Running models with Umlaut
Once a model is deployed in MLflow with `track_model()`, it can be run by calling `run_model()`.

```
from umlaut import Umlaut

result = Umlaut().run_model(
    model_name="Revenue Forecast",
    input_config={"revenue": 3},
    stage="Staging",
)
print(f"Revenue will{'' if result else ' not'} exceed target")
```

Running the simple `Revenue Forecast` model with `revenue = 3` will return `False` as the revenue does not exceed the target of 5. The call to the model will be tracked in MLflow with model inputs and results.

____
## User Interface
`MLflow` provides a useful interface for interacting with models and visualizing their performance.

#### Deploy a `staging` and `production` version of the same model for testing changes before promoting.
<img width="1423" alt="image" src="https://user-images.githubusercontent.com/44371073/219545008-79b5f5bd-78be-4acd-98bb-4775061bdd33.png">

#### Track all model run inputs and outputs.
<img width="1423" alt="image" src="https://user-images.githubusercontent.com/44371073/219547948-3c2146fd-ab87-4844-9b74-2d608c439724.png">

class ExampleModel():
    """Example business logic that can be wrapped into a model.
       The class must contain a 'run' method with the input config
       mapped to the corresponding model parameters."""
    def business_logic(self, revenue: int) -> bool:
        target = 5
        return revenue > target

    def run(self, model_input: dict) -> bool:
        return self.business_logic(revenue=model_input.get("revenue"))


if __name__ == "__main__":
    """Saves the model to MLflow in an experiment run"""
    import os
    import sys

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    from umlaut import Umlaut

    Umlaut().track_model(
        model=ExampleModel(),
        model_name="Revenue Forecast",
        run_name="Track",
    )

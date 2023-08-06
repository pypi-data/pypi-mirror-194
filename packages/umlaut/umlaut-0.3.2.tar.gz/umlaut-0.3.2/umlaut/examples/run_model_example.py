if __name__ == "__main__":
    """Pulls the model from MLflow and runs it with input params"""
    import os
    import sys

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    from umlaut import Umlaut

    result = Umlaut().run_model(
        model_name="Revenue Forecast",
        input_config={"revenue": 3},
        stage="Staging",
    )
    print(f"Revenue will{'' if result else ' not'} exceed target")

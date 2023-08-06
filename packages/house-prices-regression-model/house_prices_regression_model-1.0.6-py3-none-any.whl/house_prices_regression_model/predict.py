import typing as t
import numpy as np
import pandas as pd

from house_prices_regression_model import __version__ as VERSION
from house_prices_regression_model.processing.data_manager import load_pipeline
from house_prices_regression_model.config.core import load_config_file, SETTINGS_PATH
from house_prices_regression_model.processing.data_validation import validate_inputs

# Config files
config = load_config_file(SETTINGS_PATH)
PIPELINE_ARTIFACT_NAME = config["PIPELINE_ARTIFACT_NAME"]
pipeline_file_name = f"{PIPELINE_ARTIFACT_NAME}_v{VERSION}.pkl"
cb_pipe = load_pipeline(file_name=pipeline_file_name)


#Function
def make_prediction(*,input_data: t.Union[pd.DataFrame, dict],) -> list:
    """Make a prediction using a saved model pipeline."""
    df = pd.DataFrame(input_data)
    validated_df, error_dict = validate_inputs(input_data=df)
    errors_list = list(error_dict.values())
    results = {'model_output': None}
    if error_dict == {}:
        log_predictions = cb_pipe.predict(validated_df)
        predictions = [np.exp(pred) for pred in log_predictions]
        results['model_output'] = predictions
    else:
        results['model_output'] = 'Errors making prediction:' + ' '.join(map(str, errors_list))
    return results

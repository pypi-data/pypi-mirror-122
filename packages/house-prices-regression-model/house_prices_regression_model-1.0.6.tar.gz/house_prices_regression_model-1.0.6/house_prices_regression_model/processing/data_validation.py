from house_prices_regression_model.config.core import load_config_file
from house_prices_regression_model.config.core import SETTINGS_PATH

# Config file
config = load_config_file(SETTINGS_PATH)
VARS_NUMERIC = config["VARS_NUM"]
VARS_CATEGORICAL = config["VARS_CAT"]

#Validate inputs
def validate_inputs(input_data):
  validated_df = input_data.copy()
  error_dict = {}

  #Let's validate our data before predicting
  #1) Let's validate the data type of each column
  try:
    validated_df[VARS_NUMERIC] = validated_df[VARS_NUMERIC].astype(float)
    validated_df[VARS_CATEGORICAL] = validated_df[VARS_CATEGORICAL].astype(str)
  except Exception as inst:
    first_error = 'Check the data type of each input variable.'
    error_dict['first_error'] = first_error

  #2) Let's validate the numeric columns are positive numbers.
  # The most important case is for the variable 'GrLivArea' where we apply the log
  try:
    for col in VARS_NUMERIC:
      assert validated_df[col].values[0] > 0
  except Exception as inst:
    second_error = 'Make sure all numeric columns are positive.'
    error_dict['second_error'] = second_error
  return validated_df, error_dict
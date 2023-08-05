# main runner
import argparse
import pandas as pd
from dateutil.relativedelta import relativedelta

# Run from Jupyter
# import forecast.utils as utils
# from forecast.models import DATE_COLUMN_NAME, VALUE_COLUMN_NAME, initialize_model

# Run from pycharm
import utils
from models import DATE_COLUMN_NAME, VALUE_COLUMN_NAME, initialize_model

FREQUENCY_MAPPING = {
    "weekly": "W",
    "monthly": "MS"
}


def get_train_end_date(time_series_df, training_holdout):
    """ Determines the start date for the test data and throws a warning if less than 1 year of training data is included
    """
    training_rows = int(len(time_series_df) * training_holdout)
    train_end_date = time_series_df.iloc[training_rows][DATE_COLUMN_NAME]

    if (train_end_date - time_series_df[DATE_COLUMN_NAME].min()).days < 365:
        print("Warning: Less than 1 year of data provided for training")

    return train_end_date


def run_forecast_ensemble(
        dataframe,
        date_column,
        target_column,
        forecast_horizon_years,
        aggregate_operation="sum",
        training_holdout_pct=0.3,
        frequency=None,
        period_format=None):
    # Initialize with copy of input date
    df = dataframe.copy()
    df[DATE_COLUMN_NAME] = pd.to_datetime(df[date_column])

    # Creates time series and ensures proper naming and frequency
    frequency = FREQUENCY_MAPPING.get(frequency)
    df = utils.create_time_series_from_records(
        df,
        target_column,
        aggregate_operation,
        period_format)
    df = df[[DATE_COLUMN_NAME, VALUE_COLUMN_NAME]]

    # Create Future Forecast Periods
    start_date = pd.to_datetime(dataframe[DATE_COLUMN_NAME]).max() + relativedelta(days=1)
    end_date = start_date + relativedelta(years=forecast_horizon_years)
    period_list = pd.date_range(start=start_date, end=end_date, freq=frequency)

    # Mark dataframe with training/testing split
    train_end_date = get_train_end_date(df, training_holdout_pct)

    # Assemble ensemble of models
    named_model_list = [
        # "GreyKite",
        # "FBProphet",
        # "Naive",
        "XGBoost",
        "RandomForest",
        "SARIMA"
    ]

    # For each model, run a full evaluation and add to the ensemble results
    ensemble = []
    for model_name in named_model_list:
        print(f"    Running --{model_name}")
        model_dict = {"name": model_name}
        model_dict["model"] = initialize_model(model_name)
        results = model_dict["model"].evaluate(
            dataframe=df,
            train_end_date=train_end_date,
            frequency=frequency,
            forecast_period_list=period_list)
        model_dict["predictions"] = results.pop("predictions")
        model_dict["actual"] = results.pop("actual")
        model_dict["forecast"] = results.pop("forecast")
        model_dict["performance_metrics"] = results
        model_dict["weight"] = model_dict["performance_metrics"]["r2"]
        print(model_dict)
        print(f"Number of Predictions: {len(model_dict['predictions'])}")
        ensemble.append(model_dict)
        print("    " + '*' * 50)

    # Combine outputs to calculate ensemble effectiveness
    total_weight = sum([model["weight"] for model in ensemble])
    ensemble_predictions_list = []
    for model in ensemble:
        print(f"    Adding {model['name']} to ensemble")
        model["weight"] = model["weight"] / total_weight
        predictions = pd.Series(model["predictions"]).reset_index(drop=True) * model["weight"]
        actual = pd.Series(model["actual"])
        ensemble_predictions_list.append(predictions)
    ensemble_predictions = sum(ensemble_predictions_list)
    ensemble_actuals = actual

    performance_metrics = utils.get_model_statistics(ensemble_predictions, ensemble_actuals)
    consolidated_metrics = utils.consolidate_scores(performance_metrics, ensemble_actuals.mean())

    degraded_accuracies = {}
    prediction_years = (df[DATE_COLUMN_NAME].max() - df[DATE_COLUMN_NAME].min()).days / 365
    for year in range(0, forecast_horizon_years):
        if year > prediction_years:
            years_outside_of_training = year - prediction_years
            degraded_accuracies[year] = (0.95 ** years_outside_of_training) * consolidated_metrics["composite"]
        else:
            degraded_accuracies[year] = consolidated_metrics["composite"]

    ensemble.append({
        "name": "ensemble",
        "model": None,
        "predictions": ensemble_predictions,
        "actuals": ensemble_actuals,
        "performance_metrics": performance_metrics,
        "consolidated_metrics": consolidated_metrics,
        "weight": None
    })

    return ensemble

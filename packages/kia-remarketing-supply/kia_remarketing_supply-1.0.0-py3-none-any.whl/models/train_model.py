from dask.dataframe.methods import sample
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pickle
from tqdm.auto import tqdm
from pandas.tseries.offsets import MonthEnd
from dateutil.relativedelta import relativedelta
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
from datetime import datetime
from src.features import feature_engineering as fe
from joblib import dump
import mlflow


def shorten_training_range(row, months_offset=5):
    if row["train_months_range"] > months_offset:
        return row["train_end_date"] - pd.DateOffset(months=months_offset)
    else:
        return row["train_start_date"]


def create_train_test_splits(dates, num_train_months=36):
    """Creates a dataframe of training splits from the training data dates.

    Args:
        dates (Timestamps Array): A series of sold dates from the training dataset.

    Returns:
        pd.DataFrame: A DataFrame of training and test split dates.
    """
    data_dict_list = list()

    add_month_ind = 1

    # Rounds the the train date to the first day of the month.
    min_train_date = dates.min().replace(day=1)

    # Rounds the last training date to the last day of the month.
    max_train_date = dates.max() + MonthEnd(1)

    # Creates indices that will be used to subset a dataframe by months.
    train_start_date = min_train_date
    train_end_date = min_train_date + MonthEnd(1)
    while True:
        data_dict = dict()

        train_end_date = min_train_date + MonthEnd(add_month_ind)
        train_start_date = train_end_date - relativedelta(months=num_train_months)
        test_start_date = (min_train_date + MonthEnd(add_month_ind + 1)).replace(day=1)
        test_end_date = min_train_date + MonthEnd(add_month_ind + 1)
        if train_end_date == max_train_date:
            df = pd.DataFrame(data_dict_list)
            return df

        else:
            data_dict["split_ind"] = add_month_ind
            data_dict["train_start_date"] = train_start_date
            data_dict["train_end_date"] = train_end_date
            data_dict["test_start_date"] = test_start_date
            data_dict["test_end_date"] = test_end_date
            data_dict_list.append(data_dict)
        add_month_ind += 1


def train_tss_models(monthly_splits_row, X_y_df, model_save_directory):
    data_dict = dict()

    X_y_df_copy = X_y_df.copy()

    # Filters the training with start and end dates.
    X_y_train_df = X_y_df_copy.loc[
        (
            (X_y_df_copy.index >= monthly_splits_row["train_start_date"])
            & (X_y_df_copy.index <= monthly_splits_row["train_end_date"])
        )
    ]
    X_train_df = X_y_train_df.drop(columns="sale_price")
    y_train_df = X_y_train_df["sale_price"]

    # Filters the test set with start and end dates.
    X_y_test_df = X_y_df_copy.loc[
        (
            (X_y_df_copy.index >= monthly_splits_row["test_start_date"])
            & (X_y_df_copy.index <= monthly_splits_row["test_end_date"])
        )
    ]
    X_test_df = X_y_test_df.drop(columns="sale_price")
    y_test_df = X_y_test_df["sale_price"]

    # Initializes and trains a random forest regressor.
    opt_rf_regr = RandomForestRegressor(n_estimators=111, n_jobs=-1)
    opt_rf_regr.fit(X_train_df, y_train_df)

    # Creates predictions for the test set.
    test_preds = opt_rf_regr.predict(X_test_df)

    # Calculates the r2_score for the test set.
    rf_r2 = r2_score(y_test_df, test_preds)

    # Saves everything.
    dump(
        opt_rf_regr,
        f"{model_save_directory}/{str(monthly_splits_row['split_ind']).zfill(3)}.joblib",
    )
    data_dict["r2_score"] = rf_r2
    data_dict["train_n"] = X_y_train_df.shape[0]
    data_dict["test_n"] = X_y_test_df.shape[0]
    return data_dict


def train_grouped_models(X_df_arr, y_df_arr, model_save_path):
    data_dict_arr = []
    models_arr = []
    for ind in tqdm(range(len(X_df_arr))):
        if ind >= 1:
            if ind == 1:
                X_train = X_df_arr[0]
                y_train = y_df_arr[0]
            else:
                X_train = pd.concat(X_df_arr[0:ind])
                y_train = pd.concat(y_df_arr[0:ind])

            # Initializes, trains, and predicts a randomforest regressor.
            opt_rf_regr = RandomForestRegressor(n_estimators=111, n_jobs=-1)
            opt_rf_regr.fit(X_train, y_train)
            test_preds = opt_rf_regr.predict(X_df_arr[ind])

            # Calculates the r2_score for the random forest and mmr data.
            rf_r2 = r2_score(y_df_arr[ind], test_preds)

            data_dict = {
                "r2_score": rf_r2,
                "test_set_month": f"{X_df_arr[ind].index[0].year}/{X_df_arr[ind].index[0].month}",
                "n": y_df_arr[ind].shape[0],
            }

            # append model and data
            models_arr.append(opt_rf_regr)
            data_dict_arr.append(data_dict)

    with open(model_save_path, "wb") as handle:
        pickle.dump(models_arr, handle, protocol=pickle.HIGHEST_PROTOCOL)

    results_df = pd.DataFrame(data_dict_arr)
    return results_df


def train_fleet_model(fleet_ddf, wide_fleet_ddf, model_save_path, mlflow_run_name, offset_months=18, backtest_months=24, only_train_latest=True):
    best_mae = 1e10
    best_model = None
    pred_df_arr = list()

    test_train_splits_df = create_train_test_splits(
        dates=fleet_ddf["sold_date"], num_train_months=56
    )
    test_train_splits_df = test_train_splits_df.iloc[1:, :]
    subset_test_train_splits_df = test_train_splits_df.tail(backtest_months)

    print(subset_test_train_splits_df)
    
    if not only_train_latest:
        with mlflow.start_run(experiment_id=1, run_name=mlflow_run_name):
            data_dict_arr = list()
            model_arr = list()

            for index, row in tqdm(
                subset_test_train_splits_df.iterrows(),
                total=subset_test_train_splits_df.shape[0],
                desc="Train test split training",
            ):
                data_dict = dict()

                # Splits the test and train sets.
                train_ddf = wide_fleet_ddf.loc[
                    (wide_fleet_ddf["sold_date"] >= row["train_start_date"])
                    & (wide_fleet_ddf["sold_date"] <= row["train_end_date"]),
                    :,
                ]
                test_ddf = wide_fleet_ddf.loc[
                    (wide_fleet_ddf["sold_date"] >= row["test_start_date"])
                    & (wide_fleet_ddf["sold_date"] <= row["test_end_date"]),
                    :,
                ]

                # Get the X and y for both train and test sets.
                sample_weights = (
                    train_ddf["sold_date"]
                    .apply(
                        lambda x: calc_sample_weights(
                            sold_date=x, end_train_date=row["train_end_date"]
                        ),
                        meta=("sold_date", "int64"),
                    )
                    .compute()
                )

                X_train_df = train_ddf.drop(
                    columns=[
                        "secured_date",
                        "date_picked_up",
                        "sold_date",
                        "announced_condition",
                        "auction_family",
                        "auction_state",
                        "recondition_total",
                        "sale_price",
                    ]
                ).compute()
                X_train_df = X_train_df.set_index("vin")
                y_train_df = train_ddf["sale_price"].compute()

                X_test_df = test_ddf.drop(
                    columns=[
                        "secured_date",
                        "date_picked_up",
                        "sold_date",
                        "announced_condition",
                        "auction_family",
                        "auction_state",
                        "recondition_total",
                        "sale_price",
                    ]
                ).compute()
                X_test_df = X_test_df.set_index("vin")
                y_test_df = test_ddf["sale_price"].compute()

                # Checks to see if the training or test set is empty.test_ddf
                if (X_train_df.shape[0] == 0) or (X_test_df.shape[0] == 0):
                    continue

                # Fits the random forest regressor to the training data.
                rf_regr = RandomForestRegressor(n_estimators=111, n_jobs=-1)
                rf_regr.fit(X_train_df, y_train_df, sample_weight=sample_weights)

                # Calcultates predictions and metrics for test set performance.
                preds = rf_regr.predict(X_test_df)
                pred_df = X_test_df.copy()
                pred_df["pred_price"] = preds
                pred_df_arr.append(pred_df)

                err = mean_absolute_error(y_test_df, preds)
                r2 = r2_score(y_test_df, preds)

                # Saves metrics in data dictionary.
                data_dict["train_start_date"] = row["train_start_date"]
                data_dict["train_end_date"] = row["train_end_date"]
                data_dict["test_start_date"] = row["test_start_date"]
                data_dict["test_end_date"] = row["test_end_date"]
                data_dict["ntest"] = X_test_df.shape[0]
                data_dict["mae"] = err
                data_dict["r2"] = r2
                data_dict_arr.append(data_dict)
                
                model_arr.append(rf_regr)

            # Saves the modeling results summary as a .csv file.
            model_results_df = pd.DataFrame(data_dict_arr)
            model_summary_path = (
                f"results/modeling_summary/ts_offset{str(offset_months).zfill(2)}.csv"
            )
            model_results_df.to_csv(model_summary_path, index=False)

            # Calculates summary metrics across the time series models and then logs parameters and metrics into mlflow.
            mean_mae = np.average(model_results_df["mae"], weights=model_results_df["ntest"])
            mean_r2 = np.average(model_results_df["r2"], weights=model_results_df["ntest"])
            mlflow.log_param("num_backtest_months", backtest_months)
            mlflow.log_param("num_offset_months", offset_months)
            mlflow.log_metric("mean_mae", mean_mae)
            mlflow.log_metric("mean_r2", mean_r2)
            mlflow.log_artifact(model_summary_path)
        return pred_df_arr
    else:
        # Saves the model for the best performing avg_mae.
        # Splits the test and train sets.
        final_train_start_date = subset_test_train_splits_df["train_start_date"].values[-1]
        final_train_ddf = wide_fleet_ddf.loc[
            (wide_fleet_ddf["sold_date"] >= final_train_start_date),
            :
        ]
        # Get the X and y for both train and test sets.
        sample_weights = (
            final_train_ddf["sold_date"]
            .apply(
                lambda x: calc_sample_weights(
                    sold_date=x, end_train_date=subset_test_train_splits_df["train_end_date"].values[-1]
                ),
                meta=("sold_date", "int64"),
            )
            .compute()
        )

        final_X_train_df = final_train_ddf.drop(
            columns=[
                "secured_date",
                "date_picked_up",
                "sold_date",
                "announced_condition",
                "auction_family",
                "auction_state",
                "recondition_total",
                "sale_price",
            ]
        ).compute()
        final_X_train_df = final_X_train_df.set_index("vin")
        final_y_train_df = final_train_ddf["sale_price"].compute()

        # Fits the random forest regressor to the training data.
        final_rf_regr = RandomForestRegressor(n_estimators=111, n_jobs=-1)
        final_rf_regr.fit(final_X_train_df, final_y_train_df, sample_weight=sample_weights)

        with open(model_save_path, 'wb') as handle:
            pickle.dump(final_rf_regr, handle, protocol=pickle.HIGHEST_PROTOCOL)

        train_cols = final_X_train_df.columns
        with open('data/external/fleet_cols.pickle', 'wb') as handle:
            pickle.dump(train_cols, handle, protocol=pickle.HIGHEST_PROTOCOL)


def train_regr_model(fleet_ddf, train_start, train_end):
    # Subsets the training data by start and end dates.
    train_ss_ddf = fleet_ddf.loc[
            (fleet_ddf["sold_date"] >= train_start) & (fleet_ddf["sold_date"] <= train_end),
            :
        ]

    # Creates features.
    train_ss_wide_ddf = fe.engineer_fleet_features(train_ss_ddf, dataset_type="train", interim_wide_path="data/interim/wide_fleet.parquet", ohe_pickle_path="data/external/fleet_ohe.pickle")

    # Calculates the sample weights.
    sample_weights = (
        train_ss_wide_ddf["sold_date"]
        .apply(
            lambda x: calc_sample_weights(
                sold_date=x, end_train_date=train_end
            ),
            meta=("sold_date", "int64"),
        )
        .compute()
    )

    # Splits the training set into X and y.
    X_train_ss_wide_df = train_ss_wide_ddf.drop(
        columns=[
            "secured_date",
            "date_picked_up",
            "sold_date",
            "announced_condition",
            "auction_family",
            "auction_state",
            "recondition_total",
            "sale_price",
        ]
    ).compute()

    X_df = X_train_ss_wide_df.set_index("vin")
    y_df = train_ss_wide_ddf["sale_price"].compute()

    # Fits the random forest regressor to the training data.
    final_rf_regr = RandomForestRegressor(n_estimators=111, n_jobs=-1)
    final_rf_regr.fit(X_df, y_df, sample_weight=sample_weights)
    return final_rf_regr

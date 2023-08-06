import numpy as np
import pandas as pd
import dask.dataframe as dd
import calendar
import pickle
from datetime import datetime, date
from sklearn.preprocessing import OneHotEncoder


def extract_season(month):
    """Extracts season string from numeric calendar month.

    Args:
        month (int): Calendar month number.

    Returns:
        string: The season of the month in lower case format.
    """
    if 3 <= month <= 5:
        season = "spring"
    elif 6 <= month <= 8:
        season = "summer"
    elif 9 <= month <= 11:
        season = "fall"
    else:
        season = "winter"
    return season


def create_date_features(sales_vin_ddf, date_column, min_date):
    """Creates date/time related features from the specified date column.

    Args:
        sales_vin_ddf (dask.DataFrame): Dask DataFrame that contains the merged sales_vin data.
        date_column (string): The date column that is used to create features.

    Returns:
        dd.DataFrame: A dask.DataFrame containing the sales_vin_ddf with added features created for the date column.
    """
    sales_vin_ddf["days_from_min"] = sales_vin_ddf[date_column].apply(
        lambda x: (x - min_date).days, meta=(date_column, "int64")
    )

    # Creates a column for the integer month the car was sold.
    sales_vin_ddf["month_sold"] = sales_vin_ddf[date_column].dt.month

    # Creates a column for the season for which the car was sold.
    sales_vin_ddf["season_sold"] = sales_vin_ddf["month_sold"].apply(
        extract_season, meta=("month_sold", "object")
    )

    # Converts the month integer to a string.
    sales_vin_ddf["month_sold"] = (
        sales_vin_ddf["month_sold"]
        .copy()
        .apply(lambda x: calendar.month_name[int(x)], meta=("month_sold", "object"))
    )

    # Extracts the day name from the sold_date.
    sales_vin_ddf["day_name"] = sales_vin_ddf[f"{date_column}"].dt.day_name()

    # Extracts the day of the year.
    sales_vin_ddf["day_of_year"] = sales_vin_ddf[f"{date_column}"].dt.dayofyear

    # Extracts the week number name from the sold_date.
    sales_vin_ddf["year_number"] = sales_vin_ddf[f"{date_column}"].dt.year

    # Calculates difference between the sold year and the model year.
    sales_vin_ddf["year_diff"] = sales_vin_ddf["year_number"] - sales_vin_ddf["year"]

    # Copys and converts some columns to a categorical variable.
    sales_vin_ddf["year_number_cat"] = sales_vin_ddf["year_number"].apply(
        lambda x: str(x), meta=("year_number", "object")
    )

    return sales_vin_ddf


def calc_avg_sale_price(sales_vin_df):

    has_sold_date_df = sales_vin_df.dropna(subset=["sold_date"])

    avg_sale_price = (
        has_sold_date_df.set_index("sold_date")
        .groupby(["model", "trim", "year", pd.Grouper(freq="M")])[["sale_price"]]
        .mean()
        .reset_index()
    )
    avg_sale_price.rename(columns={"sale_price": "prev_avg_sale_price"}, inplace=True)
    return avg_sale_price


def add_regressor_to_future(future_df, regressors_df):
    """
    Adds extra regressors to a `future` DataFrame dataframe created by fbprophet.

    Parameters
    ----------
    data : pandas.DataFrame
        A `future` DataFrame created by the fbprophet `make_future` method

    regressors_df: pandas.DataFrame
        The pandas.DataFrame containing the regressors (with a datetime index)

    Returns
    -------
    futures : pandas.DataFrame
        The `future` DataFrame with the regressors added
    """

    futures = future_df.copy()
    futures.index = pd.to_datetime(futures.ds)
    regressors = pd.concat(regressors_df, axis=1)
    futures = futures.merge(regressors, left_index=True, right_index=True)
    futures = futures.reset_index(drop=True)

    return futures


def engineer_fleet_features(
    fleet_ddf,
    dataset_type,
    interim_wide_path="data/interim/wide_fleet.parquet",
    ohe_pickle_path="data/external/fleet_ohe.pickle",
):
    if dataset_type == "train":
        # Creates date features from sold_date and merges them with the fleet_ddf.
        fleet_fe_ddf = create_date_features(
            fleet_ddf, date_column="sold_date", min_date=datetime(2000, 1, 1)
        )
    elif dataset_type == "test":
        fleet_fe_ddf = create_date_features(
            fleet_ddf, date_column="sim_sold_date", min_date=datetime(2000, 1, 1)
        )

    # Converst to wide format using one hot encoders for categorical variables.
    cat_cols = [
        "auction",
        "model",
        "trim",
        "year_number_cat",
        "month_sold",
        "season_sold",
        "day_name",
    ]

    numer_fleet_fe_ddf = fleet_fe_ddf.drop(columns=cat_cols)

    if dataset_type == "train":
        with open("data/external/fleet_master_ohe.pickle", "rb") as handle:
            ohe = pickle.load(handle)
        wide_fleet_df = pd.DataFrame(
            ohe.fit_transform(fleet_fe_ddf[cat_cols].compute()).toarray()
        )
        wide_fleet_df.columns = list(ohe.get_feature_names().flatten())

    elif dataset_type == "test":
        with open(ohe_pickle_path, "rb") as handle:
            ohe = pickle.load(handle)
        wide_fleet_df = pd.DataFrame(
            ohe.transform(fleet_fe_ddf[cat_cols].compute()).toarray()
        )
        wide_fleet_df.columns = list(ohe.get_feature_names().flatten())

    result_df = pd.concat(
        [
            numer_fleet_fe_ddf.compute().reset_index(drop=True),
            wide_fleet_df.reset_index(drop=True),
        ],
        axis=1,
        ignore_index=True,
    )
    result_df.columns = list(numer_fleet_fe_ddf.columns.values.flatten()) + list(
        ohe.get_feature_names().flatten()
    )

    result_df.columns = (
        result_df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    # Saves the wide formatted fleet data. # fix this ish
    wide_fleet_ddf = dd.from_pandas(result_df, npartitions=5).repartition(
        partition_size="100MB"
    )
    wide_fleet_ddf.to_parquet(interim_wide_path, overwrite=True, engine="pyarrow")
    return wide_fleet_ddf


def save_master_fleet_ohe(fleet_ddf, ohe_pickle_path):
    # Creates date features.
    fleet_fe_ddf = create_date_features(
        fleet_ddf, date_column="sold_date", min_date=datetime(2000, 1, 1)
    )

    # Converst to wide format using one hot encoders for categorical variables.
    cat_cols = [
        "auction",
        "model",
        "trim",
        "year_number_cat",
        "month_sold",
        "season_sold",
        "day_name",
    ]

    # Subsets the fleet_ddf for numeric columns.
    numer_fleet_fe_ddf = fleet_fe_ddf.drop(columns=cat_cols)

    # Initialize a ohe
    ohe = OneHotEncoder(handle_unknown="ignore")
    wide_fleet_df = pd.DataFrame(
        ohe.fit_transform(fleet_fe_ddf[cat_cols].compute()).toarray()
    )

    # Add an additional column for next year.
    ohe_cats = ohe.categories_
    ohe_cats[3] = np.append(ohe_cats[3], str(date.today().year + 1))

    # Sets the category names
    ohe.categories = ohe_cats
    wide_fleet_df = pd.DataFrame(
        ohe.fit_transform(fleet_fe_ddf[cat_cols].compute()).toarray()
    )
    wide_fleet_df.columns = list(ohe.get_feature_names().flatten())

    # Saves the onehotencoders.
    with open(ohe_pickle_path, "wb") as handle:
        pickle.dump(ohe, handle, protocol=pickle.HIGHEST_PROTOCOL)


def calc_sample_weights(sold_date, end_train_date):
    end_train_date = pd.to_datetime(end_train_date)
    months_diff = abs(end_train_date.year - sold_date.year) * 12 + abs(
        end_train_date.month - sold_date.month
    )
    if months_diff <= 1:
        sample_weight = 10

    elif months_diff <= 2:
        sample_weight = 5

    elif months_diff <= 3:
        sample_weight = 4

    elif months_diff <= 6:
        sample_weight = 3

    elif months_diff <= 12:
        sample_weight = 2

    else:
        sample_weight = .5
    return sample_weight


def make_features(fleet_ddf, start_date, end_date):
    # Subsets the data by start and end dates.
    fleet_ss_ddf = fleet_ddf.loc[
        (fleet_ddf["sold_date"] >= start_date) & (fleet_ddf["sold_date"] <= end_date), :
    ]

    if fleet_ss_ddf.shape[0].compute() == 0:
        return None

    # Mean input for grades that are missing.
    fleet_ss_ddf["initial_grade"] = fleet_ss_ddf["initial_grade"].fillna(value=fleet_ss_ddf["initial_grade"].mean())
    fleet_ss_ddf["final_grade"] = fleet_ss_ddf["final_grade"].fillna(value=fleet_ss_ddf["final_grade"].mean())

    # Creates features.
    fe_fleet_ss_ddf = engineer_fleet_features(
        fleet_ss_ddf,
        dataset_type="train",
        interim_wide_path="data/interim/wide_fleet.parquet",
        ohe_pickle_path="data/external/fleet_master_ohe.pickle",
    )
    return fe_fleet_ss_ddf






def split_X_y(fe_fleet_ddf):
    # Splits the training set into X and y.
    X_df = fe_fleet_ddf.drop(
        columns=[
            "secured_date",
            "date_picked_up",
            "sold_date",
            "auction_family",
            "auction_state",
            "sale_price",
        ]
    ).compute()

    X_df = X_df.set_index("vin")
    y_df = fe_fleet_ddf["sale_price"].compute()

    return X_df, y_df

from datetime import timedelta, datetime
import dask.dataframe as dd
import pandas as pd
from glob import glob
from tqdm.auto import tqdm
import numpy as np

def create_simulated_date_column(ddf, num_days_add, is_from_today_date=False):
    """ Creates a simulated sold date using secured date + t(days).

    Args:
        df (dask.dataframe): The sales_vin Dask DataFrame.
        num_days_add (int): The number of days to add.

    Returns:
        dask.dataframe: The sales_vin Dask DataFrame with the added 'sim_sold_date' column.
    """
    sim_ddf = ddf.copy()
    if is_from_today_date:
        sim_ddf["sim_sold_date"] = (datetime.now() + timedelta(days=num_days_add))

    else:
        sim_ddf["sim_sold_date"] = sim_ddf["secured_date"].apply(
            lambda x: x + timedelta(days=num_days_add),
            meta=("secured_date", "datetime64[ns]"),
        )
    return sim_ddf


def simulate_date_column(ddf, year, month, day):
    """ Creates a simulated dataframe for a date.

    Args: 
        ddf (dask.dataframe): The interim sales_vin or fleet_vin Dask DataFrame.
        year (int): The simulated year.
        month (int): The simulated month.
        day (int): The simulated day.

    Returns:
        dask.dataframe: The original dask dataframe with an sim_sold_date column.
    """

    sim_ddf = ddf.copy()
    sim_ddf["sim_sold_date"] = np.datetime64(f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}")
    return sim_ddf


def predict_tss(row, X_y_sim_directory, tss_model_directory):
    data_dict_arr = list()

    all_files = glob(X_y_sim_directory + "/*.parquet")
    all_files = sorted(all_files)
    X_y_sim_ddf_arr = []
    t_ind = 0
    for filename in tqdm(all_files):
        data_dict = dict()

        X_y_sim_ddf = dd.read_parquet(filename)
        X_y_sim_subset_ddf = X_y_sim_ddf.loc[
            row["test_start_date"] : row["test_end_date"]
        ]
        X_sim_subset_df = X_y_sim_subset_ddf.drop(columns=["sale_price"]).compute()
        tss_model = load(
            tss_model_directory + f"/{str(row['split_ind']).zfill(2)}.joblib"
        )
        data_dict["split_ind"] = row["split_ind"]
        data_dict["t_ind"] = t_ind
        data_dict["y_preds"] = tss_model.predict(X_sim_subset_df)

        data_dict_arr.append(data_dict)
        t_ind += 1

    return data_dict_arr


import pandas as pd
import dask.dataframe as dd
import numpy as np
from pandas.tseries.offsets import MonthEnd


def fix_column_names(ddf):
    """ Fixes column names of a DataFrame.

    For all columns; stips whitespace, lowercase, replace space with underscore, remove parathesis.

    Args:
        ddf (dask.dataframe): Dask Dataframe.

    Returns:
        dask.dataframe: A Dask DataFrame with fixed column names.
    """
    # Maps the lowering function to all column names.
    ddf.columns = (
        ddf.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.strip()
    )
    return ddf


def fix_auction_column_typo(ddf):
    """ Fixes the typo for the vehicle colummn.

    Args:
        ddf (dask.dataframe): A Dask DataFrame that contains auction data.

    Returns:
        dask.dataframe: A Dask DataFrame of auction data with the column typo fixed.
    """
    return ddf.rename(columns={"vehcile_miles": "vehicle_miles"})


def fix_auction_dates(ddf):
    """ Converts date strings to numpy timestamps.

    Args:
        ddf (dask.dataframe): The auction Dask DataFrame.

    Returns:
        dask.dataframe: Auction Dask DataFrame with fixed date columns.
    """
    ddf["sold_date"] = dd.to_datetime(ddf["sold_date"])
    ddf["date_picked_up"] = dd.to_datetime(ddf["date_picked_up"])
    ddf["secured_date"] = dd.to_datetime(ddf["secured_date"])
    return ddf


def convert_yesno_to_bool(ddf):
    """ Converts the damage columns from strings of 'Yes'/'No' to a boolean.

    Args:
        ddf (dask.dataframe): The auction Dask DataFrame.

    Returns:
        dask.dataframe: The Dask DataFrame with the damage columns converted to booleans.
    """
    ddf["frame_damage"] = ddf["frame_damage"].fillna("no")
    ddf["major_damage"] = ddf["major_damage"].fillna("no")
    ddf["frame_damage"] = ddf["frame_damage"].apply(lambda x: x.lower() == 'yes', meta=("frame_damage", "bool"))
    ddf["major_damage"] = ddf["major_damage"].apply(lambda x: x.lower() == 'yes', meta=("major_damage", "bool"))
    return ddf


def clean_vin_df(vehicle_master_ddf):
    """ Creates features from the 'model_short_desc' column in the vin DataFrame.

    Args:
        ddf (dask.dataframe): Dask DataFrame that contains vin data.

    Returns:
        dask.dataframe: Vin Dask DataFrame with two more columns for 'is_4x4' and 'is_AWD'.
    """
    # Loads the kma_edm_vehicle_master table, which will be used to merge model year trim into the current fleet inventory.
    vehicle_master_ddf = vehicle_master_ddf[
        [
            "vin",
            "model_year",
            "trim_level_desc",
            "series_desc",
            "model_short_desc",
            "msrp_total_amt",
        ]
    ]

    vehicle_master_ddf["is_4x4"] = vehicle_master_ddf["model_short_desc"].apply(
        lambda x: "4X4" in x.upper(),
        meta=("object", "boolean")
    )
    vehicle_master_ddf["is_awd"] = vehicle_master_ddf["model_short_desc"].apply(
        lambda x: "AWD" in x.upper(), meta=("object", "boolean")
    )
    vehicle_master_ddf = vehicle_master_ddf.drop(columns=["model_short_desc"])
    vehicle_master_ddf = vehicle_master_ddf.rename(
        columns={
            "model_year": "year",
            "trim_level_desc": "trim",
            "series_desc": "model",
            "msrp_total_amt": "msrp",
        }
    )
    return vehicle_master_ddf


def merge_auction_and_vin_df(sales_df, vin_df):
    """ Left merges the auction/sales DataFrame with the vin DataFrame.

    Args:
        sales_df (pandasd.dataframe): Sales Pandas DataFrame.
        vin_df (pandas.dataframe): Vin Pandas DataFrame.

    Returns:
        pandas.dataframe: The merged Pandas DataFrame.
    """

    # Merges the vin specific Kia data into the sales_df.
    sales_vin_df = dd.merge(
        sales_df,
        vin_df[["vin", "ext_desc", "is_4X4", "is_AWD", "msrp"]],
        how="left",
        on="vin",
    )

    return sales_vin_df


def merge_fleet_and_vin_df(fleet_df, vin_df, merge_method="inner"):
    """ Left merges the auction/sales DataFrame with the vin DataFrame.

    Args:
        fleet_df (pandas.dataframe): Fleet Pandas DataFrame.
        vin_df (pandas.dataframe): Vin Pandas DataFrame.

    Returns:
        pandas.dataframe: The merged Pandas DataFrame.
    """
    
    fleet_vin_df = pd.merge(
        fleet_df,
        vin_df[["vin", "ext_desc", "is_4X4", "is_AWD", "msrp"]],
        how=merge_method,
        on="vin",
    )

    return fleet_vin_df

# @task
# def merge_auction_and_msrp(sales_vin_df, vin_msrp_df):
#     return pd.merge(sales_vin_df, vin_msrp_df, how="left", on="vin")


# @task
# def merge_auction_and_avg_price(sales_vin_df, avg_price_df):
#     sales_vin_df = pd.merge(
#         sales_vin_df,
#         avg_price_df,
#         how="left",
#         left_on=["year", "model", "trim", "prev_month_date"],
#         right_on=["year", "model", "trim", "sold_date"],
#     )

#     sales_vin_df.drop(columns=["sold_date_y"], inplace=True)
#     sales_vin_df.rename(columns={"sold_date_x": "sold_date"}, inplace=True)
#     return sales_vin_df


# @task
# def add_prev_month_date(sales_df):
#     sales_df["prev_month_date"] = sales_df["secured_date"] + MonthEnd(-1)
#     return sales_df


# @task
# def filter_no_sold_date(sales_df):
#     return sales_df[sales_df["sold_date"].isna()]


def fix_vehicle_miles(vehicle_mile):
    if vehicle_mile is None:
        return np.nan
    else:
        return float(vehicle_mile.replace(",", ""))


def process_sold_autoims(sold_autoims_ddf):
    # Renames columns
    sold_autoims_ddf = sold_autoims_ddf.rename(
        columns={
            "unibody/frame_damage": "frame_damage",
            "mileage": "vehicle_miles",
            "vehicle_decimal_grade_original_cr": "initial_grade",
            "vehicle_decimal_grade_approved_cr": "final_grade",
        }
    )

    # Converts vehicle_miles to a float64.
    sold_autoims_ddf["vehicle_miles"] = sold_autoims_ddf["vehicle_miles"].apply(
        lambda x: fix_vehicle_miles(x), meta=("object", "float64")
    )

    # Drops data that doesn't have a sale_price.
    sold_autoims_ddf = sold_autoims_ddf.dropna(subset=["sale_price"])

    # Converts sale_price to a float64.
    sold_autoims_ddf["sale_price"] = sold_autoims_ddf["sale_price"].apply(
        lambda x: float(x.replace(",", "").replace("$", "")), meta=("object", "float64")
    )

    # Fixes the dates from objects to datetime64[ns].
    sold_autoims_ddf = fix_auction_dates(sold_autoims_ddf)

    # Converts the yes/no columns to a boolean.
    sold_autoims_ddf = convert_yesno_to_bool(sold_autoims_ddf)

    return sold_autoims_ddf



def fix_flat_index(col):
    if col[-1] == "_":
        return col[:-1]
    else:
        return col
# import modules
import pandas as pd
import numpy as np
import cx_Oracle
import os
import sys
import pickle
from config import keys
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller
from pathlib import PurePath, Path
from tqdm.auto import tqdm


module_path = str(Path.cwd().absolute())
proj_root = module_path
# import pickle5 as pickle
import pickle

# VPN required for this module


def wait_action(driver, xpath, key=0):
    wait_function = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    if key != 0:
        wait_function.send_keys(key)
    else:
        wait_function.click()
    return


def instant_action(driver, xpath, action=1, key=0):
    driver_element = driver.find_element(By.XPATH, xpath)
    if action == 2:
        driver_element.send_keys(key)
    if action == 3:
        driver_element.clear()
    else:
        driver_element.click()
    return


def xpath_format(raw):
    output = "//*[@" + raw.replace('''"''', "'") + "]"
    return output


def get_autoIMS_data(USERNAME, PASSWORD):
    Initial_path = str(Path(PurePath("data", "external")))
    Path(Initial_path).mkdir(parents=True, exist_ok=True)
    chrome_download_path = str(PurePath(proj_root, "data", "external"))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    prefs = {"download.default_directory": chrome_download_path}
    chrome_options.add_experimental_option("prefs", prefs)
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(keys["URL"])
    wait_action(driver, xpath_format('''id="loginUsername"'''), USERNAME)
    wait_action(driver, xpath_format('''id="password"'''), PASSWORD)
    wait_action(driver, xpath_format('''id="submit"'''))
    wait_action(
        driver,
        xpath_format('''href="/jsp/livereports2/showFilters.jsp?rptId=212833"'''),
    )
    wait_action(driver, xpath_format('''href="javascript:doRunSearch()"'''))
    wait_action(driver, xpath_format('''href="/CSVGenerator"'''))
    time.sleep(10)
    filename = max(
        [Initial_path + "\\" + f for f in os.listdir(Initial_path)],
        key=os.path.getctime,
    )

    print(filename)

    print(
        f'Saving autoims data to {str(PurePath(proj_root, "data", "external", "autoims.csv"))}'
    )
    shutil.move(filename, str(PurePath(proj_root, "data", "external", "autoims.csv")))
    print("moved to file correctly")
    print(str(PurePath("data", "external", "autoims.csv")))
    autoims_df = pd.read_csv(str(PurePath("data", "external", "autoims.csv")), skiprows=1)
    print("get auto ims data completed")
    driver.quit()
    return autoims_df


# VPN required for this module


def Oracle_DB_connect(USERNAME, PASSWORD):
    connec = None
    try:
        dsn_tns = cx_Oracle.makedsn("nasipexadb-scan", "1521", service_name="pkwh")
        connec = cx_Oracle.connect(user=USERNAME, password=PASSWORD, dsn=dsn_tns)
    except cx_Oracle.DatabaseError as e:
        print(e)
        print("You need to be on VPN to utilize this module.")
    return connec


def get_current_fleet_preprocess(AIM_user, AIM_pass, connec, skip_aim=False):
    ######## Get Auto IMS Data ########
    if skip_aim:
        autoims_df = pd.read_csv(
            str(PurePath("data", "external", "autoims.csv")), skiprows=1
        )
    else:
        autoims_df = get_autoIMS_data(AIM_user, AIM_pass)

    # rename existing columns to match
    columns = [
        "vin",
        "vehicle_miles",
        "auction_family",
        "auction",
        "auction_state",
        "frame_damage",
        "major_damage",
        "initial_grade",
        "final_grade",
        "date_picked_up",
        "secured_date",
        "sale_price",
        "sold_date",
    ]
    autoims_df.columns = columns

    ##### Get Vin_Master #####
    Path(str(PurePath(proj_root, "data", "pkl"))).mkdir(parents=True, exist_ok=True)

    target_iterable_vin_list = []
    for i in tqdm(range(0, len(autoims_df["vin"]), 100)):
        vins_list = autoims_df["vin"].tolist()[i : i + 100]
        vins_list = [" '" + vin + "' " for vin in vins_list]
        vins_list = ",".join(vins_list)
        target_iterable_vin_list.append(vins_list)
    df_list = []
    for vins_list in tqdm(target_iterable_vin_list):
        sql = f"""SELECT * FROM KMA_PROD.VEHICLE WHERE KMA_PROD.VEHICLE.VIN  IN  ({vins_list}) order by KMA_PROD.VEHICLE.REC_CREATE_DATE desc """
        check = pd.read_sql(sql, connec)
        df_list.append(check)
    result = pd.concat(df_list)
    Vin_Master = result.drop_duplicates(["VIN"], keep="first")

    #### Get trim data and merge ####
    sql = """SELECT * FROM KMA_PROD.TRIM_LEVEL"""
    trim = pd.read_sql(sql, connec)
    trim["SERIESTRIMCD"] = trim["SERIES_CD"].astype(str) + trim["TRIM_LEVEL_CD"].astype(
        str
    )
    trim["REC_CREATE_DATE"] = pd.to_datetime(trim.REC_CREATE_DATE)
    trim = trim.sort_values("REC_CREATE_DATE").drop_duplicates(
        ["SERIESTRIMCD"], keep="last"
    )
    Vin_Master = pd.merge(
        Vin_Master,
        trim,
        how="left",
        left_on=["SERIES_CD", "TRIM_LEVEL_CD"],
        right_on=["SERIES_CD", "TRIM_LEVEL_CD"],
    )

    ### Get model data and merge ###
    sql = """select * from KMA_PROD.MODEL_MASTER"""
    model = pd.read_sql(sql, connec)
    print("Getting data from KMA_PROD.MODEL_MASTER")
    model[["MODEL", "SUBSERIES"]] = model["SERIES_MODEL"].str.split("/", expand=True)
    model["MODEL"] = model["MODEL"].str.strip()
    model["MODELYEARCD"] = model["MODEL_CD"].astype(str) + model["MODEL_YEAR"].astype(
        str
    )
    model["REC_CREATE_DATE"] = pd.to_datetime(model.REC_CREATE_DATE)
    model = model.sort_values("REC_CREATE_DATE").drop_duplicates(
        ["MODELYEARCD"], keep="last"
    )
    Vin_Master["MODELYEARCD"] = Vin_Master["MODEL_CD"].astype(str) + Vin_Master[
        "MODEL_YEAR"
    ].astype(str)
    Vin_Master = Vin_Master.merge(model, how="left", on="MODELYEARCD")

    with open(str(PurePath(proj_root, "data", "pkl", "Vin_Master_CI.pkl")), "wb") as f:
        pickle.dump(Vin_Master, f)

    ###### Gather Fleet Data ######
    sql = """SELECT * FROM (select KMA_PROD.FLEET_VEHICLE.* , 
    rank () over (partition by KMA_PROD.FLEET_VEHICLE.VIN order by KMA_PROD.FLEET_VEHICLE.REC_CREATE_DATE desc) as rnk1 from KMA_PROD.FLEET_VEHICLE)
    x where x.rnk1 = 1
    """
    print("Getting fleet data")

    fleet_all = pd.read_sql(sql, connec)
    fleet_all = fleet_all[["VIN", "TOTAL_REPAIR_DAMAGE_AMT", "AT_RETURN_MILEAGE"]]
    fleet_all.columns = ["vin", "recondition_total", "AT_RETURN_MILEAGE"]

    current_inventory = autoims_df.loc[autoims_df["sold_date"].isna()]
    sold_auto_ims = autoims_df.loc[~autoims_df["sold_date"].isna()]
    current_inventory = autoims_preprocess_general(
        current_inventory, Vin_Master, fleet_all
    )
    print("Preprocessing autoims general")
    sold_auto_ims = autoims_preprocess_general(sold_auto_ims, Vin_Master, fleet_all)

    print("Saving processed current inventory")
    # Pickle and then return training df #
    save_name = str(PurePath(proj_root, "data", "pkl", "current_inventory.pkl"))
    with open(save_name, "wb") as f:
        pickle.dump(current_inventory, f)

    save_name = str(PurePath(proj_root, "data", "pkl", "sold_auto_ims.pkl"))
    with open(save_name, "wb") as f:
        pickle.dump(sold_auto_ims, f)

    return current_inventory


def autoims_preprocess_general(df, Vin_Master, fleet_all):
    df["vehicle_miles"] = (
        df["vehicle_miles"]
        .str.replace("$", "")
        .str.replace(",", "")
        .str.replace(" ", "")
        .astype(np.float64)
    )
    df["major_damage"] = df["major_damage"].fillna("NO")
    df["initial_grade"] = df["initial_grade"].astype(np.float64)
    df["final_grade"] = df["final_grade"].astype(np.float64)
    df["sale_price"] = (
        df["sale_price"]
        .str.replace("$", "")
        .str.replace(",", "")
        .str.replace(" ", "")
        .astype(np.float64)
    )
    df["auction_family"] = df["auction_family"].replace(
        {
            "ADESA": "Adesa",
            "McConkey Auction Group": "Independent",
            """America's Auto Auctions""": "Independent",
        }
    )

    ###### Gather Fleet Data ######
    df = df.merge(fleet_all, how="left", on="vin")

    ## Select necessary data ##
    Vin_Master = Vin_Master[["VIN", "MODEL", "MODEL_YEAR_x", "TRIM_LEVEL_DESC"]]
    Vin_Master.columns = ["vin", "model", "year", "trim"]
    df = df.merge(Vin_Master, how="left", on="vin")

    # fill missing values based on data from other sources
    df["date_picked_up"] = df["date_picked_up"].fillna(df["secured_date"])
    df["vehicle_miles"] = df["vehicle_miles"].fillna(df["AT_RETURN_MILEAGE"])

    # add default values to missing fields.
    df["announced_condition"] = np.nan
    df["frame_damage"] = "no"
    df["major_damage"] = "NO"

    del df["AT_RETURN_MILEAGE"]

    return df


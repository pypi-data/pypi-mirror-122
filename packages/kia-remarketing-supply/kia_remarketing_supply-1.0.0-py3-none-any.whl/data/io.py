from dask.dataframe.io import parquet
import pandas as pd
import dask.dataframe as dd
from glob import glob
#from joblib import dump, load
from tqdm.auto import tqdm
import pickle
import subprocess
import pyarrow as pa
import os
from pyarrow import fs

os.environ["ARROW_LIBHDFS_DIR"] = "/usr/hdp/3.0.1.0-187/usr/lib"

def extract_dfs_from_dir(path, ext="csv"):
    """ Get's all of the files and appends into a list.

    Takes a path that has multiple files that match the extension.
    Then, reads each of the files and appends them to an array.

    Args:
        path (string): The path for the directory that contains the files.
        ext (str, optional): The extension to match for. Defaults to "csv".

    Returns:
        list: An array of pd.Dataframes.
    """
    ext = "/*." + ext
    all_files = glob(path + ext)
    df_arr = []
    for filename in all_files:
        if ext == "/*.csv":
            df = pd.read_csv(filename)
        elif ext == "/*.feather":
            df = pd.read_feather(filename)
        else:
            df = None
        df_arr.append(df)
    return df_arr


def extract_models_arr(path, ext="joblib"):
    """ Get's all of the model joblibs and appends them to a list.

    Takes a path that has multiple files that match the extension.
    Then, reads each of the files and appends them to an array.

    Args:
        path (string): The path for the directory that contains the files.
        ext (str, optional): The extension to match for. Defaults to "/*.joblib".

    Returns:
        list: An array of sklearn trained models.
    """
    ext = "/*." + ext
    all_files = glob(path + ext)
    all_files = sorted(all_files)
    models_arr = []
    for filename in tqdm(all_files):
        if ext == "/*.joblib":
            model = load(filename)
        else:
            model = None
        models_arr.append(model)
    return models_arr


def remove_hive_staging_files(kma_user="kma62139", cluster_type="AC"):
    cluster_host = None
    if cluster_type == "AC":
        cluster_host = "hdfs://kmapb00mn001.pus0c02.hcloud.io"
    elif cluster_type == "HC":
        cluster_host = "kmaph00mn001.pus0c01.hcloud.io"
    hdfs = fs.HadoopFileSystem(cluster_host, user=kma_user)
    file_info_list = hdfs.get_file_info(
        fs.FileSelector("/user/hive/warehouse", recursive=True)
    )

    parquet_file_path_list = [
        cluster_host + file_info.path
        for file_info in file_info_list
    ]
    rm_file_path_list = [parquet_path for parquet_path in parquet_file_path_list if  ".hive-staging" in parquet_path]

    for rm_file_path in rm_file_path_list:
        subprocess.call(["hadoop", "fs", "-rm", "-R", rm_file_path])



def remove_staging_in_parquet_table(table_path, kma_user, cluster_host):
    hdfs_interface = pa.hdfs.connect(host=cluster_host, user=kma_user)
    parquet_files = hdfs_interface.ls(table_path)
    rm_files = [parquet_file for parquet_file in parquet_files if ".hive-staging" in parquet_file]
    for rm_file in rm_files:
        subprocess.call(["hadoop", "fs", "-rm", "-R", rm_file])



# def remove_hive_staging_files_v2(kma_user="kma62139", cluster_type="AC"):
#     cluster_host = None
#     if cluster_type == "AC":
#         cluster_host = "hdfs://kmapb00mn001.pus0c02.hcloud.io"
#     elif cluster_type == "HC":
#         cluster_host = "kmaph00mn001.pus0c01.hcloud.io"
#     hdfs = fs.HadoopFileSystem(cluster_host, user=kma_user)
#     file_info_list = hdfs.get_file_info(
#         fs.FileSelector("/user/hive/warehouse", recursive=True)
#     )

#     parquet_file_path_list = [
#         cluster_host + file_info.path
#         for file_info in file_info_list
#     ]
#     rm_file_path_list = [parquet_path for parquet_path in parquet_file_path_list if  ".hive-staging" in parquet_path]

#     for rm_file_path in rm_file_path_list:
#         subprocess.call(["hadoop", "fs", "-rm", "-R", rm_file_path])


def read_hdfs_parquet(hdfs_host, parquet_directory):
    hdfs = fs.HadoopFileSystem(hdfs_host)
    file_info_list = hdfs.get_file_info(
        fs.FileSelector(parquet_directory, recursive=True)
    )
    parquet_file_path_list = [
        hdfs_host + file_info.path
        for file_info in file_info_list
        if str(file_info.type) != "FileType.Directory"
    ]
    return dd.read_parquet(
        path=parquet_file_path_list, engine="pyarrow", chunk_size="100MB"
    )

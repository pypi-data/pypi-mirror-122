# ---------------------------------------------------------------------------------------------
# convert.py library functions
# ---------------------------------------------------------------------------------------------

#----------------------replace_symbols----------------------

SYMBOLS = {' ': '_', '.': '_', '-': '_', '/':'_'}

def replace_symbols(str_value: str):

    """Replace symbols in the string. 
    SYMBOLS = {' ': '_', '.': '_', '-': '_', '/':'_'}
    """
    for k in SYMBOLS:
        str_value = str_value.replace(k, SYMBOLS[k])
    return str_value

#----------------------label_to_code----------------------
import pandas as pd
from slugify import slugify

def label_to_code(df_value: pd.Series):

    """Ensure ascii transcoding, replace capitals into lowercase, and replace additional symbols"""
    result = df_value
    result.str.encode('ascii', 'ignore')
    result.str.decode('ascii')
    result = result.apply(lambda x: slugify(x))
    result = result.apply(lambda x: replace_symbols(x))
    return result

#----------------------label_to_code_non_slug----------------------
def label_to_code_non_slug(df_value: pd.Series):

    """Ensure ascii transcoding, replace capitals into lowercase, and replace additional symbols"""
    result = df_value
    result.str.encode('ascii', 'ignore')
    result.str.decode('ascii')
    result = result.apply(lambda x: replace_symbols(x))
    return result

#----------------------iso_label----------------------
from iso3166 import countries

def iso_label(country_dict : dict):
    
    """In case we only have ISO code for countries and we want to add label.
    Turn a code:label dict(in that order, label is in this case full of ISO codes) into a ISO:label dict(in that order, label is in this case full of real countries labels).
    """
    result=dict()
    for i in country_dict:
        tmp = countries.get(i)
        result[i]=tmp.name
    return result

#----------------------label_iso----------------------
def label_iso(country_dict : dict):

    """In case we only have label countries and we want to add ISO 3166-1 alpha-3 standard (3-letters ISO code).
    Turn a code:label dict(in that order) into a ISO:label dict(in that order)
    """
    result=dict()
    for i in country_dict.values():
        tmp = countries.get(i)
        result[i]=tmp.alpha3
    inv_result = {v: k for k, v in result.items()}
    return inv_result

#----------------------create_dimenson_dict----------------------
def create_dimenson_dict(df_code: pd.Series, df_label: pd.Series):

    """Two dataframe series are packaged into a code-value dictionary.
    If codes are missing they are generated from labels.
    If labels are missing codes are duplicated.
    """

    if df_code.empty and df_label.empty:
        raise ValueError('Please provide either a non empty list of code or non empty list of label.')

    if df_code.empty:
        df_code = label_to_code(df_label)

    if df_label.empty:
        df_label = df_code

    df_dict = dict(zip(df_code, df_label))

    return df_dict

#----------------------create_name_label----------------------
def create_name_label(ts_dimensions : dict, dict_dim : dict) : 

    """Create a series names label"""
    
    L=[]
    for i in ts_dimensions : 
        tmp = ts_dimensions[i]
        L.append(dict_dim[i][tmp])
    return L

#----------------------datetime_tuple_to_str----------------------
def datetime_tuple_to_str(val:tuple):

    " Transform tuple date into Dbnomics valid string date format: (YYYY,M,D) ==> (YYYY-MM-DD) "
    
    day=str(val[2])
    month=str(val[1])
    year=str(val[0])
    if val[1]<10:
        month='0' + str(val[1])
    if val[2]<10:
        day='0' + str(val[2])
    return year + '-' + month + '-' + day

#----------------------datetime_str_to_str----------------------
def datetime_str_to_str(val:str):
    " Transform string date with hours, minutes and seconds into Dbnomics valid string date format: (YYYY-MM-DD HH:MM:SS) ==> (YYYY-MM-DD) or (YYYY,MM,DD HH:MM:SS) ==> (YYYY-MM-DD)"
    return val.split(' ',1)[0]


#----------------------write_json_file----------------------
from pathlib import Path
import json

def write_json_file(file_path: Path, data: dict):

    """Write data the JSON way to file_path."""
    
    with file_path.open('w', encoding='utf-8') as json_fd:
        json.dump(data, json_fd, ensure_ascii=False, indent=2, sort_keys=True)


#----------------------write_series_jsonl----------------------

def write_series_jsonl(series_filepath: Path, prep_df_list: list):
    """Write series list to series.jsonl file at once."""
    with series_filepath.open('wt', encoding='utf-8') as fd:
        fd.write('\n'.join(map(json.dumps, prep_df_list)))


#----------------------memory_usage----------------------
import os, psutil

def memory_usage():

    "Measure the total memory used by Python process. Result in bytes"
    
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

#----------------------clear_entries_wo_data----------------------

def clear_entries_wo_data(D : dict):

    """Clear dictionaries from entries without data.
    Example : If we input D = {1 : 'A', 2 : '', 3 : 'E'}, the output will be {1: 'A', 3: 'E'}
    """
    return {k: v for k, v in D.items() if v}


#----------------------dataset_json_to_csv----------------------
import csv

def dataset_json_to_csv(source_dir : Path):


    """Convert dataset.json into a csv file"""
    json_file = json.load(open(source_dir,"r",encoding="utf-8"))
    dict_data=json_file['dimensions_values_labels']
    
    def create_list_dimension(dimension_name_code : str):
        # return a list dict_type like with all data from ONE dimension code/label 
        L=[]
        dim_dict=dict()
        for keys in dict_data[dimension_name_code]:
                if keys != 'nan':
                    dim_dict=dict()
                    dim_dict[dimension_name_code + '_code'] = keys
                    dim_dict[dimension_name_code + '_label'] = dict_data[dimension_name_code][keys]
                    L.append(dim_dict)
        return L

    def create_combine_csv():
    
        dim_list_df=[]
        ext='.csv'

        for i in json_file['dimensions_codes_order']:

            dim_csv_file = i + ext

            with open (dim_csv_file , 'w',encoding="utf-8" ) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=[i + '_code' ,i +'_label'])
                writer.writeheader()
                for data in create_list_dimension(i):
                    writer.writerow(data)


            dim_list_df.append(pd.read_csv(dim_csv_file))
            os.remove(dim_csv_file)

        combined_csv=pd.concat(dim_list_df,axis=1)
        combined_csv.to_csv("dataset.csv", index=False, encoding='utf-8-sig')
    
    create_combine_csv()


#----------------------series_jsonl_to_csv----------------------

def series_jsonl_to_csv(source_dir : Path):

    """Convert series.jsonl into a csv file"""

    json_file = []
    for line in open(source_dir, 'r', encoding="utf-8"):
        json_file.append(json.loads(line))
        
    def create_list_observations():
        L=[]
        dim_dict=dict()

        for keys in json_file:

            tmp = keys['observations'][1:]

            for j in range(len(tmp)):
                date = tmp[j][0]
                obs = tmp[j][1]

                dim_dict=dict()
                dim_dict['code'] = keys['code']
                dim_dict['PERIOD'] = date
                dim_dict['VALUE'] = obs

                L.append(dim_dict)

        return L
    
    def create_csv_file():  
        csv_file = 'series.csv' 
        with open (csv_file , 'w',encoding="utf-8-sig",newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['code' ,'PERIOD','VALUE'])
            writer.writeheader()
            for data in create_list_observations():
                writer.writerow(data)
    
    create_csv_file()

# ---------------------------------------------------------------------------------------------
# download.py library functions
# ---------------------------------------------------------------------------------------------

#----------------------downloadIfNewerThanLocal----------------------
import urllib.request
import urllib.error
import logging
from datetime import datetime

log = logging.getLogger(__name__)

def downloadIfNewerThanLocal(sourceURL: str, targetPath: str):

    if Path(targetPath).exists():
        target_timestamp = datetime.fromtimestamp(os.path.getmtime(targetPath))
    else:
        target_timestamp = datetime(1900, 1, 1)

    target_timestamp_str = target_timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    req = urllib.request.Request(url=sourceURL, headers={"If-Modified-Since": target_timestamp_str})

    try:
        u = urllib.request.urlopen(req)

    except urllib.error.HTTPError as e:
        if e.code == 304:
            log.info('no updates for: {}; download aborted'.format(targetPath))
        else:
            log.error('unexpected error for: {};'.format(targetPath))

    else:
        f = open(targetPath, 'wb')
        f.write(u.read())
        f.close()
        log.info('file written {};'.format(targetPath))



# ---------------------------------------------------------------------------------------------
# Recovery of environment variables
# ---------------------------------------------------------------------------------------------
def recov_env_var(env_var:str):
    """Retrieved environment variables from os """
    var=os.environ.get(env_var)
    if len(var)==0:
        log.error('environment variables {} not found'.format(env_var))
        raise ValueError('environment variables {} not found'.format(env_var))
    else:
        return var



# ---------------------------------------------------------------------------------------------
# Arguments
# ---------------------------------------------------------------------------------------------

import argparse

def argument():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source_dir', type=Path, help='path of source directory')
    parser.add_argument('target_dir', type=Path, help='path of target directory')
    parser.add_argument('--log', default='WARNING', help='level of logging messages')
    args = parser.parse_args()

    source_dir = args.source_dir
    if not source_dir.exists():
        parser.error("Source dir {!r} not found".format(str(source_dir)))

    target_dir = args.target_dir
    if not target_dir.exists():
        parser.error("Target dir {!r} not found".format(str(target_dir)))

    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {}'.format(args.log))

    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(asctime)s:%(message)s",
        level=numeric_level,
        handlers=[logging.FileHandler(target_dir / "debug.log"), logging.StreamHandler()]
    )
    
    return (source_dir,target_dir)


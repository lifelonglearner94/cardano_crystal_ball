from serpapi import GoogleSearch
from sqlite3_cache import Cache
from cardano_crystal_ball.helper.file_system_helper import get_from_env
import pandas as pd
from cardano_crystal_ball.helper.file_system_helper import search_upwards

TIMEOUT=60*60*24*5 # 5 Tage

cache = Cache(filename='cache.db',
              path = search_upwards('raw_data')/"raw_data",
              in_memory=False,
              timeout=TIMEOUT
              )

def get_trends(kw_list):
    key = "get_trends-"+",".join(kw_list)
    csv_result = get_trends_from_cache(key)
    if csv_result == None:
        print ("+++++++ not in the cache "+key)
        params = {
        "api_key": get_from_env("SERPAPI_KEY"),
        "engine": "google_trends",
        "q": ",".join(kw_list),
        "data_type": "TIMESERIES",
        "csv": "true",
        "date": "today 5-y",
        "no_cache": "true"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        csv_result = results.get('csv')
        put_trends_to_cache(key,csv_result)
    result = format_result_as_dataframe(csv_result)
    # results.to_csv(search_upwards('raw_data')/'raw_data/serpapi.csv')
    result.to_csv(search_upwards('raw_data')/('raw_data/' + get_from_env("NAME_TRENDS_CSV")))
    return result

def format_result_as_dataframe(csv_result):
    result = []
    for row in csv_result[3:]:
        result.append(row.split(","))
    df = pd.DataFrame(result)
    df.columns = ["Week","Bitcoin","Cardano","cardano price","cryptocurrency","Ethereum"]
    df.index = df['Week']
    df = df.drop("Week",axis=1)
    df.head()
    return df

def get_trends_from_cache(key):
    result = cache.get(key, default=None)
    if result:
        print ("+++++++ key found in cache "+key)
    return result

def put_trends_to_cache(key, value, timeout = TIMEOUT):
    print ("+++++++ write to cache "+key)
    return cache.set(key, value, timeout)

if __name__ == "__main__":
    results = get_trends(["Bitcoin","Cardano","cardano price","cryptocurrency","Ethereum"])
    results.to_csv(search_upwards('raw_data')/'raw_data/serpapi.csv')
    # print (results)

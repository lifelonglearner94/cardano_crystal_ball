from cardano_crystal_ball.apis.live_coin_watch.utils import *
from cardano_crystal_ball.params import *

def load_more_livecoin_data_and_save(start: str, end: str, full_data=False):
    '''Input shapes need to be YYYY-MM-DD HH:MM:SS'''

    dir_path = os.path.join(LOCAL_DATA_PATH, 'raw')

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    df = get_alot_of_data(start, end)

    df = df.drop_duplicates()

    df["date"] = pd.to_datetime(df["date"])

    df.set_index("date", drop=True, inplace=True)


    start = start.replace(":", "_").replace(" ", "_")
    end = end.replace(":", "_").replace(" ", "_")
    if full_data == False:
        the_path = os.path.join(LOCAL_DATA_PATH, 'raw', f"livecoin_from_{start}_to_{end}.csv")
    else:
        the_path = os.path.join(LOCAL_DATA_PATH, 'raw', f"Hourly_ada_utc.csv")

    df.to_csv(the_path)

    return df

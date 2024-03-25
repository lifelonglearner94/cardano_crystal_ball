import pandas as pd
import requests
from cardano_crystal_ball.helper.file_system_helper import search_upwards
from cardano_crystal_ball.helper.file_system_helper import get_from_env


def get_fg_from_api(limit = "700"):
    url = "https://api.alternative.me/fng/"
    params = {"limit": limit, "date_format":"kr"}
    response = requests.get(url, params).json()
    df = pd.DataFrame(response.get('data'))
    df = df.drop(['time_until_update'],axis=1)
    df = df.sort_values('timestamp')
    df.to_csv (search_upwards('raw_data')/'raw_data/fg.csv')
    df.to_csv(search_upwards('raw_data')/('raw_data/' + get_from_env("NAME_FG_CSV")))

    return df


if __name__ == "__main__":
    get_fg_from_api()

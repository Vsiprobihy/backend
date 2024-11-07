import json

import numpy as np
import pandas as pd
from django.conf import settings


class DataLoader:
    """Class for loading data from JSON file."""

    @staticmethod
    def load_city_data():
        file_path = settings.BASE_DIR / 'event' / 'constants' / 'city_data.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            cleaned_data = pd.json_normalize(data).replace({np.nan: None}).to_dict(orient="records")
        return cleaned_data

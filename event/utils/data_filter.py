class DataFilter:
    """Class for filtering data by region and city."""

    @staticmethod
    def filter_by_region(data, region_query):
        if region_query:
            return [
                item for item in data
                if isinstance(item.get("Region"), str) and item.get("Region").lower().startswith(region_query.lower())
            ]
        return data

    @staticmethod
    def filter_by_city(data, city_query):
        if city_query:
            return [
                item for item in data
                if isinstance(item.get("City"), str) and item.get("City").lower().startswith(city_query.lower())
            ]
        return data

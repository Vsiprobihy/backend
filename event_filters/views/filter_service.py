import re


class EventFilterService:
    @staticmethod
    def filter_by_distance(events, distance_min, distance_max):
        filtered_events = []
        for event in events:
            for distance in event.distances.all():
                match = re.search(
                    r"(\d+)(\s?км|\s?km|\s?м|\s?m)", distance.name, re.IGNORECASE
                )
                if match:
                    distance_value = float(match.group(1))
                    unit = match.group(2).strip().lower()

                    if unit in ["м", "m"]:
                        distance_value /= 1000

                    if (distance_min is None or distance_value >= distance_min) and (
                        distance_max is None or distance_value <= distance_max
                    ):
                        filtered_events.append(event)
                        break
        return filtered_events

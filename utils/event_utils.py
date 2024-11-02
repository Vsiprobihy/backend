from event.constants.constants_event import REGIONS

def get_region_name(code):
    """Returns the name of the region by its code."""
    for region_code, region_name in REGIONS:
        if region_code == code:
            return region_name
    return code

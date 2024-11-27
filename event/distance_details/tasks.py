from datetime import date


def apply_cost_change_rules(distance):
    """
    Applies cost change rules for a given DistanceEvent instance.
    Updates the 'cost' field if a rule condition is met.
    """
    today = date.today()
    current_participants = 100  # Replace this with logic to get the current participant count

    applicable_rules = distance.cost_change_rules.all()

    # Apply rules based on participants and date
    for rule in applicable_rules:
        if rule.from_date and rule.from_date <= today:
            # Rule based on date
            distance.cost = rule.cost
        elif rule.from_participants and current_participants >= rule.from_participants:
            # Rule based on participants
            distance.cost = rule.cost

    distance.save()
    return distance.cost

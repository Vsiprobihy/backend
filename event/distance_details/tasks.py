from datetime import date


def apply_cost_change_rules(distance):
    """
    Applies cost change rules for a given DistanceEvent instance.
    Updates the 'cost' field if a rule condition is met.
    """
    today = date.today()
    current_participants = 100  # Replace this with logic to get the current participant count

    applicable_rules = distance.costChangeRules.all()

    # Apply rules based on participants and date
    for rule in applicable_rules:
        if rule.fromDate and rule.fromDate <= today:
            # Rule based on date
            distance.cost = rule.cost
        elif rule.fromParticipants and current_participants >= rule.fromParticipants:
            # Rule based on participants
            distance.cost = rule.cost

    distance.save()
    return distance.cost

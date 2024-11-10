import phonenumbers
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    # Check if a string contains only numbers and '+' symbols for the country code
    if not all(char.isdigit() or char == "+" for char in value):
        raise ValidationError(f"{value} should only contain digits and a '+' sign.")

    try:
        parsed_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError(f"{value} is not a valid phone number.")
    except phonenumbers.NumberParseException:
        raise ValidationError(f"{value} is not a valid phone number format.")

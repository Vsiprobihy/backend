from io import BytesIO

import phonenumbers
from django.core.exceptions import ValidationError
from PIL import Image


def validate_phone_number(value):
    # Check if a string contains only numbers and '+' symbols for the country code
    if not all(char.isdigit() or char == '+' for char in value):
        raise ValidationError(f"{value} should only contain digits and a '+' sign.")

    try:
        parsed_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError(f'{value} is not a valid phone number.')
    except phonenumbers.NumberParseException:
        raise ValidationError(f'{value} is not a valid phone number format.')


def validate_image_file(file):
    # Check the file extension
    allowed_extensions = ['jpg', 'jpeg', 'png']
    extension = file.name.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise ValidationError(f'Unsupported file type: {extension}. Allowed types: {", ".join(allowed_extensions)}')

    # Validate that the file is a valid image
    try:
        image = Image.open(file)
        if image.format not in ['PNG', 'JPEG', 'JPG']:
            raise ValidationError('Invalid file format. Only PNG, JPG, and JPEG are allowed.')
    except Exception:
        raise ValidationError('Uploaded file is not a valid image.')


def validate_file_size(file):
    # Restrict file size to a maximum of 5 MB
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size exceeds {max_size_mb}MB limit.')


def process_image(file, size=None):
    try:
        image = Image.open(file)

        # Convert RGBA to RGB to remove alpha channel
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Create a thumbnail of size
        if size:
            image.thumbnail(size)

        # Save the processed image into memory
        thumb_io = BytesIO()
        image.save(thumb_io, format='JPEG')
        thumb_io.seek(0)
        file.file = thumb_io  # Replace the original file with the processed one
    except Exception:
        raise ValidationError('Error processing image')

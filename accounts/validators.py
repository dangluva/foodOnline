import os.path
from django.core.exceptions import ValidationError


def allow_only_images_validator(value):
    extension = os.path.splitext(value.name)[1]  # in cover-image.jpg, jpg will be [1]
    print(extension)
    valid_extensions = ['.png', '.jpg', 'jpeg']
    if not extension.lower() in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension. Upload one of these extensions: {", ".join(valid_extensions)}')


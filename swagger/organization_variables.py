from drf_yasg import openapi


class Response:
    OrganizationResponse = openapi.Response(
        'Organization details response',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id', 'users', 'name', 'email'],
            properties={
                'id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Unique identifier for the organization'
                ),
                'users': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['user', 'role'],
                        properties={
                            'user': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='User email associated with the organization'
                            ),
                            'role': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Role of the user in the organization (e.g., owner)'
                            ),
                        }
                    ),
                    description='List of users associated with the organization and their roles'
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Name of the organization'
                ),
                'site_url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    nullable=True,
                    description='Website URL of the organization'
                ),
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    nullable=True,
                    description='Contact phone number of the organization'
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Contact email of the organization'
                ),
                'instagram_url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    nullable=True,
                    description='Instagram profile URL of the organization'
                ),
                'facebook_url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    nullable=True,
                    description='Facebook profile URL of the organization'
                ),
                'telegram_url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    nullable=True,
                    description='Telegram profile URL of the organization'
                ),
                'main_image': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='URL of the main image for the organization'
                ),
                'background_image': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='URL of the background image for the organization'
                ),
            }
        )
    )

    OrganizationsListResponse = openapi.Response(
        'List of organizations response',
        schema=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['id', 'users', 'name', 'email'],
                properties={
                    'id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='Unique identifier for the organization'
                    ),
                    'users': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            required=['user', 'role'],
                            properties={
                                'user': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_EMAIL,
                                    description='Email of the user associated with the organization'
                                ),
                                'role': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Role of the user in the organization (e.g., owner)'
                                ),
                            }
                        ),
                        description='List of users and their roles'
                    ),
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Name of the organization'
                    ),
                    'site_url': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        nullable=True,
                        description='Website URL of the organization'
                    ),
                    'phone_number': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        nullable=True,
                        description='Contact phone number of the organization'
                    ),
                    'email': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_EMAIL,
                        description='Contact email of the organization'
                    ),
                    'instagram_url': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        nullable=True,
                        description='Instagram profile URL of the organization'
                    ),
                    'facebook_url': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        nullable=True,
                        description='Facebook profile URL of the organization'
                    ),
                    'telegram_url': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        nullable=True,
                        description='Telegram profile URL of the organization'
                    ),
                    'main_image': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        nullable=True,
                        description='URL of the main image for the organization'
                    ),
                    'background_image': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        nullable=True,
                        description='URL of the background image for the organization'
                    ),
                }
            )
        )
    )

    ModeratorInviteResponse = openapi.Response(
        'Moderator invitation response',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'success': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Confirmation message of successful moderator invitation',
                    default='Moderator invited successfully'
                )
            },
            required=['success']
        )
    )


class Request:
    OrganizationRequestBody = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Name of the organization',
                default='My Organization',
            ),
            'site_url': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='Website URL of the organization',
                nullable=True,
                default='http://example.com',
            ),
            'phone_number': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Contact phone number of the organization',
                nullable=True,
                default='+1234567890',
            ),
            'email': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description='Contact email of the organization',
                default='contact@organization.com',
            ),
            'instagram_url': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='Instagram profile URL',
                nullable=True,
                default='http://instagram.com/myorganization',
            ),
            'facebook_url': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='Facebook profile URL',
                nullable=True,
                default='http://facebook.com/myorganization',
            ),
            'telegram_url': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='Telegram profile URL',
                nullable=True,
                default='http://t.me/myorganization',
            ),
            'main_image': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='URL of the main image for the organization',
                default='http://example.com/main_image.jpg',
            ),
            'background_image': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='URL of the background image for the organization',
                default='http://example.com/background_image.jpg',
            ),
        },
        required=['name', 'email', 'users'],
    )

    ModeratorInviteRequestBody = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='User email',
                default='user1@examople.com',
            ),
            'message': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='Message to user',
                nullable=True,
                default='Welcome to organization',
            ),
        },
        required=['name', 'email', 'users'],
    )

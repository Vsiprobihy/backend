from drf_yasg import openapi


class Responce:
    EventResponse = openapi.Response(
        'Event created successfully',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                'id', 'name', 'competitionType', 'dateFrom', 'dateTo',
                'place', 'placeRegion', 'organizer', 'distances'
            ],
            properties={
                'id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Event ID'
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Event name'
                ),
                'competitionType': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=['name'],
                        properties={
                            'name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Type of competition'
                            ),
                        },
                    ),
                ),
                'dateFrom': openapi.Schema(
                    type=openapi.FORMAT_DATE,
                    description='Event start date'
                ),
                'dateTo': openapi.Schema(
                    type=openapi.FORMAT_DATE,
                    description='Event end date'
                ),
                'place': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Event location'
                ),
                'placeRegion': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Region of the event'
                ),
                'photos': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    nullable=True,
                    description='Event photos URL'
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Short description of the event'
                ),
                'registrationLink': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Registration link for the event'
                ),
                'hideParticipants': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description='Hide participants flag'
                ),
                'schedulePdf': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    nullable=True,
                    description='Schedule PDF link'
                ),
                'coOrganizer': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Co-Organizer description'
                ),
                'organizer': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=['id', 'users', 'name', 'email'],
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='Organizer ID'
                        ),
                        'users': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                required=['user', 'role'],
                                properties={
                                    'user': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='User email'
                                    ),
                                    'role': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='User role'
                                    ),
                                },
                            ),
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Organizer name'
                        ),
                        'siteUrl': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Organizer website'
                        ),
                        'phoneNumber': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Organizer phone number'
                        ),
                        'email': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Organizer email'
                        ),
                        'instagramUrl': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Organizer Instagram URL'
                        ),
                        'facebookUrl': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Organizer Facebook URL'
                        ),
                        'telegramUrl': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Organizer Telegram URL'
                        ),
                    },
                ),
                'distances': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        required=[
                            'id', 'name', 'competitionType', 'category',
                            'startNumberFrom', 'startNumberTo',
                            'allowRegistration', 'length',
                            'promoOnlyRegistration', 'cost', 'isFree',
                            'showNameOnNumber', 'showStartNumber', 'event'
                        ],
                        properties={
                            'id': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Distance ID'
                            ),
                            'name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Distance name'
                            ),
                            'competitionType': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Type of competition'
                            ),
                            'category': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Category of participants'
                            ),
                            'allowRegistration': openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                description='Flag for registration availability'
                            ),
                            'length': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Distance length'
                            ),
                            'startNumberFrom': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Start number range (from)'
                            ),
                            'startNumberTo': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Start number range (to)'
                            ),
                            'ageFrom': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Minimum age'
                            ),
                            'ageTo': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Maximum age'
                            ),
                            'cost': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Cost of participation'
                            ),
                            'isFree': openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                description='Flag indicating free participation'
                            ),
                            'promoOnlyRegistration': openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                description='Promo-only registration flag'
                            ),
                            'showNameOnNumber': openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                description='Flag to show name on number'
                            ),
                            'showStartNumber': openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                description='Flag to show start number'
                            ),
                            'event': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Associated event ID'
                            ),
                            'additionalOptions': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    required=['id', 'itemType', 'price', 'distance'],
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description='Option ID'
                                        ),
                                        'itemType': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description='Type of additional item'
                                        ),
                                        'price': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description='Price of additional item'
                                        ),
                                        'distance': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description='Associated distance ID'
                                        ),
                                    },
                                ),
                            ),
                            'costChangeRules': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    required=['id', 'cost', 'fromDate'],
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description='Cost change rule ID'
                                        ),
                                        'cost': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description='Updated cost for the distance'
                                        ),
                                        'fromParticipants': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            nullable=True,
                                            description='Minimum number of participants to apply this rule'
                                        ),
                                        'fromDate': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            format=openapi.FORMAT_DATE,
                                            description='Start date for the cost change rule'
                                        ),
                                    },
                                ),
                                description='List of cost change rules for the distance'
                            ),
                            'ageCategories': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    required=['id', 'name', 'gender', 'ageFrom', 'ageTo'],
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description='Age category ID'
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description='Name of the age category'
                                        ),
                                        'gender': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description='Gender for the category (e.g., male, female)'
                                        ),
                                        'ageFrom': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description='Minimum age for this category'
                                        ),
                                        'ageTo': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description='Maximum age for this category'
                                        )
                                    }
                                ),
                                description='List of age categories for the distance'
                            ),
                            'promoCodes': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    required=['id', 'name', 'promoType', 'discountValue', 'isActive'],
                                    properties={
                                        'id': openapi.Schema(
                                            type=openapi.TYPE_INTEGER,
                                            description='Promo code ID'
                                        ),
                                        'name': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description='Name of the promo code'
                                        ),
                                        'promoType': openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description='Type of promo code (e.g., discount, free entry)'
                                        ),
                                        'discountValue': openapi.Schema(
                                            type=openapi.TYPE_NUMBER,
                                            description='Value of the discount'
                                        ),
                                        'isActive': openapi.Schema(
                                            type=openapi.TYPE_BOOLEAN,
                                            description='Whether the promo code is active'
                                        ),
                                        'isSingleUse': openapi.Schema(
                                            type=openapi.TYPE_BOOLEAN,
                                            description='Whether the promo code can only be used once'
                                        ),
                                    },
                                ),
                                description='List of promo codes for the distance'
                            ),
                        },
                    ),
                ),
                'extendedDescription': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Detailed description of the event'
                ),
            },
        ),
    )


class Request:
    EventRequestBody = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Name of the event',
                default='Winter Wonderland Run 2024',
            ),
            'competitionType': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Type of competition',
                            default='running',
                        )
                    },
                    required=['name']
                ),
                description='List of competition types',
            ),
            'dateFrom': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Event start date',
                default='2024-10-28',
            ),
            'dateTo': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Event end date',
                default='2024-10-28',
            ),
            'place': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Location of the event',
                default='Lviv',
            ),
            'placeRegion': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Location of the event',
                default='lviv_region',
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Event description',
                default='Embrace the winter spirit with our Winter Wonderland Run!',
            ),
            'registrationLink': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='Registration link',
                default='http://site.com/registration/winter-wonderland-run-2024',
            ),
            'hideParticipants': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description='Whether to hide participants',
                default=True,
            ),
            'coOrganizer': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Co-Organizer description'
            ),
            'organization_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the organizer',
                default=1,
            ),
            'distances': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id',
                                             default=1),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the distance',
                                               default='5km Snow Run'),
                        'competitionType': openapi.Schema(type=openapi.TYPE_STRING,
                                                           description='Type of competition',
                                                           default='running'),
                        'category': openapi.Schema(type=openapi.TYPE_STRING,
                                                   description='Category of participants', default='adults'),

                        'length': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                 description='Length of the distance in km', default=5.0),

                        'startNumberFrom': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                            description='Starting number', default=1),

                        'startNumberTo': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                          description='Ending number', default=300),

                        'showStartNumber': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                            description='Show start number', default=True),

                        'showNameOnNumber': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                              description='Show name on the number',
                                                              default=True),
                        'ageFrom': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum age',
                                                   default=16),
                        'ageTo': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum age',
                                                 default=60),
                        'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cost of the distance',
                                               default=55),
                        'isFree': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the distance free',
                                                  # noqa: E501
                                                  default=False),
                        'promoOnlyRegistration': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                  description='Promo-only registration',
                                                                  default=False),
                        'allowRegistration': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                             description='Allow registration', default=True),

                        'additionalOptions': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id',
                                                         default=1),
                                    'itemType': openapi.Schema(type=openapi.TYPE_STRING,
                                                                description='Type of additional option',
                                                                default='t_shirt'),
                                    'price': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                            description='Price of additional option',
                                                            default=250),
                                },
                                required=['itemType', 'price'],
                            ),
                            description='Additional options for the distance'
                        ),
                        'costChangeRules': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                required=['cost', 'fromDate'],
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='Cost change rule ID',
                                        default=1
                                    ),
                                    'cost': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Updated cost for the distance',
                                        default='100'
                                    ),
                                    'fromParticipants': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        nullable=True,
                                        description='Minimum number of participants to apply this rule'
                                    ),
                                    'fromDate': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATE,
                                        description='Start date for the cost change rule'
                                    ),
                                },
                            ),
                            description='List of cost change rules for the distance'
                        ),
                        'ageCategories': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                required=['name', 'gender', 'ageFrom', 'ageTo'],
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='Age category ID (optional during creation)',
                                        default=1
                                    ),
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Name of the age category',
                                        default='Young Adults'
                                    ),
                                    'gender': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Gender for the category (e.g., male, female)',
                                        default='M'
                                    ),
                                    'ageFrom': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='Minimum age for this category',
                                        default=16
                                    ),
                                    'ageTo': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='Maximum age for this category',
                                        default=25
                                    )
                                }
                            ),
                            description='List of age categories for the distance'
                        ),
                        'promoCodes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                required=['name', 'promoType', 'discountValue', 'isActive'],
                                properties={
                                    'id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='Age category ID (optional during creation)',
                                        default=1
                                    ),
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Name of the promo code',
                                        default='WINTER10'
                                    ),
                                    'promoType': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Type of promo code (e.g., discount, free entry)',
                                        default='percentage'
                                    ),
                                    'discountValue': openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        description='Value of the discount',
                                        default=10
                                    ),
                                    'isActive': openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description='Whether the promo code is active',
                                        default=True
                                    ),
                                    'isSingleUse': openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description='Whether the promo code can only be used once',
                                        default=False
                                    ),
                                }
                            ),
                            description='List of promo codes for the distance'
                        ),
                    },
                    required=[
                        'name', 'competitionType', 'category',
                        'startNumberFrom', 'startNumberTo',
                        'allowRegistration', 'length',
                        'promoOnlyRegistration', 'cost', 'isFree',
                        'showNameOnNumber', 'showStartNumber', 'event'
                    ],
                ),
                description='List of distances',
            ),
            'extendedDescription': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Extended description of the event',
                default='Experience the beauty of winter while getting fit!',
            ),
        },
        required=[
            'name',
            'competitionType',
            'dateFrom',
            'dateTo',
            'place',
            'placeRegion',
            'organization_id',
            'additional_items',
            'distances',
        ],
    )

    EventRequestBodyPost = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Name of the event',
                default='Winter Wonderland Run 2024',
            ),
            'competitionType': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='Id of competition',
                            default=1,
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Type of competition',
                            default='running',
                        )
                    },
                    required=['name']
                ),
                description='List of competition types',
            ),
            'dateFrom': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Event start date',
                default='2024-10-28',
            ),
            'dateTo': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                description='Event end date',
                default='2024-10-28',
            ),
            'place': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Location of the event',
                default='Lviv',
            ),
            'placeRegion': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Location of the event',
                default='lviv_region',
            ),
            'description': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Event description',
                default='Embrace the winter spirit with our Winter Wonderland Run!',
            ),
            'registrationLink': openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description='Registration link',
                default='http://site.com/registration/winter-wonderland-run-2024',
            ),
            'hideParticipants': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description='Whether to hide participants',
                default=True,
            ),
            'coOrganizer': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Co-Organizer description'
            ),
            'organization_id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='ID of the organizer',
                default=1,
            ),
            'distances': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the distance',
                                               default='5km Snow Run'),
                        'competitionType': openapi.Schema(type=openapi.TYPE_STRING,
                                                           description='Type of competition',
                                                           default='running'),
                        'category': openapi.Schema(type=openapi.TYPE_STRING,
                                                   description='Category of participants', default='adults'),

                        'length': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                 description='Length of the distance in km', default=5.0),

                        'startNumberFrom': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                            description='Starting number', default=1),

                        'startNumberTo': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                          description='Ending number', default=300),

                        'showStartNumber': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                            description='Show start number', default=True),

                        'showNameOnNumber': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                              description='Show name on the number',
                                                              default=True),
                        'ageFrom': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum age',
                                                   default=16),
                        'ageTo': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum age',
                                                 default=60),
                        'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cost of the distance',
                                               default=55),
                        'isFree': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the distance free',
                                                  # noqa: E501
                                                  default=False),
                        'promoOnlyRegistration': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                  description='Promo-only registration',
                                                                  default=False),
                        'allowRegistration': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                             description='Allow registration', default=True),

                        'additionalOptions': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'itemType': openapi.Schema(type=openapi.TYPE_STRING,
                                                                description='Type of additional option',
                                                                default='t_shirt'),
                                    'price': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                            description='Price of additional option',
                                                            default=250),
                                },
                                required=['itemType', 'price'],
                            ),
                            description='Additional options for the distance'
                        ),
                        'costChangeRules': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                required=['cost', 'fromDate'],
                                properties={
                                    'cost': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Updated cost for the distance',
                                        default='100'
                                    ),
                                    'fromParticipants': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        nullable=True,
                                        description='Minimum number of participants to apply this rule'
                                    ),
                                    'fromDate': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        format=openapi.FORMAT_DATE,
                                        description='Start date for the cost change rule'
                                    ),
                                },
                            ),
                            description='List of cost change rules for the distance'
                        ),
                        'ageCategories': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                required=['name', 'gender', 'ageFrom', 'ageTo'],
                                properties={
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Name of the age category',
                                        default='Young Adults'
                                    ),
                                    'gender': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Gender for the category (e.g., male, female)',
                                        default='M'
                                    ),
                                    'ageFrom': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='Minimum age for this category',
                                        default=16
                                    ),
                                    'ageTo': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='Maximum age for this category',
                                        default=25
                                    )
                                }
                            ),
                            description='List of age categories for the distance'
                        ),
                        'promoCodes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                required=['name', 'promoType', 'discountValue', 'isActive'],
                                properties={
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Name of the promo code',
                                        default='WINTER10'
                                    ),
                                    'promoType': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Type of promo code (e.g., discount, free entry)',
                                        default='percentage'
                                    ),
                                    'discountValue': openapi.Schema(
                                        type=openapi.TYPE_NUMBER,
                                        description='Value of the discount',
                                        default=10
                                    ),
                                    'isActive': openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description='Whether the promo code is active',
                                        default=True
                                    ),
                                    'isSingleUse': openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description='Whether the promo code can only be used once',
                                        default=False
                                    ),
                                }
                            ),
                            description='List of promo codes for the distance'
                        ),
                    },
                    required=[
                        'name', 'competitionType', 'category',
                        'startNumberFrom', 'startNumberTo',
                        'allowRegistration', 'length',
                        'promoOnlyRegistration', 'cost', 'isFree',
                        'showNameOnNumber', 'showStartNumber', 'event'
                    ],
                ),
                description='List of distances',
            ),
            'extendedDescription': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Extended description of the event',
                default='Experience the beauty of winter while getting fit!',
            ),
        },
        required=[
            'name',
            'competitionType',
            'dateFrom',
            'dateTo',
            'place',
            'placeRegion',
            'organization_id',
            'additional_items',
            'distances',
        ],
    )

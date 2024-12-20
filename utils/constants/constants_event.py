REGIONS = [
    ('vinnytsia_region', 'Vinnytsia oblast'),
    ('volyn_region', 'Volyn oblast'),
    ('dnipropetrovsk_region', 'Dnipropetrovsk oblast'),
    ('donetsk_region', 'Donetsk oblast'),
    ('zhytomyr_region', 'Zhytomyr oblast'),
    ('zakarpattia_region', 'Zakarpattia oblast'),
    ('zaporizhzhia_region', 'Zaporizhzhia oblast'),
    ('ivano-frankivsk_region', 'Ivano-Frankivsk oblast'),
    ('kyiv_region', 'Kyiv oblast'),
    ('kirovohrad_region', 'Kirovohrad oblast'),
    ('luhansk_region', 'Luhansk oblast'),
    ('lviv_region', 'Lviv oblast'),
    ('mykolaiv_region', 'Mykolaiv oblast'),
    ('odesa_region', 'Odesa oblast'),
    ('poltava_region', 'Poltava oblast'),
    ('rivne_region', 'Rivne oblast'),
    ('sumy_region', 'Sumy oblast'),
    ('ternopil_region', 'Ternopil oblast'),
    ('kharkiv_region', 'Kharkiv oblast'),
    ('kherson_region', 'Kherson oblast'),
    ('khmelnytskyi_region', 'Khmelnytskyi oblast'),
    ('cherkasy_region', 'Cherkasy oblast'),
    ('chernihiv_region', 'Chernihiv oblast'),
    ('chernivtsi_region', 'Chernivtsi oblast'),
]

COMPETITION_TYPES = [
    ('running', 'Running'),
    ('trail', 'Trail'),
    ('ultramarathon', 'Ultramarathon'),
    ('cycling', 'Cycling'),
    ('online', 'Online'),
    ('walking', 'Walking'),
    ('ocr', 'OCR'),
    ('swimming', 'Swimming'),
    ('triathlon', 'Triathlon'),
]

STATUS_PENDING = 'pending'
STATUS_UNPUBLISHED = 'unpublished'
STATUS_PUBLISHED = 'published'

STATUS_CHOICES = [
    (STATUS_PENDING, 'Pending'),
    (STATUS_UNPUBLISHED, 'Unpublished'),
    (STATUS_PUBLISHED, 'Published'),
]

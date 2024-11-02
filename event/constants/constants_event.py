REGIONS = [
    ('vinnytsia_region', 'Вінницька область'),
    ('volyn_region', 'Волинська область'),
    ('dnipropetrovsk_region', 'Дніпропетровська область'),
    ('donetsk_region', 'Донецька область'),
    ('zhytomyr_region', 'Житомирська область'),
    ('zakarpattia_region', 'Закарпатська область'),
    ('zaporizhzhia_region', 'Запорізька область'),
    ('ivano-frankivsk_region', 'Івано-Франківська область'),
    ('kyiv_region', 'Київська область'),
    ('kirovohrad_region', 'Кіровоградська область'),
    ('luhansk_region', 'Луганська область'),
    ('lviv_region', 'Львівська область'),
    ('mykolaiv_region', 'Миколаївська область'),
    ('odesa_region', 'Одеська область'),
    ('poltava_region', 'Полтавська область'),
    ('rivne_region', 'Рівненська область'),
    ('sumy_region', 'Сумська область'),
    ('ternopil_region', 'Тернопільська область'),
    ('kharkiv_region', 'Харківська область'),
    ('kherson_region', 'Херсонська область'),
    ('khmelnytskyi_region', 'Хмельницька область'),
    ('cherkasy_region', 'Черкаська область'),
    ('chernihiv_region', 'Чернігівська область'),
    ('chernivtsi_region', 'Чернівецька область'),
]

COMPETITION_TYPES = [
    ('running', 'Біг'),
    ('trail', 'Трейл'),
    ('ultramarathon', 'Ультрамарафон'),
    ('cycling', 'Велоспорт'),
    ('online', 'Online'),
    ('walking', 'Ходьба'),
    ('ocr', 'OCR'),
    ('swimming', 'Плавання'),
    ('triathlon', 'Тріатлон'),
]

STATUS_PENDING = 'pending'
STATUS_UNPUBLISHED = 'unpublished'
STATUS_PUBLISHED = 'published'

STATUS_CHOICES = [
    (STATUS_PENDING, 'Очікує затвердження'),
    (STATUS_UNPUBLISHED, 'Не опублікована'),
    (STATUS_PUBLISHED, 'Опублікована'),
]
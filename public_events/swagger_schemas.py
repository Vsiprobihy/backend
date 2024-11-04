from event.serializers.events import EventSerializer

class SwaggerDocs:

    class TakeEvent:
        get = {
        'tags' : ["Public Events"],
        "responses":{200: EventSerializer}
        }
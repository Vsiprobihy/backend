from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from event.models import Event
from event.serializers import EventSerializer
from django.db.models import Q
import re

class EventFilterView(APIView):
    def get(self, request):
        # Получаем параметры фильтрации из GET-запроса
        competition_type = request.GET.get('competition_type', None)
        name = request.GET.get('name', None)
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)
        place = request.GET.get('place', None)
        distance_min = request.GET.get('distance_min', None)
        distance_max = request.GET.get('distance_max', None)

        # Базовый QuerySet для объектов Event
        events = Event.objects.all()

        # Применяем фильтры
        if competition_type:
            events = events.filter(competition_type=competition_type)
        
        if name:
            events = events.filter(name__icontains=name)

        if month:
            events = events.filter(Q(date_from__month=month) | Q(date_to__month=month))

        if year:
            events = events.filter(Q(date_from__year=year) | Q(date_to__year=year))

        if place:
            events = events.filter(place__icontains=place)

        # Фильтрация по диапазону дистанций
        if distance_min and distance_max:
            try:
                # Попытка преобразовать в вещественные числа. 
                # Если значения невозможно преобразовать в числа 
                # (например, пользователь ввел нечисловые данные), произойдет ошибка.
                distance_min = float(distance_min)
                distance_max = float(distance_max)

                # Применяем фильтрацию по дистанциям
                events = events.filter(
                    distances__name__regex=rf'(\d+)(\s?км|\s?km)'
                ).distinct()

                filtered_events = []
                for event in events:
                    # Проверяем каждую дистанцию события
                    for distance in event.distances.all():
                        # Извлекаем число из строки
                        match = re.search(r'(\d+)', distance.name)
                        if match:
                            distance_value = float(match.group(1))
                            # Если дистанция попадает в диапазон
                            if distance_min <= distance_value <= distance_max:
                                filtered_events.append(event)
                                break  # Если хотя бы одна дистанция подходит, добавляем событие

                events = filtered_events

            except ValueError:
                return Response({"error": "Invalid distance range"}, status=status.HTTP_400_BAD_REQUEST)

        # Сериализация результатов
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

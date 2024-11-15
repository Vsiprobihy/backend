from rest_framework import pagination
from rest_framework.response import Response


class Pagination(pagination.PageNumberPagination):
    page_size = 12

    def get_paginated_response(self, data):
        return Response(
            {
                'pagination': {
                    'next_page': self.get_next_link(),
                    'current_page': self.page.number,
                    'previous_page': self.get_previous_link(),
                    'num_pages': self.page.paginator.num_pages,
                },
                'items_count': self.page.paginator.count,
                'items': data,
            }
        )

from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    A custom limit-offset based pagination.

    Overridden to customize the response format.
    Default limit (page size) is set to 10.
    Maximum limit (page size) is set to 100.
    """

    default_limit = 10
    max_limit = 100

    def get_total_pages(self, total, limit):
        """
        Method to calculate the total number of pages.
        """
        return (total + limit - 1) // limit

    def get_current_page(self, offset, limit):
        """
        Method to calculate the current page number.
        """
        return (offset // limit) + 1

    def get_paginated_response(self, data):
        """
        Overridden method to customize the pagination response.
        """
        total = self.count
        current_page = self.get_current_page(self.offset, self.limit)
        total_pages = self.get_total_pages(total, self.limit)

        previous_page = current_page - 1 if current_page > 1 else None
        next_page = current_page + 1 if current_page < total_pages else None

        return Response({
            'pagination': {
                'total_records': total,
                'total_pages': total_pages,
                'previous_page': previous_page,
                'next_page': next_page,
                'limit': self.limit
            },
            'results': data
        })

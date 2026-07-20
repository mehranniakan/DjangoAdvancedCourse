from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_object': self.page.paginator.count,
            'total_pages':self.page.paginator.num_pages,
            'current_page':self.page.number,
            'page_item_count': self.page_size,
            'results': data
        })
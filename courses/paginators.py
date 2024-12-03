from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10


class CustomOffsetPagination(LimitOffsetPagination):
    default_limit = 5

    # offset_query_param = 5
    # limit_query_param = 5

    max_limit = 20

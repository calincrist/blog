from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination
)

class PostLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 9
    default_limit = 4

class PostPageNumberPagination(PageNumberPagination):
    page_size = 9

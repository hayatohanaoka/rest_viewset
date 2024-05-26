from rest_framework.pagination import PageNumberPagination

class EquipmentPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 10

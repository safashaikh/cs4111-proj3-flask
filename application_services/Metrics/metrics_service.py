from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class MetricsResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_most_ordered_items(cls, count):
        res = d_service.get_most_ordered_items(count)
        return res

    @classmethod
    def get_most_popular_vendors(cls, count):
        res = d_service.get_most_popular_vendors(count)
        return res

    @classmethod
    def get_most_liked_items(cls, count):
        res = d_service.get_most_liked_items(count)
        return res
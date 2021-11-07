from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class VendorResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template("bs3363", "orders", template)
        return res


    @classmethod
    def add_by_template(cls, template):
        res = d_service.add_by_template("bs3363", "orders", template)
        return res


    @classmethod
    def update_by_template(cls, update_template, where_template):
        res = d_service.update_by_template("bs3363", "orders",
                                           update_template, where_template)
        return res


    @classmethod
    def delete_by_template(cls, template):
        res = d_service.delete_by_template("bs3363", "orders", template)
        return res
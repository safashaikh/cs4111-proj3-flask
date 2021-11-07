from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class ProductResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template("bs3363", "products", template)
        return res

    @classmethod
    def get_vendors(cls, pid):
        res = d_service.get_product_vendors(pid)
        return res

    @classmethod
    def add_by_template(cls, template):
        res = d_service.add_by_template("bs3363", "products", template)
        return res


    @classmethod
    def update_by_template(cls, update_template, where_template):
        res = d_service.update_by_template("bs3363", "products",
                                           update_template, where_template)
        return res


    @classmethod
    def delete_by_template(cls, template):
        res = d_service.delete_by_template("bs3363", "products", template)
        return res

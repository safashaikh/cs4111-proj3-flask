from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class VendorResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template("bs3363", "vendors", template)
        return res


    @classmethod
    def add_by_template(cls, template):
        res = d_service.add_by_template("bs3363", "vendors", template)
        return res


    @classmethod
    def update_by_template(cls, update_template, where_template):
        res = d_service.update_by_template("bs3363", "vendors",
                                           update_template, where_template)
        return res


    @classmethod
    def delete_by_template(cls, template):
        res = d_service.delete_by_template("bs3363", "vendors", template)
        return res


    @classmethod
    def get_products(cls, vid):
        res = d_service.get_vendor_products(vid)
        return res


    @classmethod
    def get_by_prefix(cls, prefix, column = 'name'):
        res = d_service.get_by_prefix("bs3363", "vendors", column, prefix)
        return res

from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class OrderResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template("bs3363", "orders", template)
        return res

    @classmethod
    def get_by_prefix(cls, prefix, column = 'card'):
        res = d_service.get_by_prefix("bs3363", "orders", column, prefix)
        return res

    @classmethod
    def get_orders(cls, count, oid):
        res = d_service.get_orders(count, oid)
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


    @classmethod
    def get_shipment(cls, oid):
        res = d_service.get_order_shipment(oid)
        return res


    @classmethod
    def get_address(cls, oid):
        res = d_service.get_order_address(oid)
        return res


    @classmethod
    def get_card(cls, oid):
        res = d_service.get_order_card(oid)
        return res

    @classmethod
    def get_items(cls, oid):
        res = d_service.get_order_items(oid)
        return res
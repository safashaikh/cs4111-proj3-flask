import os
from flask import Flask, Response, request, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import database_services.RDBService as db_service
from flask_cors import CORS
import json

import logging

import utils.rest_utils as rest_utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.UsersResource.user_service import UserResource
from application_services.ProductResource.product_service import ProductResource
from application_services.VendorResource.vendor_service import VendorResource
from application_services.OrdersResource.orders_service import OrderResource
from application_services.Metrics.metrics_service import MetricsResource


app = Flask(__name__)
CORS(app)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")


@app.route("/")
def index():
    """This will render our frontend application. This means that the index.html after the Angular build will need to be
    placed in the ./templates folder. All other contents of the build will be placed in the ./static folder.
    When building the angular app, make sure to run ng build --prod --build-optimizer --baseHref=”/static/ so that
    the references are handled correctly.
    """
    return render_template('index.html')  # Return index.html


@app.route("/login", methods=["GET"])
def login():
    """
    This is a very minimal login. Based on the query params, we just check in the username/pw combo is present in the
    DB and return either 200 or 403.
    """
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            username = request.args.get('username')
            password = request.args.get('password')
            authenticated = UserResource.auth(username, password)
            if authenticated:
                return Response("Logged in", status=200)
            else:
                return Response("Failed to authenticate", status=403)
        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/login', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/users', methods=["GET", "POST"])
def get_users():
    # customers
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = UserResource.get_by_template({})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "POST":
            data = input.data
            res = UserResource.add_by_template(data)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/users', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/users/<userID>', methods=["GET", "PUT", "DELETE"])
def get_users_by_userID(userID):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = UserResource.get_by_template({'cid': userID})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "PUT":
            data = input.data
            res = UserResource.update_by_template(data, {'cid': userID})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "DELETE":
            res = UserResource.delete_by_template({'cid': userID})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/users/<userID>', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/products', methods=["GET", "POST"])
def get_products():
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = ProductResource.get_by_template({})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
            print(rsp)

        elif input.method == "POST":
            data = input.data
            res = ProductResource.add_by_template(data)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/products', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/products/<pid>', methods=["GET", "PUT", "DELETE"])
def get_product_by_pid(pid):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = ProductResource.get_by_template({'pid': pid})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "PUT":
            data = input.data
            res = ProductResource.update_by_template(data, {'pid': pid})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "DELETE":
            res = ProductResource.delete_by_template({'pid': pid})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/products/<pid>', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/products/<pid>/vendors', methods=["GET"])
def get_product_vendors(pid):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = ProductResource.get_vendors(pid)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/products/<pid>/vendors', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/vendors', methods=["GET"])
def get_vendors():
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = VendorResource.get_by_template({})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
            print(rsp)

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/vendors', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/vendors/<vid>/products', methods=["GET"])
def get_vendor_products(vid):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = VendorResource.get_products(vid)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/vendors/<vid>/products', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/users/<cid>/orders', methods=["GET"])
def get_user_order(cid):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            count = request.args.get('count')
            if not count:
                count = 10
            res = UserResource.get_orders(cid, count)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/user/<cid>/orders', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/orders/<oid>/shipment', methods=["GET"])
def get_order_shipment(oid):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = OrderResource.get_shipment(oid)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/orders/<oid>/shipment', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/orders/<oid>/address', methods=["GET"])
def get_order_address(oid):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = OrderResource.get_address(oid)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/orders/<oid>/address', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/orders/<oid>/card', methods=["GET"])
def get_order_card(oid):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = OrderResource.get_card(oid)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/orders/<oid>/card', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/orders/<oid>/itemorders', methods=["GET"])
def get_order_items(oid):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = OrderResource.get_items(oid)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/orders/<oid>/items', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/metrics/most_purchased', methods=["GET"])
def get_most_purchases_items():
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            count = request.args.get('count')
            if not count:
                count = 10
            res = MetricsResource.get_most_ordered_items(count)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: 'metrics/most_purchased', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/metrics/popular_vendors', methods=["GET"])
def get_popular_vendors():
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            count = request.args.get('count')
            if not count:
                count = 10
            res = MetricsResource.get_most_popular_vendors(count)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/metrics/popular_vendors', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/metrics/most_liked', methods=["GET"])
def get_most_liked():
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            count = request.args.get('count')
            if not count:
                count = 10
            res = MetricsResource.get_most_liked_items(count)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/metrics/most_liked', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>', methods=["GET", "POST"])
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = db_service.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True) # debug=False sets the app to production mode for deployment
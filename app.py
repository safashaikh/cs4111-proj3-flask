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
from application_services.AddressResource.address_service import AddressResource
from application_services.ProductResource.product_service import ProductResource
from application_services.VendorResource.vendor_service import VendorResource



app = Flask(__name__)
CORS(app)

blueprint = make_google_blueprint(
    client_id=os.environ.get("OAUTH_ID", None),
    client_secret=os.environ.get("OAUTH_SECRET", None),
    scope=["profile", "email"],
    reprompt_consent=True
)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.register_blueprint(blueprint, url_prefix="/userlogin")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    print(resp.json())
    #TODO find person in db, if not, create user
    # then redirect to
    # return redirect("localhost:4200/customers/<id>")
    return resp.json()


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
            res = UserResource.get_orders(cid)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/user/<cid>/orders', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>', methods=["GET", "POST"])
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = db_service.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_db_connection():
    uri = os.environ.get("DBURI")
    engine = create_engine(uri)

    try:
        conn = engine.connect()
    except:
        raise RuntimeError("Cannot connect to database.")

    return conn

def _to_dict(keys, data):
    res = []
    for d in data:
        obj = {}
        for i, key in enumerate(keys):
            obj[key] = d[i]
        res.append(obj)
    
    return res


def get_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    #cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
          "LOWER( " + column_name + " )" + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + sql)

    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def _get_where_clause_args(template):

    terms = []
    
    clause = None

    if template is None or template == {}:
        clause = ""

    else:
        for k, v in template.items():
            terms.append(f'{k}={v}')

        clause = " where " + " AND ".join(terms)


    return clause


def find_by_template(db_schema, table_name, template):

    wc = _get_where_clause_args(template)

    conn = _get_db_connection()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def add_by_template(db_schema, table_name, template):
    columns = template.keys()
    columns_string = ', '.join(columns)

    values_string = []
    for v in template.values():
        if isinstance(v,int):
            values_string.append(v)
        else:
            values_string.append("'"+v+"'")

    values_string = ", ".join(values_string)

    conn = _get_db_connection()
    sql = f"insert into {db_schema}.{table_name} ({columns_string})" \
          f" values ({values_string});"
    res = conn.execute(sql)
    id = conn.insert_id()
    conn.commit()
    conn.close()

    return id


def update_by_template(db_schema, table_name, update_template, where_template):
    update_list = []
    for k, v in update_template.items():
        if isinstance(v, int):
            update_list.append(f"{k} = {v}")
        else:
            update_list.append(f"{k} = '{v}'")

    update_string = ', '.join(update_list)

    where_list = []
    for k, v in where_template.items():
        if isinstance(v, int):
            where_list.append(f"{k} = {v}")
        else:
            where_list.append(f"{k} = '{v}'")

    where_string = ', '.join(where_list)

    conn = _get_db_connection()
    sql = f"UPDATE {db_schema}.{table_name} SET {update_string} WHERE {where_string};"
    res = conn.execute(sql)
    conn.close()
    return update_template


def delete_by_template(db_schema, table_name, template):
    where_list = []
    for k, v in template.items():
        if isinstance(v, int):
            where_list.append(f"{k} = {v}")
        else:
            where_list.append(f"{k} = '{v}'")
    where_string = ' AND '.join(where_list)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql1 = f"DELETE FROM {db_schema}.{table_name} where {where_string};"
    cur.execute(sql1)
    res = cur.rowcount
    conn.commit()
    conn.close()
    return res


def get_product_vendors(pid):
    conn = _get_db_connection()
    print("GETTING PROD VENDORS")
    sql = f"SELECT v.vid, v.name, v.email, v.phone FROM Vendors v, Sells s WHERE s.vendor = v.vid AND s.product={pid}"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_vendor_products(vid):
    conn = _get_db_connection()
    print("GETTING VENDOR PRODUCTS")
    sql = f"SELECT p.pid, p.name, p.manufacturer FROM Products p, Sells s WHERE s.vendor = {vid} AND p.pid=s.product"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_user_orders(cid, count, like):
    conn = _get_db_connection()
    print("GETTING USER ORDERS")
    sql = f"WITH order_items AS (" \
            f"SELECT i.“order”, i.quantity, p.name, s.price, s.price * i.quantity AS item_total " \
            f"FROM itemorders i, sells s, products p " \
            f"WHERE i.product = s.product AND i.vendor=s.vendor AND i.product = p.pid) " \
          f"SELECT o.oid, o.odate, o.discount, o.tax, SUM(oi.item_total) AS subtotal, (1.0 + o.tax) * (SUM(oi.item_total)  * (1.0-o.discount)) AS total, " \
          f"o.card, s.shipper, s.tn, a.street_address, a.city, a.state, a.zip " \
          f"FROM Customers c, Orders o, order_items oi, shipments s, addresses a " \
          f"WHERE c.cid = {cid} AND o.customer=c.cid AND oi.“order” = o.oid AND o.oid = s.shiporder AND o.address = a.aid " \
          f"AND CAST( o.oid AS TEXT ) LIKE '{like}%' " \
          f"GROUP BY o.oid, o.odate, a.aid, s.tn " \
          f"ORDER BY o.odate DESC " \
          f"LIMIT {count}"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)

def get_orders(count, like):
    conn = _get_db_connection()
    print("GETTING ORDERS")
    sql = f"WITH order_items AS (" \
          f"SELECT i.“order”, i.quantity, p.name, s.price, s.price * i.quantity AS item_total " \
          f"FROM itemorders i, sells s, products p " \
          f"WHERE i.product = s.product AND i.vendor=s.vendor AND i.product = p.pid) " \
          f"SELECT o.oid, o.odate, o.discount, o.tax, SUM(oi.item_total) AS subtotal, (1.0 + o.tax) * (SUM(oi.item_total)  * (1.0-o.discount)) AS total, " \
          f"o.card, s.shipper, s.tn, a.street_address, a.city, a.state, a.zip, c.name as customer " \
          f"FROM Customers c, Orders o, order_items oi, shipments s, addresses a " \
          f"WHERE o.customer=c.cid AND oi.“order” = o.oid AND o.oid = s.shiporder AND o.address = a.aid " \
          f"AND CAST( o.oid AS TEXT ) LIKE '{like}%' " \
          f"GROUP BY o.oid, o.odate, s.tn, a.aid, c.name " \
          f"ORDER BY o.odate DESC " \
          f"LIMIT {count}"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_order_shipment(oid):
    conn = _get_db_connection()
    print("GETTING ORDER SHIPMENTS")
    sql = f"SELECT o.oid, s.tn, s.shipper " \
          f"FROM Orders o, Shipments s " \
          f"WHERE o.oid = {oid} AND o.oid=s.shiporder"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_order_card(oid):
    conn = _get_db_connection()
    print("GETTING ORDER SHIPMENTS")
    sql = f"SELECT o.oid, c.number, c.owner, c.expiration, c.cvv " \
          f"FROM Orders o, Cards c " \
          f"WHERE o.oid = {oid} AND o.card=c.number"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_order_address(oid):
    conn = _get_db_connection()
    print("GETTING ORDER ADDRESS")
    sql = f"SELECT o.oid, a.street_address, a.city, a.state, a.zip " \
          f"FROM Orders o, Addresses a " \
          f"WHERE o.oid = {oid} AND o.address=a.aid"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_order_items(oid):
    conn = _get_db_connection()
    print("GETTING ORDER ITEMS")
    sql = f"SELECT o.oid, i.quantity, i.product, i.vendor, p.name AS product_name, v.name AS vendor_name, s.price " \
          f"FROM orders o, itemorders i, products p, vendors v, sells s " \
          f"WHERE o.oid = {oid} AND o.oid = i.“order” AND i.product = p.pid AND i.vendor = v.vid " \
          f"AND s.product=p.pid AND s.vendor=v.vid"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_most_ordered_items(count):
    conn = _get_db_connection()
    print("GETTING MOST POPULAR ORDERS")
    sql = f"SELECT products.pid, name, SUM(itemorders.quantity) AS amount " \
          f"FROM products, itemorders " \
          f"WHERE products.pid = itemorders.product " \
          f"GROUP BY products.pid, products.name " \
          f"ORDER BY amount DESC " \
          f"LIMIT {count}"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_most_popular_vendors(count):
    conn = _get_db_connection()
    print("GETTING MOST POPULAR VENDORS")
    sql = f"SELECT v.vid, v.name, COUNT(v.name) AS num_purchases " \
          f"FROM Vendors v, Sells s, Itemorders i " \
          f"WHERE v.vid = s.vendor AND i.product = s.product AND i.vendor = s.vendor " \
          f"GROUP BY v.vid, v.name ORDER BY num_purchases DESC " \
          f"LIMIT {count}"

    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def get_most_liked_items(count):
    conn = _get_db_connection()
    print("GETTING MOST POPULAR ORDERS")
    sql = f"SELECT p.pid, p.name, COUNT(p.pid) AS amount " \
          f"FROM products p, cartadds c " \
          f"WHERE p.pid = c.product " \
          f"GROUP BY p.pid " \
          f"ORDER BY amount DESC " \
          f"LIMIT {count}"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)

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
        column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + sql)

    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)


def _get_where_clause_args(template):

    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k, v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " where " + " AND ".join(terms)


    return clause, args


def find_by_template(db_schema, table_name, template):

    wc, args = _get_where_clause_args(template)

    conn = _get_db_connection()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    cursor = conn.execute(text(sql), args=args)
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
    cur = conn.cursor()

    sql = f"insert into {db_schema}.{table_name} ({columns_string})" \
          f" values ({values_string});"
    res = cur.execute(sql)
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
    cur = conn.cursor()

    sql = f"UPDATE {db_schema}.{table_name} SET {update_string} WHERE {where_string};"
    res = cur.execute(sql)
    conn.commit()
    conn.close()
    return res


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
    # sql2 = "SELECT row_count() as no_of_rows_deleted;"
    cur.execute(sql1)
    # cur.execute(sql2)
    # res = cur.fetchone()
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


def get_user_orders(cid):
    conn = _get_db_connection()
    print("GETTING VENDOR PRODUCTS")
    sql = f"WITH order_items AS (" \
            f"SELECT i.“order”, i.quantity, p.name, s.price, s.price * i.quantity AS item_total " \
            f"FROM itemorders i, sells s, products p " \
            f"WHERE i.product = s.product AND i.vendor=s.vendor AND i.product = p.pid) " \
          f"SELECT o.oid, o.odate, o.discount, o.tax, SUM(oi.item_total) AS subtotal, (1.0 + o.tax) * (SUM(oi.item_total)  * (1.0-o.discount)) AS total " \
          f"FROM Customers c, Orders o, order_items oi " \
          f"WHERE c.cid = {cid} AND o.customer=c.cid AND oi.“order” = o.oid " \
          f"GROUP BY o.oid;"
    cursor = conn.execute(text(sql))
    res = cursor.fetchall()
    keys = cursor.keys()
    keys = list(keys)

    conn.close()

    return _to_dict(keys, res)
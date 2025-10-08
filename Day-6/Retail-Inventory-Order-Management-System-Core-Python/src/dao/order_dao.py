from src.dao.supabase_client import supabase

def create_order(order_data, items):
    # insert order
    res = supabase.table("orders").insert(order_data).execute()
    order = res.data[0] if res.data else None
    if not order:
        raise Exception("Failed to create order")
    order_id = order["order_id"]

    # insert items
    for item in items:
        payload = {
            "order_id": order_id,
            "prod_id": item["prod_id"],
            "quantity": item["quantity"],
            "price": item["price"]
        }
        supabase.table("order_items").insert(payload).execute()

    # return full order
    order_items = supabase.table("order_items").select("*").eq("order_id", order_id).execute().data
    order["items"] = order_items
    return order

def get_order_by_id(order_id):
    order_resp = supabase.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
    if not order_resp.data:
        return None
    order = order_resp.data[0]
    items = supabase.table("order_items").select("*").eq("order_id", order_id).execute().data
    order["items"] = items
    return order

def update_order(order_id, updates):
    supabase.table("orders").update(updates).eq("order_id", order_id).execute()
    return get_order_by_id(order_id)

def list_orders_by_customer(cust_id):
    orders = supabase.table("orders").select("*").eq("cust_id", cust_id).execute().data
    for o in orders:
        items = supabase.table("order_items").select("*").eq("order_id", o["order_id"]).execute().data
        o["items"] = items
    return orders

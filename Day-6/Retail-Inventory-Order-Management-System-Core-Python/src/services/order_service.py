from src.dao import order_dao, customer_dao, product_dao

class OrderError(Exception):
    pass

def create_order(customer_id, items):
    # check customer
    customer = customer_dao.get_customer_by_id(customer_id)
    if not customer:
        raise OrderError(f"Customer not found: {customer_id}")

    total_amount = 0
    enriched_items = []

    # check products and stock
    for i in items:
        prod = product_dao.get_product_by_id(i["prod_id"])
        if not prod:
            raise OrderError(f"Product not found: {i['prod_id']}")
        if i["quantity"] > prod.get("stock", 0):
            raise OrderError(f"Not enough stock for product: {i['prod_id']}")
        total_amount += i["quantity"] * float(prod["price"])
        enriched_items.append({"prod_id": i["prod_id"], "quantity": i["quantity"], "price": float(prod["price"])})

    # deduct stock
    for i in enriched_items:
        prod = product_dao.get_product_by_id(i["prod_id"])
        new_stock = prod["stock"] - i["quantity"]
        product_dao.create_product(prod["name"], prod["sku"], float(prod["price"]), new_stock, prod.get("category"))

    order_data = {"cust_id": customer_id, "total_amount": total_amount}
    return order_dao.create_order(order_data, enriched_items)

def get_order(order_id):
    return order_dao.get_order_by_id(order_id)

def list_orders_by_customer(customer_id):
    return order_dao.list_orders_by_customer(customer_id)

def cancel_order(order_id):
    order = get_order(order_id)
    if not order:
        raise OrderError("Order not found")
    if order["status"] != "PLACED":
        raise OrderError("Only PLACED orders can be cancelled")
    # restore stock
    for item in order["items"]:
        prod = product_dao.get_product_by_id(item["prod_id"])
        product_dao.create_product(prod["name"], prod["sku"], float(prod["price"]), prod["stock"] + item["quantity"], prod.get("category"))
    return order_dao.update_order(order_id, {"status": "CANCELLED"})

def complete_order(order_id):
    order = get_order(order_id)
    if not order:
        raise OrderError("Order not found")
    return order_dao.update_order(order_id, {"status": "COMPLETED"})

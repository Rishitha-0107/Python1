from src.dao import customer_dao

class CustomerError(Exception):
    pass

def add_customer(name, email, phone, city=None):
    return customer_dao.create_customer(name, email, phone, city)

def list_customers():
    return customer_dao.list_customers()

def get_customer(cust_id):
    return customer_dao.get_customer_by_id(cust_id)

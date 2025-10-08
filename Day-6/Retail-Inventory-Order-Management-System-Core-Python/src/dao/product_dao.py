from src.dao.supabase_client import supabase

def create_product(name, sku, price, stock=0, category=None):
    payload = {"name": name, "sku": sku, "price": price, "stock": stock}
    if category:
        payload["category"] = category
    supabase.table("products").insert(payload).execute()
    resp = supabase.table("products").select("*").eq("sku", sku).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_product_by_id(prod_id):
    resp = supabase.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def list_products(limit=100):
    resp = supabase.table("products").select("*").limit(limit).execute()
    return resp.data or []

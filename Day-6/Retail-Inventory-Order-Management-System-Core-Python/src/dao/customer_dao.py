from src.dao.supabase_client import supabase

def create_customer(name, email, phone, city=None):
    existing = supabase.table("customers").select("*").eq("email", email).execute()
    if existing.data:
        raise Exception("Email already exists")
    payload = {"name": name, "email": email, "phone": phone}
    if city:
        payload["city"] = city
    supabase.table("customers").insert(payload).execute()
    resp = supabase.table("customers").select("*").eq("email", email).limit(1).execute()
    return resp.data[0] if resp.data else None

def get_customer_by_id(cust_id):
    resp = supabase.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
    return resp.data[0] if resp.data else None

def list_customers(limit=100):
    resp = supabase.table("customers").select("*").limit(limit).execute()
    return resp.data or []

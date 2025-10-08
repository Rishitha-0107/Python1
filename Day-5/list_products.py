from supabase import create_client, Client
from dotenv import load_dotenv
import os
 
load_dotenv()
 
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(supabase_url, supabase_key)
 
def list_products():
    resp = sb.table("products").select("*").order("product_id", desc=False).execute()
    return resp.data
 
if __name__ == "__main__":
    products = list_products()
    if products:
        print("Products:")
        for p in products:
            print(f"{p['product_id']}: {p['name']} (SKU:{p['sku']}) — ₹{p['price']} — stock: {p['stock']}")
    else:
        print("No products found.")
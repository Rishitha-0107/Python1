
import os
from supabase import create_client, Client #pip install supabase
from dotenv import load_dotenv # pip install python-dotenv
 
load_dotenv()
 
supabase_url = os.getenv("SUPABASE_URL")
supabase_key= os.getenv("SUPABASE_KEY")
sb: Client = create_client(supabase_url, supabase_key)
 
def add_product(name, sku, price, stock):
    payload = {"name": name, "sku": sku, "price": price, "stock": stock}
    resp = sb.table("products").insert(payload).execute()
    return resp.data
 
if __name__ == "__main__":
    name = input("Enter product name: ").strip()
    sku = input("Enter SKU: ").strip()
    price = float(input("Enter price: ").strip())
    stock = int(input("Enter stock: ").strip())
 
    created = add_product(name, sku, price, stock)
    print("Inserted:", created)
 
 
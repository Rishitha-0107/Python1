from supabase import create_client, Client
from dotenv import load_dotenv
import os
 
load_dotenv()
 
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(supabase_url, supabase_key)
 
def update_stock(product_id, new_stock):
    resp = sb.table("products").update({"stock": new_stock}).eq("product_id", product_id).execute()
    return resp.data
 
if __name__ == "__main__":
    pid = int(input("Enter product_id to update: ").strip())
    new_stock = int(input("Enter new stock value: ").strip())
 
    updated = update_stock(pid, new_stock)
    if updated:
        print("Updated record:", updated)
    else:
        print("No record updated — check product_id.")

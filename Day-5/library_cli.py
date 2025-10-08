import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    print("Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
    sys.exit(1)
sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
def print_row(row: dict):
    print(" | ".join(f"{k}:{v}" for k, v in row.items()))
def add_member(name: str, email: str) -> Optional[dict]:
    payload = {"name": name, "email": email}
    resp = sb.table("members").insert(payload).execute()
    if not resp.data:
        print("Error adding member:", resp.error)
        return None
    return resp.data[0]
def get_member(member_id: int) -> Optional[dict]:
    resp = sb.table("members").select("*").eq("member_id", member_id).execute()
    return resp.data[0] if resp.data else None
def update_member_email(member_id: int, new_email: str) -> bool:
    resp = sb.table("members").update({"email": new_email}).eq("member_id", member_id).execute()
    if  not resp.data:
        print("Error updating:", resp.error)
        return False
    return len(resp.data) > 0
def delete_member(member_id: int):
    try:
        resp = sb.table("borrow_records").select("*").eq("member_id", member_id).execute()
        if resp.data and len(resp.data) > 0:
            print(" Cannot delete — member still has borrowed books.")
            return False
        del_resp = sb.table("members").delete().eq("member_id", member_id).execute()
        if not del_resp.data:
            print(" No member found with that ID.")
            return False
        else:
            print("Member deleted successfully:", del_resp.data)
            return True
    except Exception as e:
        print(" Error deleting member:", e)
        return False
def add_book(title, author, category, stock):
    payload = {
        "title": title,
        "author": author,
        "category": category,
        "stock": stock,
    }
    try:
        resp = sb.table("books").insert(payload).execute()
        return resp.data   # returns the inserted row(s)
    except Exception as e:
        print("Error inserting book:", e)
        return None
def list_books() -> List[dict]:
    resp = sb.table("books").select("*").order("book_id", desc=False).execute()
    return resp.data or []
def search_books(term: str) -> List[dict]:
    books = list_books()
    term_low = term.lower()
    return [b for b in books if term_low in (b.get("title","").lower() + b.get("author","").lower() + (b.get("category") or "").lower())]
def update_book_stock(book_id: int, new_stock: int) -> bool:
    resp = sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
    if not resp.data:
        print("Error updating stock:", resp.error)
        return False
    return len(resp.data) > 0
def delete_book(book_id: int):
    try:
        resp = sb.table("borrow_records").select("*").eq("book_id", book_id).execute()

        if resp.data and len(resp.data) > 0:
            print(" Cannot delete — book is currently borrowed.")
            return False
        del_resp = sb.table("books").delete().eq("book_id", book_id).execute()
        if not del_resp.data:
            print("No book found with that ID.")
            return False
        else:
            print("Book deleted successfully:", del_resp.data)
            return True
    except Exception as e:
        print(" Error deleting book:", e)
        return False
def borrow_book(member_id: int, book_id: int):
    try:
        book_resp = sb.table("books").select("stock").eq("book_id", book_id).execute()
        if not book_resp.data or book_resp.data[0]["stock"] <= 0:
            print("Book is out of stock.")
            return False
        borrow_resp = sb.table("borrow_records").insert({
            "member_id": member_id,
            "book_id": book_id
        }).execute()
        new_stock = book_resp.data[0]["stock"] - 1
        sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
        print(" Borrow recorded:", borrow_resp.data)
        return True
    except Exception as e:
        print(" Error borrowing book:", e)
        return False
from datetime import datetime
def return_book(record_id: int):
    try:
        rec_resp = sb.table("borrow_records").select("book_id, return_date").eq("record_id", record_id).execute()
        if not rec_resp.data:
            print(" No borrow record found with that id.")
            return False
        record = rec_resp.data[0]
        if record["return_date"] is not None:
            print(" Book already returned.")
            return False
        book_id = record["book_id"]
        sb.table("borrow_records").update({
            "return_date": datetime.now().isoformat()
        }).eq("record_id", record_id).execute()
        book_resp = sb.table("books").select("stock").eq("book_id", book_id).execute()
        if book_resp.data:
            new_stock = book_resp.data[0]["stock"] + 1
            sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
        print("Book returned successfully!")
        return True
    except Exception as e:
        print(" Error returning book:", e)
        return False
def report_overdue(days_overdue: int = 14) -> List[dict]:
    resp = sb.table("borrow_records").select("*").is_("return_date", None).execute()
    if  not resp.data:
        print("Error fetching borrow records:", resp.error)
        return []
    rows = resp.data or []
    overdue = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_overdue)
    for r in rows:
        bd = r.get("borrow_date")
        if not bd:
            continue
        try:
            bd_dt = datetime.fromisoformat(bd.replace("Z", "+00:00"))
        except Exception:
            continue
        if bd_dt < cutoff:
            # enrich with member/book details
            member = get_member(r.get("member_id")) or {}
            book_resp = sb.table("books").select("*").eq("book_id", r.get("book_id")).execute()
            book = (book_resp.data[0] if book_resp.data else {})
            r2 = r.copy()
            r2["member_name"] = member.get("name")
            r2["book_title"] = book.get("title")
            overdue.append(r2)
    return overdue
def report_most_borrowed(top_n: int = 5) -> List[Dict]:
    resp = sb.table("borrow_records").select("*").execute()
    if  not resp.data:
        print("Error fetching borrow_records:", resp.error)
        return []
    rows = resp.data or []
    counts = {}
    for r in rows:
        bid = r.get("book_id")
        counts[bid] = counts.get(bid, 0) + 1
    sorted_bids = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    result = []
    for bid, cnt in sorted_bids:
        book_resp = sb.table("books").select("*").eq("book_id", bid).execute()
        book = (book_resp.data[0] if book_resp.data else {"title": "(deleted)"})
        result.append({"book_id": bid, "title": book.get("title"), "borrow_count": cnt})
    return result
def show_member_with_borrows(member_id: int):
    try:
        member_resp = sb.table("members").select("*").eq("member_id", member_id).execute()
        if not member_resp.data:
            print(" Member not found")
            return
        member = member_resp.data[0]
        print("Member:", member)
        borrows_resp = (
            sb.table("borrow_records")
            .select("record_id, borrow_date, return_date, books(title, author)")
            .eq("member_id", member_id)
            .execute()
        )
        if not borrows_resp.data:
            print("This member has no borrowed books.")
            return
        print("Borrowed books:")
        for rec in borrows_resp.data:
            title = rec["books"]["title"]
            author = rec["books"]["author"]
            borrow_date = rec["borrow_date"]
            return_date = rec["return_date"] or "Not returned"
            print(f"- {title} by {author} | Borrowed: {borrow_date} | Returned: {return_date}")
    except Exception as e:
        print("Error fetching member borrows:", e)
def menu():
    print("\n--- Library CLI ---")
    print("1) Register Member")
    print("2) Add Book")
    print("3) List Books")
    print("4) Search Books")
    print("5) Update Book Stock")
    print("6) Update Member Email")
    print("7) Delete Member")
    print("8) Delete Book")
    print("9) Borrow Book")
    print("10) Return Book")
    print("11) Show Member & Borrows")
    print("12) Report: Overdue")
    print("13) Report: Most Borrowed")
    print("0) Exit")
def main_loop():
    while True:
        menu()
        choice = input("Enter choice: ").strip()
        if choice == "0":
            break
        if choice == "1":
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            m = add_member(name, email)
            print("Created member:", m)
        elif choice == "2":
            t = input("Title: ").strip()
            a = input("Author: ").strip()
            c = input("Category: ").strip()
            s = int(input("Stock (int): ").strip())
            b = add_book(t, a, c, s)
            print("Added book:", b)
        elif choice == "3":
            books = list_books()
            for b in books:
                print(f"{b['book_id']}: {b['title']} by {b['author']} | stock: {b['stock']} | category: {b.get('category')}")
        elif choice == "4":
            term = input("Search term (title/author/category): ").strip()
            results = search_books(term)
            for b in results:
                print(f"{b['book_id']}: {b['title']} by {b['author']} | stock: {b['stock']}")
        elif choice == "5":
            bid = int(input("Book id: ").strip())
            new_stock = int(input("New stock: ").strip())
            ok = update_book_stock(bid, new_stock)
            print("Updated." if ok else "Failed.")
        elif choice == "6":
            mid = int(input("Member id: ").strip())
            email = input("New email: ").strip()
            ok = update_member_email(mid, email)
            print("Updated." if ok else "Failed.")
        elif choice == "7":
            mid = int(input("Member id to delete: ").strip())
            ok = delete_member(mid)
            print("Deleted." if ok else "Failed.")
        elif choice == "8":
            bid = int(input("Book id to delete: ").strip())
            ok = delete_book(bid)
            print("Deleted." if ok else "Failed.")
        elif choice == "9":
            mid = int(input("Member id: ").strip())
            bid = int(input("Book id: ").strip())
            ok = borrow_book(mid, bid)
            print("Borrowed." if ok else "Failed.")
        elif choice == "10":
            rid = int(input("Borrow record id to return: ").strip())
            ok = return_book(rid)
            print("Returned." if ok else "Failed.")
        elif choice == "11":
            mid = int(input("Member id: ").strip())
            show_member_with_borrows(mid)
        elif choice == "12":
            days = int(input("Days overdue threshold (default 14): ").strip() or 14)
            rows = report_overdue(days)
            if not rows:
                print("No overdue records.")
            else:
                for r in rows:
                    print(f"{r['record_id']}: {r.get('book_title')} borrowed by {r.get('member_name')} on {r.get('borrow_date')}")
        elif choice == "13":
            topn = int(input("Top N (default 5): ").strip() or 5)
            rows = report_most_borrowed(topn)
            for r in rows:
                print(f"{r['book_id']}: {r['title']} — borrowed {r['borrow_count']} times")
        else:
            print("Unknown choice. Try again.")
if __name__ == "__main__":
    main_loop()
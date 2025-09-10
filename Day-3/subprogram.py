def applydis(p,dp):
    dp=p-(p *dp/100)
    return dp
def add_gst(p, gp=18):
    gp= p+(p*gp/100)
    return gp
def generate_invoice(cart,dp=0,gp=18):
    print("INVOICE ")
    st=0
    for product, price in cart.items():
        print(f"{product:<15}: ₹{price}")
        st+= price
    print("---------------------")
    print(f"Subtotal: ₹{st}")
    if dp> 0:
        dp=applydis(st, dp)
        print(f"After {dp}% discount: ₹{dp}")
    else:
        dp=st
    final_price = add_gst(dp, gp)
    print(f"After {gp}% GST: ₹{final_price:.2f}")
    print("---------------------")
    print("Thank you for shopping!")
def app():
    cart = []
    while True:
        print("\nE-commerce cart menu:")
        print("1. Add a product to the cart")
        print("2. Remove a product from the cart")
        print("3. Search for a product")
        print("4. Display all products")
        print("5. Show total number of products")
        print("6. Clear cart")
        print("7. Sort cart")
        print("8. Exit")
        c=int(input("Enter your choice: "))
        if c==1:
            p = input("Enter product name to add: ")
            cart.append(p)
            print(p, "added to cart")
        elif c==2:
            p = input("Enter product to remove: ")
            if p in cart:
                cart.remove(p)
                print(p, "removed from cart")
            else:
                print("Product not found")
        elif c==3:
            p = input("Enter product to be searched: ")
            if p in cart:
                print(p, "found in cart")
            else:
                print(p, "not found in cart")
        elif c==4:
            if cart:
                print("Products in cart:", cart)
            else:
                print("Cart is empty")
        elif c==5:
            print("Total number of products in cart:", len(cart))
        elif c==6:
            cart.clear()
            print("Cart cleared successfully.")
        elif c==7:
            if cart:
                cart.sort()
                print("Cart sorted:", cart)
            else:
                print("Cart is empty, cannot sort.")
        elif c==8:
            print("Exiting.")
            break
        else:
            print("Invalid choice")
app()

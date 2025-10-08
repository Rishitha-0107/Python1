import argparse
import json
from src.services import product_service
from src.dao import product_dao

# -------------------- Product Command Functions --------------------
def cmd_product_add(args):
    try:
        p = product_service.add_product(
            args.name, args.sku, args.price, args.stock, args.category
        )
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    ps = product_dao.list_products(limit=100)
    print(json.dumps(ps, indent=2, default=str))

# -------------------- CLI Parser --------------------
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # Product commands
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")

    # product add
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)

    # product list
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    return parser

# -------------------- Main --------------------
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__== "__main__":
    main()
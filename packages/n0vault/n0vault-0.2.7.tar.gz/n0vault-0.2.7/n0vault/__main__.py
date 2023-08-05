import sys
import argparse
import getpass

from n0vault import *

if __name__ == "__main__":
    sys.tracebacklimit = 0

    parser = argparse.ArgumentParser(prog = "n0vault")
    parser.add_argument("-v", "--vault",    nargs=1,        
        default=(
            VAULT_FILE:=
                (
                    VAULT_FILE_NAME
                    if (VAULT_FILE_NAME:=os.path.splitext(os.path.split(__file__)[1])[0]) not in ("__init__", "__main__")
                    else "default"
                )  + ".n0vault"
        ),
                                                          
                                                            metavar="VAULT_FILE",    action='store',       help=f"use VAULT_FILE as storage. By default: '{VAULT_FILE}'")
    parser.add_argument("-e", "--encrypt",                  default=None,            action='store_true',  help="save into ENCRYPTED vault file")
    parser.add_argument("-p", "--password", nargs=1,                                                       help="use PASSWORD")
    parser.add_argument("-d", "--decrypt",  dest="encrypt",                          action='store_false', help="save into DECRYPTED vault file")
    parser.add_argument("-u", "--update",   nargs="*",      metavar=("XPATH","VALUE"), action='append',    help=
        "add/update VALUE for the XPATH, if VALUE or both XPATH/VALUE are not defined, they should be entered manually without showing the VALUE")
    parser.add_argument("-f", "--forbid",                   default=False,           action='store_true',  help="forbid to show/decrypt storage by standard functionality")
    parser.add_argument("-r", "--remove",   nargs=1,        metavar="XPATH",         action='extend',      help="remove item with XPATH")
    parser.add_argument("-s", "--show",     nargs=1,        metavar="XPATH",         action='extend',      help="show value for the XPATH")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    
    args = parser.parse_args(sys.argv[1:])

    my_vault = n0Vault(vault_file_name = args.vault[0] if isinstance(args.vault, list) else args.vault if isinstance(args.vault, str) else None,
                       password = args.password[0] if isinstance(args.password, list) else None,
                       encrypted = args.encrypt
    )
    if my_vault.is_bit_set(2, 0b1):
        print(f"*** Saving/updating/showing of storage '{my_vault.vault_file_name}' is forbidden")
        sys.exit(-1)

    # ------------------------------------------------------
    # -u
    # ------------------------------------------------------
    for pair in args.update or []:
        if isinstance(pair, (list, tuple)):
            if (len_pair:=len(pair)) == 2:
                my_vault.update(pair[0],pair[1])
                continue
            elif len_pair == 1:
                key = pair[0]
            elif len_pair == 0:
                while True:
                    key = input("Enter value name:").strip()
                    if key:
                        break
                    print("*** Entered empty value name")
            else:
                raise Exception(f"Expected 0..2 items list. Received {len_pair} items list {pair}")
        else:
            raise Exception(f"Expected list of lists. Received: {args.update}")
            
        while True:
            value1 = getpass.getpass(f"Enter value assosiated with '{key}' (typed characters will not be shown):")
            if not value1:
                print("*** Entered empty value. Please repeat entering.")
            else:
                value2 = getpass.getpass(f"Re-enter value assosiated with '{key}' (typed characters will not be shown):")
                if value1 != value2:
                    print("*** Re-entered value is not equal to first typed. Repeat from the first step.")
                else:
                    break
        my_vault.update({key:value1})
        
    # ------------------------------------------------------
    # -r
    # ------------------------------------------------------
    for key in args.remove or []:
        if key in my_vault:
            my_vault.delete(key)
        else:
            print(f"Element with xpath '{key}' not exists, so it's not possible to remove.")
            
        if args.encrypt is None:
            args.encrypt = True
            my_vault._encrypted = True

    if args.show:
        if args.show[0][0] == "*":
            print(my_vault.show())
        else:
            for start_xpath in args.show or []:
                try:
                    start_xpath_value = my_vault._vault[start_xpath]
                    if isinstance(start_xpath_value, (int, float, str)):
                        print(f"\"{start_xpath}\" = \"{start_xpath_value}\"")
                    elif isinstance(start_xpath_value, (tuple, list, n0list, dict, n0dict)):
                        print(my_vault.show(start_xpath))
                except:
                    print(f"Element with xpath '{start_xpath}' not exists, so it's not possible to show.")
                
    if args.forbid:
        args.encrypt = True
        my_vault._encrypted = True
        
    if not args.encrypt is None:
        print(f"Saving '{my_vault.vault_file_name}' as %s%s..." % (["DECRYPTED", "ENCRYPTED"][int(my_vault._encrypted)], " (re-saving/updating/showing is forbidden)" if args.forbid else ""))
        my_vault.save(forbid_next_saving = args.forbid)

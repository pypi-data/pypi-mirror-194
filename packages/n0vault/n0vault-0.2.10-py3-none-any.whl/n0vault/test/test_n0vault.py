import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

import n0vault

def test_1():
    vault_file = os.path.splitext(os.path.split(__file__)[1])[0]+".vault"
    print("***** Opening/creating vault: " + vault_file)
    my_vault = n0vault.n0Vault()

    print("***** Set values in vault")
    my_vault["group/subgroup/key1"] = "value1"
    my_vault.update("group/subgroup/key2", "value2")
    my_vault.update({"group/subgroup/key3": "value3"})

    print("***** Get values from vault")
    print(f"{my_vault['group/subgroup/key1']=}")
    print(f"{my_vault.get('group/subgroup/key2')=}")
    print(f"{my_vault.get('group/subgroup/key3', 'Not exists')=}")
    print(f"{my_vault.get('group/subgroup/key4', 'Not exists')=}")

    print("***** Show values from vault")
    print(my_vault.show())
    
    # print("***** Save vault")
    # my_vault.save()

def main():
    test_1()

if __name__ == '__main__':
    main()

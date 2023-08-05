# n0vault
	Vault for secure storage of passwords and other sensitive data

## Usage from the command line:
	python -m n0vault [-h] [-v VAULT_FILE] [-e] [-p PASSWORD] [-d]
				   [-u [XPATH [VALUE ...]]] [-f] [-r XPATH] [-s XPATH]

	optional arguments:
	  -h, --help            show this help message and exit
	  -v VAULT_FILE, --vault VAULT_FILE
							use VAULT_FILE as storage. By default:
							'default.n0vault'
	  -e, --encrypt         save into ENCRYPTED vault file
	  -p PASSWORD, --password PASSWORD
							use PASSWORD
	  -d, --decrypt         save into DECRYPTED vault file
	  -u [XPATH [VALUE]], --update [XPATH [VALUE]]
							add/update VALUE for the XPATH, if VALUE or both
							XPATH/VALUE are not defined, they should be entered
							manually without showing the VALUE
	  -f, --forbid          forbid to show/decrypt storage by standard
							functionality
	  -r XPATH, --remove XPATH
							remove item with XPATH
	  -s XPATH, --show XPATH
							show value for the XPATH

## Sample of usage:
    python -m n0vault -d -v my_vault.file -u group/subgroup/key1 value1
    python -m n0vault -d -v my_vault.file -u group/subgroup/key2 value2
    python -m n0vault -d -v my_vault.file -u group/subgroup/key3 value3
    python -m n0vault -d -v my_vault.file -s group/subgroup/key1
    python -m n0vault -d -v my_vault.file -s group/subgroup/key2
    python -m n0vault -d -v my_vault.file -s group/subgroup/key3
    python -m n0vault -d -v my_vault.file -s *
    python -m n0vault -v my_vault.file -e
    python -m n0vault -v my_vault.file -d
    python -m n0vault -v my_vault.file -e -p Pa$$w0rD
    python -m n0vault -v my_vault.file -d -p Pa$$w0rD -s *

## Usage from the python code:
    import os
    import n0vault

    my_vault = n0vault.n0Vault(os.path.splitext(os.path.split(__file__)[1])[0]+".vault")

    my_vault["group/subgroup/key1"] = "value1"
    my_vault.update("group/subgroup/key2", "value2")
    my_vault.update({"group/subgroup/key3": "value3"})

    print(my_vault["group/subgroup/key1"])
    print(my_vault.get("group/subgroup/key2"))
    print(my_vault.get("group/subgroup/key3", "Not exists"))
    print(my_vault.get("group/subgroup/key4", "Not exists"))

    print(my_vault.show())

    my_vault.save()
	
## Result of the execution:
    value1
    value2
    value3
    Not exists
    {
        "__sign": "n0Vault1",
        "group": {
            "subgroup": {
                "key1": "value1",
                "key2": "value2",
                "key3": "value3"
            }
        }
    }

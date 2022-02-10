from Leakix import Leakix

leakix = Leakix("login", "password")
leakix.check_auth()
print(leakix.search_leaks("test"))
# Unofficial Leakix.net python library
*This project goes around the Internet and finds services to index them.*

### Usage:
```python
from Leakix import Leakix


leakix = Leakix("login", "password")
leakix.check_auth()
print(leakix.search_leaks("test"))
```
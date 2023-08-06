# CHARBYCHAR

Spice up your text by printing each individual letter instead of the entire string!

## Instructions 

1. Install: 

```
pip install charbychar
```
Alternatively, you can use:
```
py -m pip install charbychar
``` 

2. Write text:

```python
from charbychar import *

#use text using the default delay time (0.05s)
write_string("Hello, world!")

#write text using 1s delay time 
slow_write("Hello, world!")

#write text using 0.5 delay time
medium_write("Hello, world!")

#write text using 0.005 delay time
fast_write("Hello, world!")
```

3. Chew some gum. Coding is always better with gum. 
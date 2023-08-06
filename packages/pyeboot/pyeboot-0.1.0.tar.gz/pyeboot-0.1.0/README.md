# pyeboot
Python interface for pspdecrypt and sign_np.

## Installation
`pip install pyeboot`

## Usage
```
import pyeboot.decrypt
pyeboot.decrypt.run("EBOOT.BIN", "BOOT.BIN")

import pyeboot.sign
pyeboot.sign.run("BOOT.BIN", "EBOOT.BIN", "1")
```

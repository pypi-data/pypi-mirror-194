# rg15
rg15 is a library for interfacing with the [RG-15 sensor](https://store.hydreon.com/RG-15.html) via serial port. It is inspired by the following [library](https://github.com/waggle-sensor/plugin-raingauge).

## Installation

```bash
pip install rg15
```

## Exampe usage

Below is an example of basic usage:

```python
from rg15 import sensor

while True: 
    print(rg15.parse_values())
```

Output example:

```bash
Acc  0.00 mm, EventAcc  0.00 mm, TotalAcc  1.11 mm, RInt  0.00 mmph
```
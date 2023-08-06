# genpypress

This library contains several code generator helpers. It is connected to the `press` code generator.

## Usage

```python
from pathlib import Path
from genpypress import mapping

# import a file in markdown format
file = Path("TGT_ACCS_METH_RLTD_906_900_915_AMR_NIC_PCR_2_M2C.md", encoding="utf-8")
map = mapping.from_markdown(file.read_text(encoding="utf-8"))

# access table mapping property
print("Type of historization:", map.etl_historization)

# access a column mapping property (case insensitive)
print("hist_type =", map["hist_type"].transformation_rule)

# nonexisting column will - of course - blow the code up
try:
    print(map["not available"])
except KeyError as err:
    print(f"error: {err}")
```
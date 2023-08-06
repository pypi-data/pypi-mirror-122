### OCCSON

Store, manage and deploy configuration securely with Occson.

#### Installation

```
pip3 install occson
```

#### Example

```python
from occson.document import Document

document = Document("occson://0.1.0/.env", "<ACCESS_TOKEN>", "<PASSPHRASE>")
print(document.download())
print(document.upload("A=1\nB=2", True))
```

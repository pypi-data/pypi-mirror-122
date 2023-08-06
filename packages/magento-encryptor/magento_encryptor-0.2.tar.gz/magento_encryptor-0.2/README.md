Implement Magento logic to verify password.

### Installation:

```
pip install magento_encryptor
```

### Usage:

```python
import magento_encryptor
magento_hash = "c6aad9e058f6c4b06187c06d2b69bf506a786af030f81fb6d83778422a68205e:salt:1:2"
magento_encryptor.verify("mypassword", magento_hash)
```

# steamguardgenpy

**Steamguardgenpy** easily generate steam twofactor (onetime/TOTP) code.

```python
>>> from steamguardgenpy import gen_two_factor_code
>>> gen_two_factor_code('FG+4a7-86d7-4986322f7f6b')
'QQQJP'
```

Steamguardgenpy allows you to generate steam twofactor codes using your account shared secret.

## Installation

```console
python -m pip install steamguardgenpy 
```
# Kazakhstani Validators Package

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
![code size](<https://img.shields.io/github/languages/code-size/tlgtaa/py-kz-validators?color=green>)

**A collection of Python validators for various Kazakhstani identification numbers, such as the Individual Identification Number (IIN) and Taxpayer Identification Number (TIN)**

## Installation

```bash
pip install py-kz-validators
```

## Usage

Here are the available validators:

### 1. Individual Identification Number (IIN)

The IIN validator checks whether a given string represents a valid Kazakhstani Individual Identification Number.

```python
from kz.validators import IIN


if IIN.is_valid('791028302728'):
  print('IIN is valid')
else:
  print('IIN is not valid')

```

This code will output `IIN is valid` since the IIN `791028302728` is a valid Kazakhstani Individual Identification Number

## Contributing

Contributions are welcome! If you have any suggestions or issues, please open an issue or pull request on the [GitHub repository](https://github.com/tlgtaa/py-kz-validators).

**Local Installation for Contributors**

```bash
  make dev-deps
```

**After making any changes, don't forget to run flake8(`make lint`) and tests(`make test`).**

## License

This package is licensed under the [MIT License](https://opensource.org/license/mit/). See the LICENSE file for more information.

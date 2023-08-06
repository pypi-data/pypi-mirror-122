# Hijri Date Fetcher
[![made-with-python](https://img.shields.io/badge/Backend-Python-1F425F.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-Green.svg)](https://opensource.org/licenses/MIT)

A Python package to fetch current hijri date in Arabic

![hijri_date_fetcher_img](assets/hijri_date_fetcher_img.png)

### Package Link
PyPi Page: [pypi.org/project/hijri](https://pypi.org/project/hijri)

### Installation

```
pip install hijri
```

### Usage

```
from hijri import Hijri
h = Hijri()
h.fetch()

# Output is the literal day and date in Arabic: الأربعاء 4 ذو الحجة 1442 ﻫ
```

### Dependencies
You may download the following dependencies in order for the script to work

- For your terminal, you have to have both `wget` and `libxml2-utils`
- For python3, you have to install the following packages, `arabic_reshaper` and `python-bidi`

# scikit-cars: Image processing in Python

This package is a scikit-image fork.
See [https://github.com/scikit-image/scikit-image](https://github.com/scikit-image/scikit-image) for the original package.
This package add the following features to scikit-image:

- Use the SAD for channels distance in SLIC algorithm.
- Implement Chan-Sandberg-Vese segmentation (Chan-Vase for vector-valued images) with nu parameter.

**Warning** Even if the package is called scikit-cars, the python module name is still skimage.

## Installation

Use pip to install this package:

```
pip install scikit-cars
```

## Installation from source

Install dependencies using:

```
pip install -r requirements.txt
```

Then, install scikit-image using:

```
$ pip install .
```

If you plan to develop the package, you may run it directly from source:

```
$ pip install -e .  # Do this once to add package to Python path
```

Every time you modify Cython files, also run:

```
$ python setup.py build_ext -i  # Build binary extensions
```

## Scikit-image license (Modified BSD)

Copyright (C) 2011, the scikit-image team
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1.  Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
2.  Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
3.  Neither the name of skimage nor the names of its contributors may be
    used to endorse or promote products derived from this software without
    specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

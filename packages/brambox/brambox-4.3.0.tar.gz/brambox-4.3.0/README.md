<img src="https://gitlab.com/EAVISE/brambox/raw/master/docs/.static/logo-wide.png" alt="Logo" width="1000" />

_Basic Requisites for Algorithms on iMages toolBOX_

[![Version][version-badge]][release-url]
[![Python][python-badge]]()
[![Pandas][pandas-badge]]()
[![Wheel][wheel-badge]][wheel-url]
[![Pipeline][pipeline-badge]][pipeline-badge]
[![Coverage][coverage-badge]][coverage-url]

Brambox is a python toolbox that provides the necessary tools to convert image annotations, compute statistics and more.
Its main use is for object detection algorithms and datasets.


## Installing
```bash
# From wheel
pip install brambox

# From source
pip install git+https://gitlab.com/eavise/brambox
```
> This project is python 3.6 and higher so on some systems you might want to use 'pip3.6' instead of 'pip'


## Using
Once you installed brambox, you can import it in your own python program with:
```python
import brambox as bb
```
For tutorials and the API documentation [click here][doc-url].


## Contributing
See [the contribution guidelines](CONTRIBUTING.md)


## Main Contributors
Here is a list of people that made noteworthy contributions and helped to get this project where it stands today!

  - [Tanguy Ophoff](https://gitlab.com/0phoff) [![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D31LPHE)
  - [Maarten Vandersteegen](https://gitlab.com/maartenvds)


[version-badge]: https://img.shields.io/pypi/v/brambox.svg?label=version
[python-badge]: https://img.shields.io/badge/python-3.6%20%7C%203.10-9cf
[pandas-badge]: https://img.shields.io/badge/pandas-1.1%2B-e70488
[wheel-badge]: https://img.shields.io/pypi/wheel/brambox.svg
[pipeline-badge]: https://gitlab.com/EAVISE/brambox/badges/master/pipeline.svg
[coverage-badge]: https://img.shields.io/codecov/c/gitlab/eavise/brambox?token=EG18cFdzfX
[release-url]: https://gitlab.com/EAVISE/brambox/tags
[wheel-url]: https://pypi.org/project/brambox
[coverage-url]: https://codecov.io/gl/EAVISE/brambox
[doc-url]: https://eavise.gitlab.io/brambox

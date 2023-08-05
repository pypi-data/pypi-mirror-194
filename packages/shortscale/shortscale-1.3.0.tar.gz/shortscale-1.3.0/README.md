# shortscale

[![CI](https://github.com/jldec/shortscale-py/actions/workflows/CI.yaml/badge.svg)](https://github.com/jldec/shortscale-py/actions)

https://pypi.org/project/shortscale/

Python module to convert integers into English words.

This is the Python port of the shortscale function, originally written in [JavaScript](https://github.com/jldec/shortscale) and [Rust](https://github.com/jldec/shortscale-rs), documented [here](https://jldec.me/forays-from-node-to-rust). There is a also a [Go](https://github.com/jldec/shortscale-go) version.

The [short scale](https://en.wikipedia.org/wiki/Long_and_short_scales#Comparison), has different words for each power of 1000.

This implementation expresses positive and negative numbers from zero to thousands, millions, billions, trillions, quadrillions etc, up to 10**33 - 1.

### Function
```python
def shortscale(num: int) -> str
```

### Example
```python
import shortscale

# ==> four hundred and twenty billion nine hundred and ninety nine thousand and fifteen
print(shortscale.shortscale(420_000_999_015))
```

After installing this module, the function can also be called from the commnd line e.g.

```sh
$ shortscale 420_000_999_015
420,000,999,015 => four hundred and twenty billion nine hundred and ninety nine thousand and fifteen

$ shortscale 0xffffffff
4,294,967,295 => four billion two hundred and ninety four million nine hundred and sixty seven thousand two hundred and ninety five
```

### Benchmarks
```sh
$ pip install -e .

Python v3.11.2 $ python tests/bench_shortscale.py

     50000 calls,    5000000 bytes,     1264 ns/call
    100000 calls,   10000000 bytes,     1216 ns/call
    200000 calls,   20000000 bytes,     1216 ns/call

Python v3.10.9 $ python tests/bench_shortscale.py

     50000 calls,    5000000 bytes,     1811 ns/call
    100000 calls,   10000000 bytes,     1808 ns/call
    200000 calls,   20000000 bytes,     1809 ns/call
```

### Test
```sh
$ pip install pytest
$ pip install -e .
$ pytest
============================= test session starts ==============================
platform darwin -- Python 3.10.9, pytest-7.2.1, pluggy-1.0.0
rootdir: /Users/jldec/pub/shortscale-py
collected 1 item                                                               

tests/test_shortscale.py .                                               [100%]

============================== 1 passed in 0.00s ===============================
```

### Build
This assumes that access to pypi.org has been configured 

```sh
pip install build twine
python -m build
python -m twine upload dist/*
````


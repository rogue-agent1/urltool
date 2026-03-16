# urltool
URL parser, builder, encoder/decoder, and query param manipulator.

## Usage
```bash
python urltool.py parse "https://example.com/path?q=hello&page=2"
python urltool.py encode "hello world & more"
python urltool.py decode "hello%20world"
python urltool.py build --host example.com --path /api -q "key=val"
python urltool.py join "https://example.com/a/" "../b"
python urltool.py query "https://x.com?a=1&b=2" --get a
```
## Zero dependencies. Python 3.6+.

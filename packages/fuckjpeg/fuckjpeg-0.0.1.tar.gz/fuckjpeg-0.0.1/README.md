# fuckjpeg

## Development

Using [flit](https://flit.readthedocs.io/en/latest/) for this one, seems neat.

```
virtualenv venv
source venv/bin/activate
python3 -m pip install --upgrade pip flit
flit install --deps develop
flit build
```

## Testing

```
mypy fuckjpeg
pytest fuckjpeg
```
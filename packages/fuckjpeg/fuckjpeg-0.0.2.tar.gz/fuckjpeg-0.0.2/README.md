# fuckjpeg

Renames .jpeg files to .jpg because I hate that file extension.

## Usage

```
Usage: fuckjpeg [OPTIONS] PATH

  Renames files with .jpeg to .jpg because fuck that.

  You can supply a filename or a directory, and if it's a directory it'll do
  all the files.

Options:
  -o, --overwrite                 Ignore existing files and overwrite them.
  -r, --recursive                 Set this and supply a path, recursively
                                  apply the fun. Use with caution, obviously.
  -l, --log-level [debug|info|warn]
                                  Set logging level
  --help                          Show this message and exit.
```

## Version History

 - 0.0.1 - Original release.
 - 0.0.2 - Bumped version number after running black and updated readme.

## Development

Using [flit](https://flit.readthedocs.io/en/latest/) for packaging, seems neat.

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
pylint fuckjpeg
python3 -m fuckjpeg -n -r -o -l debug ~/Downloads
```
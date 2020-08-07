![header image](https://raw.githubusercontent.com/thisisreallyfrustrating/omniisan/master/readme-header.png)

# Omniisan

[Omniisan](https://omniisan.com/) is a quick-and-dirty clone of
[omnibuser](http://www.omnibuser.com/) which sadly shut down in July
2020.

Omniisan is built to use
[fanficfare](https://github.com/JimmXinu/FanFicFare) in the hope that
the lovely contributors to that project do all the real work in
keeping things up-to-date.

This tool has the following sites 'turned-on':

- Spacebattles
- Sufficientvelocity

## Quick Start

On Debian assuming python >= 3.7:
```bash
apt install -y redis python3 python3-pip python3-virtualenv python3-dev build-essential  # Install system dependencies
cp settings.cfg.example settings.cfg  # generate and edit config
make venv  # install python deps
make run  # run flask development server
make run-worker  # run worker
```
Open it in the browser at [http:/localhost:5000/](http://localhost:5000/).

## Contributing

Omniisan just calls fanficfare directly. My hope is that this
interface is less likely to change. Perhaps some nice person might
want to write an adapter to use the lib directly. This would also allow progress to be monitored and displayed directly.

Commits should be flake8 clean and formatted with black.

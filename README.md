# Omniisan

[Omniisan](https://omniisan.moe/) is a quick-and-dirty clone of
[omnibuser](http://www.omnibuser.com/) which sadly shut down in July
2020.

Omniisan is built to use
[fanficfare](https://github.com/JimmXinu/FanFicFare) in the hope that
the lovely contributors to that project do all the real work in
keeping things up-to-date.

This tool has the following sites 'turned-on':

    Spacebattles Sufficientvelocity

## Quick Start

On Debian assuming python >= 3.7:

Install system dependencies:

    apt install -y redis python3 python3-pip python3-virtualenv python3-dev build-essential

Edit the config:

    cd omniisan
    cp settings.cfg.example settings.cfg
    vi settings.cfg

Install python dependencies:

    make venv

Run the development server:

    make run

And separately spin up at least one worker:

    make run-worker

Open it in the browser at [http:/localhost:5000/](http://localhost:5000/).

## Decisions

Omniisan just calls fanficfare directly. My hope is that this
interface is less likely to change.

My hope is that someone writes an adaptor that allows for a nice
progress display. I looked into it and it looked like a medium amount
of work.

## Disclaimer

I am not a developer and never will be. I especially don't understand
frontend.

## Contributing

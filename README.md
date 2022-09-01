# shonenjumpplus

downloader for shonenjumpplus

## Installation

1. Install [Poetry](https://python-poetry.org/)

```
curl -sSL https://install.python-poetry.org | python -
```

2. Clone this repository

```
git clone https://github.com/ishioka0222/shonenjumpplus.git
```

3. Install dependencies

```
cd shonenjumpplus
poetry install --no-dev
```

## Usage

### `download` subcommand

download images

```
poetry run shonenjumpplus download https://shonenjumpplus.com/magazine/xxx --email your-email@example.com --password your-password
```

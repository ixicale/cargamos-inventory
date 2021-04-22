# cargamos-inventory

Python3 (Flask) — API Test cargamos

Resume: Make an API REST using Flask & Postgres to manage produc inventory and set stock in stores.

## Requirements

- libpq-dev
- python3-dev
- python3-venv
- postgresql
- postgresql-contrib
- Database "cargamos" (without tables, used on connection)

## Settings to run project

1. First clone git project

```sh
git clone https://github.com/ixicale/cargamos-inventory;

cd cargamos-inventory;

```

2. Create a virtualenv & activate

```sh
python3 -m venv .venv;
source .venv/bin/activate;
```

3. Install packages

```sh
pip install -r requirements.txt
```

## Run API

Init project.

```sh
flask run 
```

There we have the API root, its documentation will be displayed thanks to Swagger (powered by Flask Restful)

## RUN TEST

```sh
python -m unittest tests/test_base.py
python -m unittest --buffer
```

## API Request (resume)

### /product/

— GET: Display all products records

— POST: Add new item

### /product/{sku}

— GET: Retuns first item by SKU

— PATCH: Update record

— DEL: Delete record

### /product/{sku}/tiendas/

— GET: Shows a list of all stores with stock

### /stock/

— POST: Add new product to store

### /store/

— GET: Display all store records

— POST: Add new store

### /store/{id}

— GET: Retuns first item by ID

— PATCH: Update record

— DEL: Delete record

### /store/{id}/stock

— GET: List store stocks

— POST: Add new product on store

### /store/{id}/stock/insufficient

— GET: Returns the list of insufficient product stocks list by store

### /store/{id}/stock/{sku}

— PATCH: Update stock by store ID and SKU

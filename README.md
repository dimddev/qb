## A Quick Base Interview

### 1. Impementation details
According to implementation details the script must be capable to fetch data from one endpoint (producer) and to create or update the second endpoint (consumer). In between a data mapping between both API's must be done as well.

The project was chosen to be called `qb`, from **Quick Base**

The current `qb` implementation is done with `Python 3.7.4` and `asyncio`. So before start please ensure this python version ( the easiest way to do it is `pyenv`).

`Qb` is a command line tool. Could be executed with a detailed command line arguments describing the both endpoints ( producer/consumer) or could use a data file, that can contain a millions of pair records. The `qb` could be configured as spider to work in `One to One`, `One To Many` or `Many to Many` relations between producer and consumer endpoints.

### 2. Installation

1. Create a `virtualenv` to keep your site-packages clean.

```
$ pyenv virtualenv .qb374
```
If you are using `pyenv` the above command will create a new `virtualenv` with **Python 3.7.4**.

As usual first we clone the project:

Next we are going to activate our new `virtualenv` and proceed ahead

```
$ pyenv activate .qb374
(.qb374) $
```

So let's clone the project and install all dependencies:

```
(.qb374) $ git clone https://github.com/dimddev/qb
(.qb374) $ cd qb
```
For this demo purpose we installing all dependencies, including the dev's one.

```
(.qb374) $ pip install -e '.[develop]'
```

All dependencies could be found in `setup.py`.

### 3. Testing

The `qb` use `pytest` and `pytest-asyncio` for testing engines since it it's async nature.

```
(.qb374) $ pytest
```

with a coverage:

```
(.qb374) $ pytest --cov=qbapi tests/
```

### 4. Usage

```
(.qb374) $ python qb.py --help
```

Use command line args to produce one pipeline with one producer and one consumer:

```
(.qb374) $ python qb.py --from_cred=PRODUCER_API_CRED --from_map=name --from_map=location --from_map=email --to_cred=CONSUMER_API_CRED --to_map=name --to_map=address --to_map=email
```

The above command will use FROM_API as producer and TO_API as consumer. The mapping bettween both is done by the `--from_map` and `--to_map` options.

For more complex tasks we could use the data file. The one could be found in `qbapi/config/config.json`.

```python
data = {
  "from_api": [
    [
      "https://api.github.com/user",  # API endpoint
      "supersecretpassword:X",        # API credentials
      "token",                        # API auth type
      ["name", "email", "location"]   # Keys of interest / mapping
    ]
  ],
  "to_api": [
    [
      "https://targolini.freshdesk.com/api/v2/contacts", # API endpoint
      "supersecretpassword:X",                           # API credentials
      "basic",                                           # API auth type
      ["name", "email", "address"]                       # Keys of interest / maping
    ]
  ]
}
```

The keys of interest represent the mapping between both API fields. In this particular case the product from `from_api ` map `  ["name", "email", "location"]` and `to_api` map ` ["name", "email", "address"]` will produce an request with: ` ["name", "email", "address"]` or will map all values from the first one to secund with  changed kyes.

### 5. TODO

1. More tests.
2. Use of `uvloop` as event loop
3. Events communication between workers
4. Optimized `num_workers`
5. Profiling and optimization.

### 6. License
BSD 3

### 7. Author

Dimitar Dimitrov


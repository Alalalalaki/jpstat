# jpstat

A python package for accessing the official statistics of Japan.

## Features

- [estat api](estat-API)
- ...

## Install

```sh
pip install jpstat
```

## estat API

### Functions

All functions return one or multiple pandas DataFrames.

To see a list of statistics offered by estat api

```python
import jpstat
stat = jpstat.estat.get_stat()
```

To search data by either the code of a statistic or some key words

```python
data = jpstat.estat.get_list(statsCode="00400001")
data = jpstat.estat.get_list(searchWord="企業")
```

To dowload data

```python
data, note = jpstat.estat.statsDataId(statsCode="0000040001")
```

### Configuration

You can pass the estat api key to each function. Or you can set a configuration

```python
jpstat.options["estat.api_key"] = "MY_API_KEY"
```

To see a list of valid configuration options

```python
jpstat.config.describe_options()
```

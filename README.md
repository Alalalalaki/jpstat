# jpstat

A python package for accessing the official statistics of Japan.

## Features

- [estat api](#estat-api)
- [estat file](#estat-file)

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

You can also set the language from Japanese (default: J) to English

```python
jpstat.options["estat.lang"] = "E"
```

To see a list of valid configuration options

```python
jpstat.config.describe_options()
```

## estat File

Many statistics and datasets in estat can not be accessed through API, but are excel, csv, or pdf files and can be downloaded.

### Functions

To see a list of all statistics in estat that have downloadable files

```python
data = jpstat.estatFile.get_stat()
```

It will take some time to scraping the website of estat at the first time and then save the list to `options["estat.data_dir"]`. From then on, the function would first try to read the local file. You can force to scrape again by setting `update=True`.

To search data files by code of a statistic and the survey year (optional)

```python
data = jpstat.estatFile.get_list(statsCode="00400001")
data = jpstat.estatFile.get_list(statsCode="00400001", year="1950")
```

Use the information of data id and file type ("EXCEL"/"CSV"/"PDF") in `estatFile.get_list` to download the file

```python
data = jpstat.estatFile.get_file(statsDataId="000029094935", file_type="EXCEL")
```

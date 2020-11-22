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

[estat](https://www.e-stat.go.jp/) is the official site for government statistics in Japan. Its api service offers data of over 250+ statistics in Japan. You need to register an api key to access to the statistics.

### Functions

All functions return one or multiple pandas DataFrames.

To see a list of statistics offered by estat api

```python
import jpstat
stat = jpstat.estat.get_stat(key=YOUR_API_KEY)
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

You can also set the language from Japanese (default, "J") to English

```python
jpstat.options["estat.lang"] = "E"
```

To see a list of valid configuration options

```python
jpstat.config.describe_options()
```

## estat File

Many statistics and datasets in estat can not be accessed through API, but are excel, csv, or pdf files and can be downloaded. Here jpstat provides the functions that scrapes the information of statistics and download the files. Api key for estat is not needed, and the result is in Japanese only.

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

Again, you can save the result by setting `save=True`, and from next time jpstat would first check if the result already exists.

To download the file by using the information of data id and file type ("EXCEL"/"CSV"/"PDF") gotten from the result of `estatFile.get_list`

```python
jpstat.estatFile.get_file(statsDataId="000029094935", file_type="EXCEL")
```

The file would be downloaded to current folder by default.

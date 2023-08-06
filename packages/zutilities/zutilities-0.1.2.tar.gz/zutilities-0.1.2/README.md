# zutilities
A collection of Python utilities



## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Prerequisites
You'll need to have Python installed in order to use `zutilities`. Start by downloading and installing [Python](https://www.python.org/downloads/).
> *Note: Python 3 is recommended, however `zutilities` will probably work just fine with most verions of Python 2*


## Installation
```
python -m pip install zutilities
```

## Usage

`zutilities`.**jprint**(list_or_dict, indent=2)

Prints a list or dictionary as formatted JSON.

```
>>> zutilities.jprint([{'key1':'value1','key2':'value2'}])
[
  {
    "key1": "value1",
    "key2": "value2"
  }
]
```


`zutilities`.**read_json_file**(json_file)

Reads a JSON file from the filesystem and returns a list or dictionary.

```
>>> j = zutilities.read_json_file('file.json')
>>> j
[{'key1': 'value1', 'key2': 'value2'}]
```


`zutilities`.**get_logger**(log_level=20, format=default_log_format, streams=[sys.stdout])

Returns a _logging.RootLogger_ object with preferred defaults set. The _default_log_format_ is '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'

```
>>> logr = zutilities.get_logger()
>>> logr.info('Hello World')
[2021-10-08 21:08:40,353] {<stdin>:1} INFO - Hello world
```



## License

This project is licensed under the MIT License

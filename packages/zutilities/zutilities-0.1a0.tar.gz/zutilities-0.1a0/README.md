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

`zutilities.`**jprint**(list_or_dict, indent=2)

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


`zutilities.`**read_json_file**(json_file)

Reads a JSON file from the filesystem and returns a list or dictionary.

```
j = zutilities.read_json_file('file.json')
>>> j
[{'key1': 'value1', 'key2': 'value2'}]
```



## License

This project is licensed under the MIT License

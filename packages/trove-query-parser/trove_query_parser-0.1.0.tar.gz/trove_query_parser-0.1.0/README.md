# Trove query parser
> Convert a query from the Trove web interface into a set of parameters that can be used with the Trove API.


## Installation

`pip install trove_query_parser`

## How to use

* Construct a search in the Trove 'Newspapers and Gazettes' category.
* Copy the search url.
* Feed the url to the `parse_query` function.

```python
from trove_query_parser.parser import parse_query

parse_query('https://trove.nla.gov.au/search/category/newspapers?keyword=wragge&l-artType=newspapers&l-state=Queensland&l-category=Article&l-illustrationType=Cartoon')
```




    {'q': 'wragge',
     'zone': 'newspaper',
     'l-state': ['Queensland'],
     'l-category': ['Article'],
     'l-illustrated': 'true',
     'l-illtype': ['Cartoon']}



See the [documentation](https://wragge.github.io/trove_query_parser/) for a more detailed example.

## Limitations

Currently this only works with the 'Newspapers & Gazettes' category. Other categories may be added in time.

----

Created by [Tim Sherratt](https://timsherratt.org) ([@wragge](https://twitter.com/wragge)) for the [GLAM Workbench](https://glam-workbench.net/).

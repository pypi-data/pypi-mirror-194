# Inverted-Index-Keyword-Search

Inverted-Index-Keyword-Search is python library for searching up keywords or sub words in a corpus of data using inverted index lookup

## Installation

Use the package manager pip to install.

```bash
pip install Inverted-Index-Keyword-Search==0.1
```

## Usage

```python
import keyword_search

# returns dictionary of look up success
key_search(document,keyword_lst, n_grams_min ='default',n_grams_max='default',partial_match= False):

Usage:
doc = 'lets all search for full stack engineers and try to give him our best'
keywords = ['full stack engineers', 'engineers']

print(key_search(doc,keywords,partial_match=False))
>> {'full stack engineers': [(20, 40)]}

# returns n gram of a document for custom look up
make_ngram(document, n_grams_min,n_grams_max,)
Usage:
for start,end,value in make_ngram(document,n_grams_min,n_grams_max):

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Github

[Affan](https://github.com/Affanmir/KeywordSearch)
# freqit
Better frequency and crosstab tables.

This is a work in progress meant to provide better functionality and more options in constructing frequency tables for data analysis. Currently one-way tables are supported, crosstabulation tables to come in the future.

The package takes a pandas series and outputs a frequency table for the values within the column. 

Freqit requires that pandas and numpy are installed in the operating environment.

Installation:<br>
`pip install freqit`

Use:
```python
from freqit.oneway import freqtable
import pandas as pd

iris = pd.read_csv('https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/d546eaee765268bf2f487608c537c05e22e4b221/iris.csv')

freqtable(iris['species'])
```

Returns:
| value  | count | percentage | cum_total | cum_percentage | 
| ---------- | ----- | ---------- | --------- | -------------- | 
| setosa     | 50    | 33.333333  | 50        | 33.333333      |
| versicolor | 50    | 33.333333  | 100       | 66.666667      |
| virginica  | 50    | 33.333333  | 150       | 100.000000     |
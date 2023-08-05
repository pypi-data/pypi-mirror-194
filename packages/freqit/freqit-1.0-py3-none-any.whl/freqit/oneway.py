import pandas as pd


def freqtable(series, sort='value', asc=True):
    """One-way frequency table.

    Parameters
    ----------
    series : pandas series
        A column from a DataFrame to compute the frequency table on
    sort : str, optional
        The column the frequency table should be sorted on -
        value (series data), count (frequency count of values), or pct
        (percentage of values).
        default = value
    asc : bool, optional
        Flag indicating if sort should be ascending (default is
        True)

    Returns
    -------
    table : dataframe
        A frequency table
    """

    # summing
    table = pd.concat([series.value_counts(dropna=False).rename('count'),
                       series.value_counts(normalize=True).mul(100).rename('percentage')],
                      axis=1)
    table = table.reset_index() \
                 .rename(columns={'index': 'value'})

    # sorting
    if sort in ['value', 'count', 'pct', 'percentage', 'percent']:
        if sort in ['pct', 'percent']:
            sort = 'percentage'

        if sort == 'value':
            table = table.loc[pd.to_numeric(table.value, errors='coerce')
                                .sort_values(na_position='first',
                                             ascending=asc)
                                .index]
        else:
            table = table.sort_values(by=[sort],
                                      ascending=asc)
    else:
        print('Invalid sort!')

    # cumulating
    totn = table['count'].sum()

    table = pd.concat([table,
                       table['count'].cumsum().rename('cum_total'),
                       table['count'].cumsum().div(totn).mul(100).rename('cum_percentage')],
                      axis=1).reset_index(drop=True)

    return table

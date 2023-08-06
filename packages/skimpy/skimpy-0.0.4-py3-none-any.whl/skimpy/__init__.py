"""skimpy provides summary statistics about variables in pandas data frames."""
from collections import defaultdict
from itertools import chain

import numpy as np
import pandas as pd
import rich
from numpy.random import Generator
from numpy.random import PCG64
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typeguard import typechecked

console = Console()
QUANTILES = [0, 0.25, 0.75, 1]
HIST_BINS = 6
UNICODE_HIST = {
    0: " ",
    1 / 8: "▁",
    1 / 4: "▂",
    3 / 8: "▃",
    1 / 2: "▄",
    5 / 8: "▅",
    3 / 4: "▆",
    7 / 8: "▇",
    1: "█",
}


@typechecked
def infer_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    """Infers the, and applies new, datatypes of dataframe columns.

    :param df: input dataframe of ambiguous col type
    :type df: pd.DataFrame
    :return: dataframe with column datatypes set to best of knowledge
    :rtype: pd.DataFrame
    """
    df_types = (
        pd.DataFrame(df.apply(pd.api.types.infer_dtype, axis=0))
        .reset_index()
        .rename(columns={"index": "column", 0: "type"})
    )
    loop_types = df_types.values.tolist()
    for col in loop_types:
        if col[1] == "mixed":
            pass
        else:
            if col[1] == "decimal":
                data_type = "float64"
            elif col[1] == "string":
                data_type = "string"
            elif col[1] == "integer":
                data_type = "int"
            elif col[1] == "floating":
                data_type = "float64"
            elif col[1] == "date":
                data_type = "datetime64"
            elif col[1] == "categorical":
                data_type = "category"
            elif col[1] == "boolean":
                data_type = "bool"
            else:
                data_type = col[1]
            df[col[0]] = df[col[0]].astype(data_type)
    return df


@typechecked
def round_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Rounds dataframe to 2 s.f.

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Dataframe with numbers rounded to 2 s.f.
    """
    for col in df.select_dtypes("number"):
        df[col] = df[col].apply(lambda x: float(f'{float(f"{x:.2g}"):g}'))
    return df


@typechecked
def dataframe_to_rich_table(
    table_name: str,
    df: pd.DataFrame,
    number: str = "cyan",
    category: str = "magenta",
    datetime: str = "red",
    string: str = "green",
    bool: str = "turquoise2",
    object: str = "medium_purple1",
) -> rich.table.Table:
    """Converts a dataframe into a rich table.

    To pretty print a dataframe to the console or interactive console, it needs
    to first be converted into a rich table. This function performs that
    conversion and also colours entries in tables depending on their broad
    datatype. This function processes summaries (themselves dataframes) and is
    used to produce a table for each data type in the dataframe to be skimmed.
    A list of standard colours may be found at
    https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors

    Args:
        table_name (str): Usually one of 'number', 'bool', etc. Used as title.
        df (pd.DataFrame): summary of all data of one datatype
        number (str): colour to render numbers in
        category (str): colour to render categories in
        datetime (str): colour to render datetimes in
        string (str): colour to render strings in
        bool (str): colour to render bools in
        object (str): colour to render objects in

    Returns:
        rich.table.Table: instance of Table from the rich package
    """
    str_limit: int = 20  # For longer strings, limit chars shown.
    df = df.reset_index().rename(columns={"index": ""})
    table = Table(show_footer=False, expand=True, title=table_name, show_header=True)
    # generate dict of types to colours
    datatype_colours = {
        "number": number,
        "category": category,
        "datetime": datetime,
        "string": string,
        "bool": bool,
        "object": object,
    }
    cols_to_cat_map = dict(
        zip(
            datatype_colours.keys(),
            [
                list(df.select_dtypes(entry).columns)
                for entry in datatype_colours.keys()
            ],
        )
    )
    type_by_col_default = defaultdict(list)
    for k, seq in cols_to_cat_map.items():
        for letter in seq:
            type_by_col_default[letter].append(k)
    type_by_col = dict(
        zip(type_by_col_default.keys(), [x[0] for x in type_by_col_default.values()])
    )
    type_to_colour = dict(
        zip(type_by_col.keys(), [datatype_colours[x] for x in type_by_col.values()])
    )
    columns = list(df.columns)
    col_pos_to_colour = dict(
        zip(range(len(columns)), [type_to_colour[x] for x in columns])
    )
    rows = df.values
    # find any datetimes
    if ("first" or "last") in df.columns:
        timestamp_positions = [
            [
                [idx, i]
                for i, j in enumerate(item)
                if type(j) == pd._libs.tslibs.timestamps.Timestamp
            ]
            for idx, item in enumerate(rows)
        ]
        timestamp_pos_list = list(chain.from_iterable(timestamp_positions))
        timestamp_pos_tuples = [tuple(entry) for entry in timestamp_pos_list]
        for entry in timestamp_pos_tuples:
            hour, min, sec = rows[entry].hour, rows[entry].minute, rows[entry].second
            if hour == min == sec == 0:
                rows[entry] = rows[entry].strftime("%Y-%m-%d")
    for col in columns:
        table.add_column(str(col), overflow="fold")
    for row in rows:
        row = [
            Text(str(item)[:str_limit], style=col_pos_to_colour[i])
            for i, item in enumerate(row)
        ]
        table.add_row(*list(row))
    return table


def find_nearest(array, value):
    """Find the nearest numerical match to value in an array.

    Args:
        array (np.ndarray): An array of numbers to match with.
        value (float): Single value to find an entry in array that is close.

    Returns:
        np.array: The entry in array that is closest to value.
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


@typechecked
def create_unicode_hist(series: pd.Series) -> pd.Series:
    """Return a histogram rendered in block unicode.

    Given a pandas series of numerical values, returns a series with one
    entry, the original series name, and a histogram made up of unicode
    characters.

    Args:
        series (pd.Series): Numeric column of data frame for analysis

    Returns:
        pd.Series: Index of series name and entry with unicode histogram as
        a string, eg '▃▅█'
    """
    if series.dtype == "bool":
        series = series.astype("int")
    hist, _ = np.histogram(series, density=True, bins=HIST_BINS)
    hist = hist / hist.max()
    # now do value counts
    key_vector = np.array(list(UNICODE_HIST.keys()), dtype="float")
    ucode_to_print = "".join(
        [UNICODE_HIST[find_nearest(key_vector, val)] for val in hist]
    )
    return pd.Series(index=[series.name], data=ucode_to_print, dtype="string")


@typechecked
def numeric_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have numeric type.

    Args:
        xf (pd.DataFrame): Dataframe with columns of only numeric types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "mean": xf.mean(),
        "sd": xf.std(),
    }
    display_quantiles_as_pct = 100
    quantiles_dict = dict(
        zip(
            ["p" + str(int(x * display_quantiles_as_pct)) for x in QUANTILES],
            [xf.quantile(x) for x in QUANTILES],
        )
    )
    data_dict.update(quantiles_dict)
    # Create histogram using unicode block elements
    # https://en.wikipedia.org/wiki/Block_Elements
    hist_series = pd.concat(
        [create_unicode_hist(xf[col].dropna()) for col in xf.columns], axis=0
    )
    data_dict.update({"hist": hist_series})
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def category_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have category type.

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only category types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "ordered": pd.Series(
            dict(zip(xf.columns, [xf[col].cat.ordered for col in xf.columns]))
        ),
        "unique": pd.Series(
            dict(zip(xf.columns, [len(xf[col].unique()) for col in xf.columns]))
        ),
    }
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def bool_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have boolean type.

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only category types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    data_dict = {
        "true": xf.sum(),
        "true rate": xf.sum() / xf.shape[0],
    }
    hist_series = pd.concat(
        [create_unicode_hist(xf[col].dropna()) for col in xf.columns], axis=0
    )
    data_dict.update({"hist": hist_series})
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def string_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have string type. (NB not object type).

    Args:
        xf (pd.DataFrame):  Dataframe with columns of only string types

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "words per row": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [
                        xf[xf.columns[0]].str.count(" ").add(1).sum() / len(xf)
                        for col in xf.columns
                    ],
                )
            )
        ),
        "total words": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [
                        xf[xf.columns[0]].str.count(" ").add(1).sum()
                        for col in xf.columns
                    ],
                )
            )
        ),
    }
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def datetime_variable_summary_table(xf: pd.DataFrame) -> pd.DataFrame:
    """Summarise dataframe columns that have datetime type.

    Args:
        xf (pd.DataFrame): A dataframe with only datetime columns

    Returns:
        pd.DataFrame: A dataframe of summary statistics, with a number of rows
        determined by number of columns of xf
    """
    count_nans_vec = xf.isna().sum()
    data_dict = {
        "missing": count_nans_vec,
        "complete rate": 1 - count_nans_vec / xf.shape[0],
        "first": pd.Series(
            dict(
                zip(
                    xf.columns,
                    [xf[col].min() for col in xf.columns],
                )
            )
        ),
        "last": pd.Series(dict(zip(xf.columns, [xf[col].max() for col in xf.columns]))),
    }
    if len(xf) > 3:
        data_dict.update(
            {
                "frequency": pd.Series(
                    dict(
                        zip(xf.columns, [pd.infer_freq(xf[col]) for col in xf.columns])
                    )
                )
            }
        )
    summary_df = pd.DataFrame(data_dict)
    return summary_df


@typechecked
def skim(
    df: pd.DataFrame, header_style: str = "bold cyan", **colour_kwargs: str
) -> None:
    """Skim a data frame and return statistics.

    skim is an alternative to pandas.DataFrame.summary(), quickly providing
    an overview of a data frame. It produces a different set of summary
    functions based on the types of columns in the dataframe. You may get
    better results from ensuring that you set the datatypes in your dataframe
    you want before running skim.
    The colour_kwargs (str) are defined in dataframe_to_rich_table.

    Args:
        df (pd.DataFrame): Dataframe to skim
        header_style (str): A style to use for headers. See Rich API Styles.
        colour_kwargs (dict[str]): colour keyword arguments for rich table
    """
    if hasattr(df, "name") and "name" not in df.columns:
        name = df.name
    else:
        name = "dataframe"

    # Perform inference of datatypes
    # df = infer_datatypes(df)

    # Data summary
    tab_1_data = {"Number of rows": df.shape[0], "Number of columns": df.shape[1]}
    dat_sum_table = Table(
        title="Data Summary", show_header=True, header_style=header_style
    )
    dat_sum_table.add_column(name)
    dat_sum_table.add_column("Values")
    for key, val in tab_1_data.items():
        dat_sum_table.add_row(key, str(val))
    # Data tpes
    types_sum_table = Table(
        title="Data Types", show_header=True, header_style=header_style
    )
    tab_2_data = df.dtypes.astype(str).value_counts().to_dict()
    types_sum_table.add_column("Column Type")
    types_sum_table.add_column("Count")
    for key, val in tab_2_data.items():
        types_sum_table.add_row(key, str(val))
    # Categorys
    if "category" in df.dtypes.astype(str).to_list():
        xf = pd.DataFrame(df.dtypes.astype(str))
        cat_sum_table = Table(
            title="Categories", show_header=True, header_style=header_style
        )
        header_string = f"[{header_style}]Categorical Variables[/{header_style}]"
        cat_sum_table.add_column(header_string)
        cat_names = list(xf[xf[0] == "category"].index)
        for cat in cat_names:
            cat_sum_table.add_row(cat)
    # Summaries of cols of specific types
    types_funcs_dict = {
        "number": numeric_variable_summary_table,
        "category": category_variable_summary_table,
        "datetime": datetime_variable_summary_table,
        "string": string_variable_summary_table,
        "bool": bool_variable_summary_table,
    }
    list_of_tabs = []
    for col_type, summary_func in types_funcs_dict.items():
        xf = df.select_dtypes(col_type)
        if not xf.empty:
            sum_df = summary_func(xf)
            list_of_tabs.append(
                dataframe_to_rich_table(
                    col_type, round_dataframe(sum_df), **colour_kwargs
                )
            )
    # Put all of the info together
    grid = Table.grid(expand=True)
    tables_list = [dat_sum_table, types_sum_table]
    if "category" in df.dtypes.astype(str).to_list():
        tables_list.append(cat_sum_table)
    grid.add_row(Columns(tables_list))
    grid.add_column(justify="left")
    for sum_tab in list_of_tabs:
        grid.add_row(sum_tab)
    # Weirdly, iteration over list of tabs misses last entry
    grid.add_row(list_of_tabs[-1])
    console.print(Panel(grid, title="skimpy summary", subtitle="End"))


@typechecked
def generate_test_data() -> pd.DataFrame:
    """Generate dataframe with several different datatypes.

    For testing skimpy, it's convenient to have a dataset with many different
    data types. This function creates that dataframe.

    Returns:
        pd.DataFrame: dataframe with columns spanning several data types.
    """
    seed = 34729
    rng = Generator(PCG64(seed))
    len_df = 1000
    df = pd.DataFrame()
    df["length"] = rng.beta(0.5, 0.5, size=len_df)
    df["width"] = rng.gamma(1, 2, size=len_df)
    df["depth"] = rng.poisson(10, size=len_df)
    df["rnd"] = rng.normal(size=len_df, scale=1, loc=0)
    nan_places = rng.choice(range(len_df), size=125)
    df.loc[nan_places, "rnd"] = np.nan
    df["class"] = rng.choice(["setosa", "virtginica"], size=len_df)
    df["class"] = df["class"].astype("category")
    second_cat_var_entries = ["UK", "Mexico", "USA", "India"]
    prob = [0.6, 0.2, 0.1, 0.1]
    df["location"] = rng.choice(second_cat_var_entries, len_df, p=prob)
    df["location"] = df["location"].astype("category")
    df.loc[3, "location"] = np.nan
    df["booly_col"] = rng.choice([True, False], size=len_df)
    df["booly_col"] = df["booly_col"].astype(bool)
    # string column
    string_options = [
        "How are you?",
        "What weather!",
        "Indeed, it was the most outrageously pompous cat I have ever seen.",
    ]
    df["text"] = rng.choice(string_options, len_df)
    df.loc[[3, 5, 8, 9, 14, 22], "text"] = None
    df["text"] = df["text"].astype("string")
    # add a datetime column
    df["date"] = pd.date_range("2018-01-01", periods=len_df, freq="M")
    df["date_no_freq"] = rng.choice(
        (pd.to_datetime(pd.Series(["01/01/2022", "03/04/2023", "01/05/1992"]))), len_df
    )
    df.loc[[3, 12, 0], "date_no_freq"] = pd.NaT
    return df

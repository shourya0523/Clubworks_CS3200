'''source:
https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/'''

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st


def filter_dataframe(df: pd.DataFrame, buttonkey, **kwargs) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe
        buttonkey (str): Unique key for the checkbox widget.
        **kwargs: Optional keyword arguments.
                  'exclude' (list): A list of column names to exclude from the filter options.

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters", key=buttonkey)


    if not modify:
        return df

    df_filtered = df.copy() # Work on a copy for filtering

    # Get the list of columns to potentially filter on
    all_columns = df_filtered.columns.tolist()

    # Exclude specified columns from the list available for filtering
    columns_to_exclude = kwargs.get('exclude', [])
    available_columns_for_filter = [col for col in all_columns if col not in columns_to_exclude]

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in available_columns_for_filter: # Only process columns available for filtering
        if is_object_dtype(df_filtered[col]):
            try:
                df_filtered[col] = pd.to_datetime(df_filtered[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df_filtered[col]):
            df_filtered[col] = df_filtered[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        # Offer only the available columns for filtering
        to_filter_columns = st.multiselect("Filter dataframe on", available_columns_for_filter)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df_filtered[column]) or df_filtered[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df_filtered[column].unique(),
                    default=list(df_filtered[column].unique()),
                )
                df_filtered = df_filtered[df_filtered[column].isin(user_cat_input)]
            elif is_numeric_dtype(df_filtered[column]):
                _min = float(df_filtered[column].min())
                _max = float(df_filtered[column].max())
                step = (_max - _min) / 100 if (_max - _min) > 0 else 0.1 # Avoid division by zero
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df_filtered = df_filtered[df_filtered[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df_filtered[column]):
                # Ensure min/max are valid Timestamps before passing to date_input
                min_date = pd.Timestamp(df_filtered[column].min()).to_pydatetime()
                max_date = pd.Timestamp(df_filtered[column].max()).to_pydatetime()

                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        min_date,
                        max_date,
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    # Ensure comparison is timezone-naive
                    df_filtered = df_filtered.loc[df_filtered[column].between(start_date, end_date)]
            # Handle object/string type columns (potential fallback)
            elif is_object_dtype(df_filtered[column]):
                 user_text_input = right.text_input(
                        f"Substring or regex in {column}",
                    )
                 if user_text_input:
                    # Use case=False for case-insensitive matching
                    df_filtered = df_filtered[df_filtered[column].astype(str).str.contains(user_text_input, case=False, na=False)]

        return df_filtered
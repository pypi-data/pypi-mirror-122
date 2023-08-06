from datetime import datetime

import pandas as pd

from sdc_dp_helpers.api_utilities.date_managers import date_handler


def filter_data_by_dates(
    start_date, end_date, date_field, data_frame: pd.DataFrame, date_fmt="%Y-%m-%d"
):
    """
    Takes a data frame and filters the data by given date field and
    date scopes that can be phrases.
    If no scope is added, imply current time is expected.
    """

    _now = datetime.now().strftime(date_fmt)
    if start_date is None:
        sd = _now
    else:
        sd = date_handler(start_date, date_fmt)

    if end_date is None:
        ed = _now
    else:
        ed = date_handler(end_date, date_fmt)

    print(f"Gathering data between {sd} and {ed}.")
    # filter data by given date field
    if sd is not None and ed is not None:
        data_frame["tmp_date"] = pd.to_datetime(data_frame[date_field])
        data_frame["tmp_date"] = data_frame["tmp_date"].dt.strftime(date_fmt)
        data_frame = data_frame[
            (
                data_frame["tmp_date"]
                >= datetime.strptime(sd, date_fmt).strftime(date_fmt)
            )
            & (
                data_frame["tmp_date"]
                <= datetime.strptime(ed, date_fmt).strftime(date_fmt)
            )
        ]
        data_frame = data_frame.drop("tmp_date", axis="columns")

    if len(data_frame.index) > 0:
        return data_frame

    print(f"No data for given date filter: {sd} to {ed}.")
    return None

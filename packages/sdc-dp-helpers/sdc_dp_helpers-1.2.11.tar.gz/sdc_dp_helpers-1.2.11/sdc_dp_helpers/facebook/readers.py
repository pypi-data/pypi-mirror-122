import pandas as pd
import requests

from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.retry_managers import retry_handler
from sdc_dp_helpers.facebook.utils import filter_data_by_dates


class CustomFacebookGraphReader:
    def __init__(self, creds_file, config_file=None, **kwargs):
        self._creds = load_file(creds_file, "yml")
        self._config = load_file(config_file, "yml")
        self.version = kwargs.get("version", "v11.0")

        self._request_session = requests.Session()
        self.paging = None

    @retry_handler(exceptions=Exception, total_tries=5, should_raise=True, backoff_factor=5)
    def _graph_api_request_handler(self):
        """
        Basic handler for the Facebook api response.
        """
        print("GET: graph.facebook.com.")
        try:
            response = self._request_session.get(
                # Note the since and until params does not seem to work at all, so filtering after request
                url=f"https://graph.facebook.com/v11.0/{self._creds.get('act')}/insights",
                params={
                    "fields": self._config["fields"],
                    "date_preset": self._config["date_preset"],
                    "time_increment": self._config["time_increment"],
                    "limit": self._config["limit"],
                    "level": self._config["level"],
                    "access_token": self._creds["access_token"],
                },
            )

            if response.status_code != 200:
                raise EnvironmentError(f"Status: {response.status_code} - {response.json()}")

            response_json = response.json()
            self.paging = response_json.get("paging")

            # current configuration should not required paging since all data is
            # fetched and filtered locally
            print(self.paging)

            return response_json.get("data", None)
        except Exception as err:
            raise err

    def run_query(self):
        """
        Get metrics data from Facebook Graph API.
        The Pages API is a set of Facebook Graph API endpoints that apps can
        use to create and manage a Page's settings and content.
        Metric data of public Pages is stored by Facebook for 2 years.
        Metric data of unpublished Pages is stored for only 5 days.
        """
        json_data = self._graph_api_request_handler()
        if json_data is not None:
            data_frame: pd.DataFrame = pd.DataFrame(json_data)
            data_frame = filter_data_by_dates(
                start_date=self._config.get("start_date", None),
                end_date=self._config.get("end_date", None),
                data_frame=data_frame,
                date_field="date_start",
            )
            try:
                return data_frame.to_json(orient="records")
            except AttributeError:
                print("No data returned from Graph API.")

        return None

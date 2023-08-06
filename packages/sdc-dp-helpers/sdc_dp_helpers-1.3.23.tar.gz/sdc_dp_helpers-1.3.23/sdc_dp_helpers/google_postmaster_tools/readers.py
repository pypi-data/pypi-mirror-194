"""
CUSTOM READERS MODULE FOR GOOGLE POSTMASTER READER
"""
from typing import Dict, List, Any, Union, Generator
from googleapiclient import discovery, errors
from google.oauth2 import service_account

from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.date_managers import date_string_handler
from sdc_dp_helpers.base_readers import BaseReader


class GooglePostmasterReader(BaseReader):
    """
    Google Postmaster Reader
    """

    def __init__(self, creds_filepath: str, config_filepath: str) -> None:
        super().__init__()
        self.secrets: Dict[Any, Any] = load_file(creds_filepath)
        self.config: Dict[Any, Any] = load_file(config_filepath)
        self.service = self._get_auth()
        self.dataset: list = []
        self.success: List[bool] = []

    def _get_auth(self):
        """
        Get our credentials initialised above and use those to get client.
        """
        try:
            credentials = service_account.Credentials.from_service_account_info(
                info=self.secrets,
                scopes=["https://www.googleapis.com/auth/postmaster.readonly"],
            )
            service = discovery.build(
                serviceName="gmailpostmastertools",
                version="v1beta1",
                credentials=credentials,
            )
            return service
        except ValueError as err:
            self.not_success()
            print(f"An error has occurred: {err}")
            return None
        except RuntimeError as err:
            self.not_success()
            print(f"An error has occurred: {err}")
            return None

    def _query_handler(self, *args, **kwargs) -> dict:
        # pylint: disable=no-member
        """Handles the Query call"""
        try:
            if self.service is None:
                raise RuntimeError("Service is null.")
            if not hasattr(self.service, "domains"):
                raise RuntimeError("Service does not have domains atribute.")
            if not {"response", "request", "domain", "end_date", "start_date"}.issubset(
                set(kwargs.keys())
            ):
                raise KeyError(
                    "Invalid arguments - expecting: response, request, domain, end_date, start_date"
                )
            if kwargs["response"] is None:
                prev_request = (
                    self.service.domains()
                    .trafficStats()
                    .list(
                        parent=f"domains/{kwargs['domain']}",
                        endDate_day=int(kwargs["end_date"].day),
                        endDate_month=int(kwargs["end_date"].month),
                        endDate_year=int(kwargs["end_date"].year),
                        startDate_day=int(kwargs["start_date"].day),
                        startDate_month=int(kwargs["start_date"].month),
                        startDate_year=int(kwargs["start_date"].year),
                    )
                )
                prev_response = prev_request.execute()
                return prev_response, self.service.domains().trafficStats().list_next(
                    previous_request=prev_request,
                    previous_response=prev_response,
                )
            if kwargs["request"] is not None:
                prev_response = prev_request.execute()
                return prev_response, self.service.domains().trafficStats().list_next(
                    previous_request=prev_request,
                    previous_response=prev_response,
                )
            raise RuntimeError("Erroneous request or response")
        except errors.HttpError as err:
            self.not_success()
            print(f"An error occurred: {err}")
        except KeyError as err:
            self.not_success()
            print(f"An error occurred: {err}")
        except RuntimeError as err:
            self.not_success()
            print(f"An error occurred: {err}")
        return None, None

    def run_query(
        self,
    ) -> Union[
        Generator[Dict[List[Dict[Any, Any]], Any], None, None],
        Dict[List[Dict[Any, Any]], Any],
    ]:
        """Runs the query"""
        try:
            start_date = date_string_handler(self.config["start_date"])
            end_date = date_string_handler(self.config["end_date"])
            if start_date >= end_date:
                raise RuntimeError(
                    "An error has occured: "
                    + f"- Start Date {start_date} is not before End Date {end_date}."
                )
            for domain in self.config["domains"]:
                dataset: List[Dict[str, Any]] = []
                response, request = self._query_handler(
                    start_date=start_date,
                    end_date=end_date,
                    domain=domain,
                    request=None,
                    response=None,
                )
                dataset.extend(response["trafficStats"])
                while request is not None:
                    response, request = self._query_handler(
                        start_date=start_date,
                        end_date=end_date,
                        domain=domain,
                        request=request,
                        response=response,
                    )
                    dataset.extend(response["trafficStats"])
                if dataset is None:
                    self.not_success()
                    raise RuntimeError("response is 'None'")
                self.is_success()
                yield {
                    "date": end_date.strftime("%Y%m%d"),
                    "vertical": self.config["vertical"],
                    "brand": domain.replace(".", "_"),
                    "data": dataset,
                }
        except RuntimeError as err:
            self.not_success()
            print(f"Error occured: {err}")

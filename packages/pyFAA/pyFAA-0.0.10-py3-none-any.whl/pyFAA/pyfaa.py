import json
import requests
from bs4 import BeautifulSoup


class DataSoup:
    """
    Soup object used and created by other query objects, outputs HTML parsed BS4 object.
    :returns: HTML parsed BeautifulSoup string or None
    """

    def __init__(self, url: str, url_params: dict):
        self.url_params: dict = url_params
        self.url: str = url
        self.html_soup = self.make_soup()

    def make_soup(self):
        req = requests.get(str(self.url), params=self.url_params)
        soup = BeautifulSoup(req.content, "html.parser")
        if req.status_code != 200:
            return None
        return soup


class TailNumber:
    """
    Query object containing URL and mapping dict to create a Soup object and parse data.
    Pass in custom `label_map` to select more or less data with custom data labels.

    :returns: Dict
    """
    URL = "https://registry.faa.gov/AircraftInquiry/Search/NNumberResult?"
    REG_FIELDS = {
        "Model": "model",
        "Serial Number": "sn",
        "Status": "status",
        "Manufacturer Name": "mfg_name",
        "Certificate Issue Date": "cert_date",
        "Expiration Date": "expire_date",
        "Type Aircraft": "ac_type",
        "Type Engine": "engine_type",
        "Mode S Code (base 8 / Oct)": "modes_oct",
        "MFR Year": "mfr_year",
        "Mode S Code (Base 16 / Hex)": "modes_hex",
        "Engine Manufacturer": "engine_mfg",
        "Classification": "ac_class",
        "Engine Model": "engine_model",
        "Category": "cat"
    }

    def __init__(self,
                 tail_num: str = None,
                 label_map: dict = REG_FIELDS):
        self.tail_num = tail_num
        self.url_params = {"nNumberTxt": tail_num}
        if tail_num is None or (len(tail_num) > 6):
            raise AttributeError(f"Tail Number not valid")

    def as_dict(self):
        raw_soup = DataSoup(url=self.URL, url_params=self.url_params).html_soup
        if raw_soup is not None:
            soup_data: dict = {}
            failure_count: int = 0
            failed_on: list = []
            for field in self.REG_FIELDS:
                try:
                    data_chunk = raw_soup.find("td", text=f"{field}").find_next_sibling('td').text.strip()
                    soup_data[self.REG_FIELDS.get(field)] = data_chunk
                except AttributeError:
                    failure_count += 1
                    failed_on.append(field)
                    continue
            return {"data": soup_data,
                    "fails": {
                        "fail_count": failure_count,
                        "failed_on": failed_on}}

    def to_json(self):
        return json.dumps(self.as_dict(), indent=4, sort_keys=True)

from soup_maker import DataSoup


class TailNumber:
    URL = "https://registry.faa.gov/AircraftInquiry/Search/NNumberResult?nNumberTxt="
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

    def __init__(self, tail_num: str = None):
        self.tail_num = tail_num
        if tail_num is None or (len(tail_num) > 6):
            raise AttributeError(f"Tail Number not valid")

    def as_dict(self):
        raw_soup = DataSoup(url=self.URL, query=self.tail_num).html_soup
        if raw_soup is not None:
            soup_data: dict = {}
            for field in self.REG_FIELDS:
                try:
                    data_chunk = raw_soup.find("td", text=f"{field}").find_next_sibling('td').text.strip()
                    soup_data[self.REG_FIELDS.get(field)] = data_chunk
                except AttributeError:
                    continue
            return soup_data

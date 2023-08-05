# Ecotricity Client

This python library is intended to be used against the Ecotricity API used on the [customer portal](https://online.ecotricity.co.uk/) for fetching meter readings.

Example usage:

```
from ecotricity.client.requests import AgreementsRequest, ReadsRequest, AccountsRequest

from ecotricity.client.service import open_session

user = "yourUser"
password = "yourPassword"

session = open_session(user, password)

accounts_req = AccountsRequest()
accounts_res = accounts_req.get_accounts(session)
for account in accounts_res.data.results:
    agreements_req = AgreementsRequest()
    agreements_res = agreements_req.get_agreements(session, account.id,)
    for agreement in agreements_res.data.results:
        for product in agreement.products:
            for meter_point in product.meter_points:
                fuel_type = meter_point.fuel_type
                meter_id = meter_point.industry_id
                meter_reads_req = ReadsRequest()
                meter_reads_res = meter_reads_req.get_reads(session, meter_point.industry_id)
                for readings in meter_reads_res.data.results:
                    for reading in readings:
                        register_id = reading.register_industry_id
                        print(f'{fuel_type} - {meter_id} - {register_id} - {reading.date} - {reading.value}')
```

from datetime import datetime, timedelta
import urllib.parse
from .apicaller import APICaller

API_BASE_URL = 'https://api-mt.metrc.com'


class Metrc:
    def __init__(self, vendor_api_key, user_api_key):
        self.endpoints = {'facilities': ['/facilities/v1'],
                          'packages': ['/packages/v1/active', '/packages/v1/inactive'],
                          'harvests': ['/harvests/v1/active', '/harvests/v1/inactive'],
                          'lab_results': ['/labtests/v1/results'],
                          'outgoing_transfers': ['/transfers/v1/outgoing'],
                          'deliveries': ['/transfers/v1/{id}/deliveries'],
                          'sales_receipts': ['/sales/v1/receipts/active'],
                          'sales_transactions': ['/sales/v1/receipts/{id}']}

        self.vendor_api_key = vendor_api_key
        self.user_api_key = user_api_key
        self.api = APICaller(self.vendor_api_key, self.user_api_key)

        self.facility_data = []
        self.facilities = []
        self.dispensaries = []
        self.mipps = []
        self.init_facilities()

    def get_user_id(self):
        return self.user_api_key[0:7]

    def get_iso_start_date(self, facility):
        # Return the facility start date in ISO 8601 format with UTC offset.
        try:
            assert(facility in self.facilities)
        except AssertionError:
            print(f"Facility {facility} not available.")
            return None

        for f in self.facility_data:
            if f['License']['Number'] == facility:
                start_date = f['License']['StartDate']
                start_date += 'T00:00:00+00:00'
                break

        return start_date

    def get_json_from_urls(self, urls):
        # Returns list of unmodified JSON from endpoint GET requests.
        response_json = self.api.get_from_url_list(urls)
        return response_json

    def get_24_hour_periods(self, start_date, end_date):
        # Ingest a start and end date and return a list of tuples representing periods no greater than 24 hours, a
        # limitation of the Metrc API.
        try:
            # Verify the strings passed are ISO 8601 format and that the end date is greater than the start date.
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            assert((end_dt - start_dt).total_seconds() >= 0)
        except ValueError:
            print("Invalid date string: Must be ISO format.")
        except AssertionError:
            print("End date must be greater than start date.")
        except ValueError:
            print("One or more dates not in valid ISO format.")

        period_tuples = []

        while(1):
            # Calculate the difference in hours between the start and end date.
            difference = end_dt - start_dt
            difference = difference.total_seconds() / 3600

            if difference > 24:
                # Use the counter to create increments of < 24 hours. In this case, we subtract 1 millisecond to avoid
                # overlap when calculating subsequent 24 hour periods.
                end_date_counter = (start_dt + timedelta(days=1)) - timedelta(milliseconds=1)
                period_tuples.append((start_dt.isoformat(), end_date_counter.isoformat()))
                start_dt += timedelta(days=1)
            else:
                # If the original start and end represent a period of 24 hours or less, no modification is necessary.
                # This is also true when arriving at the end of the datetime iteration process above.
                period_tuples.append((start_dt.isoformat(), end_dt.isoformat()))
                break

        return period_tuples

    def init_facilities(self):
        # Make a request for the users available facilities. Store this in a property named "facilities".
        print('Initializing facility list...')
        ep = self.endpoints['facilities'][0]
        url = f"{API_BASE_URL}{ep}"
        self.facility_data = self.api.get_from_url_list([url])[0]

        self.facilities.clear()
        for facility in self.facility_data:
            self.facilities.append(facility['License']['Number'])

        self.dispensaries = [facility['License']['Number'] for facility in self.facility_data
                             if facility['FacilityType']['CanSellToPatients']]
        self.mipps = [facility['License']['Number'] for facility in self.facility_data
                      if facility['FacilityType']['CanInfuseProducts']]

    def get_data(self, endpoint, license_number, start_date, end_date, **kwargs):
        try:
            assert(license_number in self.facilities)
        except AssertionError:
            print('Invalid license: User must have access to facility.')

        if endpoint == 'sales_transactions':
            return self.get_sales_transactions(license_number=license_number,
                                               sales_date_start=start_date,
                                               sales_date_end=end_date,
                                               receipt_ids=kwargs.get('receipt_ids'),
                                               flatten=kwargs.get('flatten'))
        elif endpoint == 'packages':
            return self.get_packages(license_number=license_number,
                                     last_modified_start=start_date,
                                     last_modified_end=end_date,
                                     flatten=kwargs.get('flatten'))

    def get_packages(self, license_number, last_modified_start, last_modified_end, flatten=True):
        print('Getting packages for ' + license_number + ' between ' + last_modified_start + ' and ' + last_modified_end)

        date_ranges = self.get_24_hour_periods(last_modified_start, last_modified_end)
        urls = []

        for ep in self.endpoints['packages']:
            for period in date_ranges:
                query_dict = {'licenseNumber': license_number,
                              'lastModifiedStart': period[0],
                              'lastModifiedEnd': period[1]}
                query = urllib.parse.urlencode(query_dict)
                urls.append(f"{API_BASE_URL}{ep}?{query}")

        response = self.get_json_from_urls(urls)

        packages = [package for period in response if period for package in period]

        if flatten:
            print('Flattening packages...')
            doc_list = []

            for package in packages:
                item = package.pop('Item')
                new_item = {}

                for key, value in item.items():
                    key = 'Item' + key
                    new_item.update({key: value})

                package.update(new_item)
                doc_list.append(package)

            return doc_list
        else:
            return packages

    def get_sales_receipts(self, license_number, sales_date_start, sales_date_end):
        # Return a tuple containing a list of receipt IDs and list of receipts represented as dictionaries.
        print('Getting sales receipts for ' + license_number + ' between ' + sales_date_start + ' and ' + sales_date_end)

        date_ranges = self.get_24_hour_periods(sales_date_start, sales_date_end)
        urls = []

        for ep in self.endpoints['sales_receipts']:
            for period in date_ranges:
                query_dict = {'licenseNumber': license_number, 'salesDateStart': period[0], 'salesDateEnd': period[1]}
                query = urllib.parse.urlencode(query_dict)
                urls.append(f"{API_BASE_URL}{ep}?{query}")

        response = self.get_json_from_urls(urls)

        # We get a list of lists from the async url request -- a list of receipts for each period requested, all
        # within the top-level list. Here we flatten this and extract a list of receipt IDs for easy integration with
        # other endpoints (transactions).
        receipts = [receipt for period in response if period for receipt in period]
        ids = [receipt['Id'] for receipt in receipts if isinstance(receipt, dict)]

        return (ids, receipts)

    def get_sales_transactions(self, license_number, sales_date_start=None, sales_date_end=None, receipt_ids=None,
                               flatten=True):
        # Return a list of transaction information using a list of receipt IDs for lookup. If flatten is true, return
        # a list of elements containing transaction information per individual package. Multiple elements
        # (transactions) can share a receipt ID. If flatten is false, return a list of receipts containing a nested list
        # of individual packages involved. First, if no IDs are provided, get them automatically for the date range
        # provided. This requires calling get_sales_reciepts().
        if not receipt_ids:
            try:
                assert(sales_date_start)
                assert(sales_date_end)
            except AssertionError:
                print('No receipt IDs provided: start and end date required.')

            print('No IDs provided when getting transactions...')
            receipt_ids = self.get_sales_receipts(license_number, sales_date_start, sales_date_end)[0]
            if not receipt_ids:
                print("No receipts in time period specified. Skipping transaction lookup.")
                return []

        print('Getting sales transactions...')
        urls = []

        for ep in self.endpoints['sales_transactions']:
            for i in receipt_ids:
                query_dict = {'licenseNumber': license_number}
                query = urllib.parse.urlencode(query_dict)
                ep_with_id = ep.replace('{id}', str(i))
                urls.append(f"{API_BASE_URL}{ep_with_id}?{query}")

        response = self.get_json_from_urls(urls)

        if flatten:
            print('Flattening transactions...')
            doc_list = []

            # Extract relevant information that would otherwise not be included when isolating an individual
            # transaction and append it.
            for receipt in response:
                receipt_info = {
                    'ReceiptNumber': receipt['ReceiptNumber'],
                    'SalesDateTime': receipt['SalesDateTime'],
                    'SalesCustomerType': receipt['SalesCustomerType'],
                    'PatientLicenseNumber': receipt['PatientLicenseNumber'],
                    'IsFinal': receipt['IsFinal'],
                    'ArchivedDate': receipt['ArchivedDate'],
                    'RecordedDateTime': receipt['RecordedDateTime'],
                    'RecordedByUserName': receipt['RecordedByUserName'],
                    'ReceiptLastModified': receipt['LastModified']
                }

                for transaction in receipt['Transactions']:
                    transaction.update(receipt_info)
                    doc_list.append(transaction)

            return doc_list
        else:
            return response


if __name__ == '__main__':
    import os

    vendor_api_key = os.environ['METRC_VENDOR_API_KEY']
    user_api_key = os.environ['METRC_USER_API_KEY']
    m = Metrc(vendor_api_key, user_api_key)

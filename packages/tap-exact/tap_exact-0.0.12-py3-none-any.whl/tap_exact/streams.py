"""Stream type classes for tap-exact."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_exact.client import ExactOnlineStream
from exactonline.resource import GET

from datetime import datetime

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class SalesInvoicesStream(ExactOnlineStream):
    """Define custom stream."""

    name = "sales-invoices"
    primary_keys = ["InvoiceID"]
    replication_key = "Modified"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property(
            "InvoiceID",
            th.StringType,
            description="The unique identifier of the invoice"
        ),
        th.Property(
            "InvoiceDate",
            th.DateTimeType,
            description="The invoice date"
        ),
        th.Property(
            "InvoiceNumber",
            th.IntegerType,
            description="The invoice number"
        ),
        th.Property(
            "InvoiceTo",
            th.StringType,
            description="The customer whom the invoice is made for"
        ),
        th.Property(
            "InvoiceToName",
            th.StringType,
            description="The name of the customer whom the invoice is made for"
        ),
        th.Property(
            "OrderDate",
            th.DateTimeType,
            description="The order date"
        ),
        th.Property(
            "OrderedBy",
            th.StringType,
            description="The customer who made the order"
        ),
        th.Property(
            "OrderedByName",
            th.StringType,
            description="The name of the customer who made the order"
        ),
        th.Property(
            "AmountDC",
            th.NumberType,
            description="Amount in the default currency of the company"
        ),
        th.Property(
            "Modified",
            th.DateTimeType,
            description="Last modified date"
        ),
    ).to_dict()

    def get_path(self, context: Optional[dict]) -> str:
        """Return the path of the Exact API"""

        replication_key_value = self.get_starting_timestamp(context).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
        path = "/salesinvoice/SalesInvoices?" \
            f"$filter={self.replication_key}%20ge%20datetime%27{replication_key_value}%27&" \
            "$select=InvoiceID,InvoiceDate,InvoiceNumber,InvoiceTo,InvoiceToName,OrderDate,OrderedBy,OrderedByName,AmountDC,Modified"

        return path

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator or row-type dictionary objects"""
        
        resp = self.conn.rest(GET('v1/%d/%s' % (self.division, self.get_path(context) )))
        
        # The fields that have /Date(unixmilliseconds)/ objects that should be converted into datetime objects
        keys = ['InvoiceDate', 'Modified', 'OrderDate']

        for row in resp:
            
            # We loop through the keys that should be modified
            for key in keys:
                row[key] = datetime.fromtimestamp( int(row[key][6:-2] / 1000.0) )

            yield row
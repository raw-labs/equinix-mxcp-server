import pandas as pd


def _to_clean_string(value):
    """Convert mixed Excel cell values to trimmed strings."""
    if pd.isna(value):
        return pd.NA
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value).strip()


def model(dbt, session):
    """Load Vodafone Ireland billing data from the TDR worksheet."""
    dbt.config(materialized="table")

    file_path = "source_data/Vodafone Ireland Supplier Data.xlsx"
    source_df = pd.read_excel(file_path, sheet_name="TDR", header=1, engine="openpyxl")

    column_map = {
        "Trx Number": "trx_number",
        "Trx Date": "trx_date",
        "Currency": "currency",
        "Product Category": "product_category",
        "Charge Type": "charge_type",
        "charge type clean": "charge_type_clean",
        "IBX": "ibx",
        "Quantity": "quantity",
        "Unit Price": "unit_price",
        "Line Amount": "line_amount",
        "GST Amount": "gst_amount",
        "Total Amount": "total_amount",
        "Description": "description",
        "Product Offering": "product_offering",
        "Product Elements": "product_elements",
        "Billing Agreement": "billing_agreement",
        "Serial Number": "serial_number",
        "Recurring Charge From Date": "recurring_charge_from",
        "Recurring Charge To Date": "recurring_charge_to",
        "Customer Name": "customer_name",
    }

    billing_df = source_df[list(column_map.keys())].rename(columns=column_map).copy()

    billing_df["trx_date"] = pd.to_datetime(billing_df["trx_date"], errors="coerce").dt.date
    billing_df["recurring_charge_from"] = pd.to_datetime(
        billing_df["recurring_charge_from"], errors="coerce"
    ).dt.date
    billing_df["recurring_charge_to"] = pd.to_datetime(
        billing_df["recurring_charge_to"], errors="coerce"
    ).dt.date

    numeric_columns = ["quantity", "unit_price", "line_amount", "gst_amount", "total_amount"]
    for column in numeric_columns:
        billing_df[column] = pd.to_numeric(billing_df[column], errors="coerce").astype(float)

    string_columns = [
        "trx_number",
        "currency",
        "product_category",
        "charge_type",
        "charge_type_clean",
        "ibx",
        "description",
        "product_offering",
        "product_elements",
        "billing_agreement",
        "serial_number",
        "customer_name",
    ]
    for column in string_columns:
        billing_df[column] = billing_df[column].map(_to_clean_string).astype("string")

    billing_df["currency"] = billing_df["currency"].str.upper()

    billing_df = billing_df.dropna(
        subset=["trx_number", "trx_date", "currency", "product_category", "charge_type", "ibx"]
    )

    final_columns = [
        "trx_number",
        "trx_date",
        "currency",
        "product_category",
        "charge_type",
        "charge_type_clean",
        "ibx",
        "quantity",
        "unit_price",
        "line_amount",
        "gst_amount",
        "total_amount",
        "description",
        "product_offering",
        "product_elements",
        "billing_agreement",
        "serial_number",
        "recurring_charge_from",
        "recurring_charge_to",
        "customer_name",
    ]

    return billing_df[final_columns]

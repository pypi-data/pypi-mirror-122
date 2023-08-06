from Excelutilities.importing_data_helpers import add_col_data_from_another_sheet
import decimal
import datetime
add_col_data_from_another_sheet("ASIN data", "INPUT DATA", [float, int, decimal.Decimal,datetime.datetime, str])

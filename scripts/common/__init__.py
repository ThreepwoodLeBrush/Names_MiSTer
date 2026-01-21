class _Options:
    names_files = {
            "names_CHAR18_Manufacturer_EU": 18,
            "names_CHAR18_Manufacturer_JP": 18,
            "names_CHAR18_Manufacturer_US": 18,
            "names_CHAR18_Common_EU": 18,
            "names_CHAR18_Common_JP": 18,
            "names_CHAR18_Common_US": 18,
            "names_CHAR28_Manufacturer_EU": 28,
            "names_CHAR28_Manufacturer_JP": 28,
            "names_CHAR28_Manufacturer_US": 28,
            "names_CHAR28_Common_EU": 28,
            "names_CHAR28_Common_JP": 28,
            "names_CHAR28_Common_US": 28,
            "names_CHAR54_Manufacturer_EU": 54,
        }

    sorted_names_files = sorted(names_files.keys())

    csv_separator = ";"
    csv_quote_char = '|'
    format_line_separator = "|"
    formatter_line_names_txt = "                   |                  |         |                         |"
    straight_line_char = "="
    padding_char = " "
    straight_line_every = 40
    format_line_every = 10
    output_names_csv = "names.csv"
    input_names_csv = "names.csv"
    cores_column_rightpadding_csv = 30
    cores_column_rightpadding_txt = 19
    cores_column_name = "Cores"
    strip_from_reference = "names_CHAR"

options = _Options

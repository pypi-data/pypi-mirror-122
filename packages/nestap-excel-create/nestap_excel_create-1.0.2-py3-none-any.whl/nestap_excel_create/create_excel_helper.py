from decimal import Decimal
from io import BytesIO
import xlsxwriter

EXCEL_STR_FORMAT = 1
EXCEL_DATETIME_FORMAT = 2
EXCEL_DECIMAL_FORMAT = 3
EXCEL_DATE_FORMAT = 4


def worksheet_format(workbook):
    format_header = workbook.add_format(
        {'align': 'center', 'bold': 1, 'font_size': 10, 'font_color': 'blue', 'bg_color': '#DAF7A6',
         'underline': True, 'valign': 'vcenter'}
    )
    format_data = workbook.add_format({'align': 'center', 'font_size': 10, 'valign': 'vcenter'})
    heading_format = workbook.add_format({'align': 'left', 'font_size': 15, 'valign': 'vcenter'})
    return format_header, format_data, heading_format


def create_excel_sheets(attachments_list):
    attachments = []
    try:
        if attachments_list and len(attachments_list) > 0:
            for attachment_excel in attachments_list:
                excel_memory_buffer = create_excel(attachment_excel['sheets_list'])
                if excel_memory_buffer:
                    receipt_excel = {
                        "filename": attachment_excel['file_name'] + ".xlsx",
                        "content": excel_memory_buffer.read(),
                        "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    }
                    attachments.append(receipt_excel)
    except Exception as e:
        print(e)
    return attachments


def create_excel_header(excel_sheet, columns_keys, format_header, header_row):
    column_no = 0
    for col in columns_keys:
        excel_sheet.write(header_row, column_no, col[1], format_header)
        column_no += 1


def create_excel_rows(excel_sheet, columns_keys, row_format, data_row_list):
    row_no = 1
    for each_row in data_row_list:
        column_no = 0
        for col in columns_keys:
            try:
                if col[2] == EXCEL_DATETIME_FORMAT:
                    excel_sheet.write(row_no, column_no, each_row[col[0]].strftime('%Y-%m-%d %H:%M'), row_format)
                elif col[2] == EXCEL_DECIMAL_FORMAT:
                    excel_sheet.write(row_no, column_no, Decimal(each_row[col[0]]).quantize(Decimal('0.1')), row_format)
                elif col[2] == EXCEL_STR_FORMAT:
                    excel_sheet.write(row_no, column_no, str(each_row.get(col[0], '--')), row_format)
                elif col[2] == EXCEL_DATE_FORMAT:
                    excel_sheet.write(row_no, column_no, each_row[col[0]].strftime('%Y-%m-%d'), row_format)
                else:
                    excel_sheet.write(row_no, column_no, each_row.get(col[0], '--'), row_format)
                column_no += 1
            except:
                excel_sheet.write(row_no, column_no, each_row.get(col[0], '--'), row_format)
                column_no += 1
        row_no += 1


# In create_excel method you can pass list of dictionary sheet_name, column_name and data_list that's it.
def create_excel(attachment_excel):
    workbook_name = None
    try:
        workbook_name = BytesIO()
        workbook = xlsxwriter.Workbook(workbook_name, {'in_memory': True})
        for each_sheet in attachment_excel:
            worksheet = workbook.add_worksheet(each_sheet['sheet_name'])
            format_header, format_data, heading_format = worksheet_format(workbook)
            create_excel_header(worksheet, each_sheet['columns_keys'], format_header, 0)
            create_excel_rows(worksheet, each_sheet['columns_keys'], format_data, each_sheet['data_list'])
        workbook.close()
        workbook_name.seek(0)
    except Exception as e:
        print(e)
        if workbook_name:
            workbook_name.close()
        workbook_name = None
    return workbook_name

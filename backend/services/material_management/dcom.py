import pythoncom
import win32com.client


def read_excel_data(file_path, sheet_name="Sheet1", remote_server=None):
    """ Đọc dữ liệu từ file Excel thông qua DCOM trên máy chủ hoặc từ xa """
    try:
        pythoncom.CoInitialize()

        if remote_server:
            excel = win32com.client.DispatchEx("Excel.Application", remote_server)
        else:
            excel = win32com.client.Dispatch("Excel.Application")

        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        sheet = workbook.Sheets(sheet_name)

        data = []
        row = 2
        while sheet.Cells(row, 1).Value:
            material_name = sheet.Cells(row, 1).Value
            quantity = sheet.Cells(row, 2).Value
            supplier_id = sheet.Cells(row, 3).Value
            data.append({"name": material_name, "quantity": quantity, "supplier_id": supplier_id})
            row += 1

        workbook.Close(SaveChanges=False)
        excel.Quit()
        pythoncom.CoUninitialize()
        return data
    except Exception as e:
        return {"error": str(e)}

def update_excel_data(file_path, updated_data, remote_server=None):
    """ Cập nhật dữ liệu vào file Excel thông qua DCOM """
    try:
        pythoncom.CoInitialize()

        if remote_server:
            excel = win32com.client.DispatchEx("Excel.Application", remote_server)
        else:
            excel = win32com.client.Dispatch("Excel.Application")

        excel.Visible = False
        workbook = excel.Workbooks.Open(file_path)
        sheet = workbook.Sheets("Sheet1")  # Chỉnh sửa đúng sheet

        for i, row in enumerate(updated_data, start=2):
            sheet.Cells(i, 1).Value = row["name"]
            sheet.Cells(i, 2).Value = row["quantity"]
            sheet.Cells(i, 3).Value = row["supplier_id"]

        workbook.Save()  # Lưu lại file Excel
        workbook.Close()
        excel.Quit()
        pythoncom.CoUninitialize()

        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
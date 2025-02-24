import win32com.client

try:
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True  # Kiểm tra xem có mở được Excel không
    print("Excel COM Object đã khởi chạy thành công!")
    excel.Quit()
except Exception as e:
    print(f"Lỗi: {e}")

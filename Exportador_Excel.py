from openpyxl import Workbook
# Create a workbook and add a worksheet.
wb = Workbook()
# grab the active worksheet
ws = wb.active
class ExportadorExcel:

    def __init__(self):
        self.row = 0
        self.col = 0
    
    def generarReporteChecadas(self,fecha1,fecha2):
        
        

from openpyxl import Workbook


'''В этом файле происходит запись полученных данных в таблицу excel'''
workbook = Workbook()
sheet = workbook.active
sheet["A1"] = 'Domain'
sheet["B1"] = 'IP'
sheet["C1"] = 'Open Port'
sheet["D1"] = 'Service'
sheet["E1"] = 'Version'
sheet["F1"] = 'Services Info'

sheet.column_dimensions['A'].width = 15
sheet.column_dimensions['B'].width = 15
sheet.column_dimensions['C'].width = 15
sheet.column_dimensions['D'].width = 30
sheet.column_dimensions['E'].width = 67
sheet.column_dimensions['F'].width = 30

class writeExcel(object):

    def __init__(self, sheet_1, sheet_2, sheet_3, sheet_4, sheet_5):
        self.sheet_1 = sheet_1
        self.sheet_2 = sheet_2
        self.sheet_3 = sheet_3
        self.sheet_4 = sheet_4
        self.sheet_5 = sheet_5

    def write_ports(self):
        d = 1
        sheet["A2"] = self.sheet_1
        sheet["B2"] = self.sheet_2
        for open_port in self.sheet_3:
            d += 1
            sheet['C' + str(d)] = open_port

    def write_services(self):
        d = 1
        for service_of_port in self.sheet_4:
            d += 1
            sheet['D' + str(d)] = service_of_port

    def write_versions(self):
        d = 1
        for version_of_service in self.sheet_5:
            d += 1
            sheet['E' + str(d)] = version_of_service

    def save_all(self):
        workbook.save(filename='PentestInfo.xlsx')



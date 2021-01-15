# -*- coding: utf-8 -*-
"""
Created on Fri May  1 22:46:33 2020

@author: ovicko
"""

from bs4 import BeautifulSoup
import requests
import time
import xlsxwriter
hudumaUrl = "https://www.hudumanamba.go.ke/search-counties/#"

source = requests.get(hudumaUrl).text
soup = BeautifulSoup(source,'lxml')
table = soup.find("div", {"class":"wpb_wrapper"})

#table1 = table.find('table')
table1 = soup.find("table", {"class":"tablepress","id":"tablepress-3"})

#get the columns
table_head = table1.find("thead")
table_head_row = table_head.find("tr")

heading_list = []
for column in table_head_row.find_all("th"):
    column_name = column.text
    heading_list.append(column_name)
    
print(heading_list)

#get tbody
# =============================================================================
tb_tbody = table1.find("tbody")
tb_tbody_row = tb_tbody.find_all("tr")
# 
table_data = []
for row in tb_tbody_row:
    row_data = []
    for data in row.find_all("td"):
        row_data.append(data.text)
         #print(data.text,end=" ")
    table_data.append(row_data)
#print(table_data)
# =============================================================================
 # Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('counties.xlsx')
worksheet = workbook.add_worksheet()

  # Adjust the column width.
worksheet.set_column(1, 1, 15)
 # Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': 1})
  # Write some data headers.
worksheet.write('A1', 'COUNTY_CODE', bold)
worksheet.write('B1', 'COUNTY', bold)
worksheet.write('C1', 'SUB_COUNTY', bold)
worksheet.write('D1', 'DIVISION', bold)
worksheet.write('E1', 'LOCATIONS', bold)
worksheet.write('F1', 'SUB_LOCATIONS', bold)
 
  # Start from the first cell below the headers.
row = 1
col = 0

for COUNTY_CODE, COUNTY, SUB_COUNTY,DIVISION,LOCATIONS, SUB_LOCATIONS in (table_data):

     worksheet.write_string  (row, col,     COUNTY_CODE )
     worksheet.write_string  (row, col + 1, COUNTY)
     worksheet.write_string  (row, col + 2, SUB_COUNTY)
     worksheet.write_string  (row, col + 3, DIVISION)
     worksheet.write_string  (row, col + 4, LOCATIONS)
     worksheet.write_string  (row, col + 5, SUB_LOCATIONS)
     row += 1
workbook.close()
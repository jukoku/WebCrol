import gspread
import datetime
from sv import*

# json 파일이 위치한 경로를 값으로 줘야 합니다.
gc = gspread.service_account(json_file_path)
wks = gc.open_by_url(spreadsheet_url)

wks = wks.worksheet('테스트')
wks.clear()

# Update a range of cells using the top left corner address
wks.update('A1', [[1, 2], [3, 4]])

# Or update a single cell
wks.update_acell('B42', "it's down there somewhere, let me take another look.")

# Format the header
wks.format('A1:B1', {'textFormat': {'bold': True}})
now = datetime.datetime.now()
testlist = ['ai', 'best', 'come', 'down', 'else']
testlist.append(now.strftime("%Y-%m-%d %H:%M:%S"))
count = [x for x in range(0, len(testlist))]
list_col = [testlist, count]

linklist = wks.col_values(1)
print(linklist)

for link in linklist:
  print(link)

print(list_col)
wks.insert_cols(list_col, 1)
# wks.append_row(testlist)



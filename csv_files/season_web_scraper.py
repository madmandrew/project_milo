from bs4 import BeautifulSoup

# config variables...
bracketYear = 2016  # end of the season year ie 2015-2016 is 2016 bracket year
file_type = "team_season"
table_id = "6472"  # the randomly generated id that is assigned to the table in html
path_to_project = "C:\\Users\\andrew\\PycharmProjects\\"

soup = BeautifulSoup(open("{}project_milo\\csv_files\\html_sources\\season_html_source\\{}_{}.html".format(path_to_project, bracketYear, file_type)))

file = open("{}project_milo\\csv_files\\season_files\\{}_{}.csv".format(path_to_project, bracketYear, file_type), "w")


tableRows = soup.find("table", id="table-{}".format(table_id)).find("tbody").find_all('tr')

headerRow = tableRows[0].find_all('td')
del headerRow[0]
header = ""
for cell in headerRow:
    header += cell.find_all("b")[0].get_text() + ","
header = header[:-1] + "\n"

file.write(header)

for row in tableRows:
    cells = row.find_all('td')
    # thisTeam = cells[1].find_all('span')[0].get_text()
    del cells[0]  # delete team number
    rowOfData = ""
    for cell in cells:
        rowOfData += cell.find_all('span')[0].get_text() + ","
    rowOfData = rowOfData[:-1] + "\n"

    file.write(rowOfData)
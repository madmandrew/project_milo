from bs4 import BeautifulSoup

def get_oppenent(tableRows, currentRowIndex, roundIndex, result):
    for i in range(currentRowIndex + 1, 64):
        thisResult = tableRows[i].find_all('td')[roundIndex].get_text()
        if thisResult != 'x':
            parts = thisResult.split('-')
            thisResult = parts[1] + '-' + parts[0]
            if thisResult == result:
                return tableRows[i].find_all('td')[2].get_text()
    return "none"

bracketYear = 2016
soup = BeautifulSoup(open("C:\\Users\\andrew\\Downloads\\{}.html".format(bracketYear)))


#print(soup.prettify())
tableRows = soup.find("table", id="tbl").find("tbody").find_all('tr')
del tableRows[0]
del tableRows[0]

parsedRows = []
for row in tableRows:
    cells = row.find_all('td')
    if len(cells) > 8:
        round1 = cells[9].get_text()
        if '-' in round1:
            parsedRows.append(row)

file = open("{}_bracket_results.csv".format(bracketYear), "w")
for i, row in enumerate(parsedRows):
    cells = row.find_all('td')
    thisTeam = cells[2].get_text()

    roundBaseValue = 8
    for roundNumber in range(1, 7):
        roundIndex = roundBaseValue + roundNumber
        roundResult = cells[roundIndex].get_text()
        if roundResult == 'x':
            break
        else:
            opponent = get_oppenent(parsedRows, i, roundIndex, roundResult)
            if opponent != "none":
                scores = roundResult.split('-')
                winning_team = ""
                if int(scores[0]) > int(scores[1]):
                    # this team won
                    winning_team = thisTeam
                else:
                    # opponent won
                    winning_team = opponent
                print("{} vs {} | round {} | score: {} | winner: {}".format(thisTeam, opponent, roundNumber, roundResult, winning_team))
                # for csv
                print("year | round | team 1 | team 2 | winner")
                print("{} | {} | {} | {} | {}".format(bracketYear, roundNumber, thisTeam, opponent, winning_team))
                csvString = "{},{},{},{},{}\n".format(bracketYear, roundNumber, thisTeam, opponent, winning_team)
                print(csvString)
                file.write(csvString)


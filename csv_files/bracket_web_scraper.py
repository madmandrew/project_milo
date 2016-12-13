from bs4 import BeautifulSoup

previous_matches = []
previous_matches_by_round = [[], [], [], [], [], []]
def get_oppenent(tableRows, currentRowIndex, roundIndex, result, roundNumber):
    roundLimits = [1, 4, 8, 16, 32, 64]
    roundLimit = currentRowIndex + 1 + roundLimits[roundNumber - 1]
    if roundLimit > 64:
        roundLimit = 64
    for i in range(currentRowIndex + 1, roundLimit):
        thisResult = tableRows[i].find_all('td')[roundIndex].get_text()
        if thisResult != 'x':
            parts = thisResult.split('-')
            thisResult = parts[1] + '-' + parts[0]
            if thisResult == result:
                return tableRows[i].find_all('td')[2].get_text()
    return "none"

def loadBracketFromHtml(bracketYear):
    relativePath = "C:\\Users\\andrew\\PycharmProjects\\"
    soup = BeautifulSoup(open("{}project_milo\\csv_files\\html_sources\\bracket_source\\{}.html".format(relativePath, bracketYear)))


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

    file = open("{}project_milo\\csv_files\\bracket_results\\{}_bracket_results.csv".format(relativePath, bracketYear), "w")
    file.write("Match Number,Bracket Year,Round Number,Team 1,Team 2,Winner\n")
    matchNumbers = [1, 33, 49, 57, 61, 63]
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
                opponent = get_oppenent(parsedRows, i, roundIndex, roundResult, roundNumber)
                if thisTeam in previous_matches_by_round[roundNumber - 1]:
                    opponent = "none"

                if opponent != "none" and ("{},{}".format(opponent, thisTeam) not in previous_matches):
                    scores = roundResult.split('-')
                    winning_team = ""
                    if int(scores[0]) > int(scores[1]):
                        # this team won
                        winning_team = thisTeam
                    else:
                        # opponent won
                        winning_team = opponent
                    #print("Match {}: {} vs {} | round {} | score: {} | winner: {}".format(matchNumbers[roundNumber - 1], thisTeam, opponent, roundNumber, roundResult, winning_team))
                    # for csv
                    #print("match | year | round | team 1 | team 2 | winner")
                    #print("{} | {} | {} | {} | {}".format(bracketYear, roundNumber, thisTeam, opponent, winning_team))
                    csvString = "{},{},{},{},{},{}\n".format(matchNumbers[roundNumber - 1], bracketYear, roundNumber, thisTeam, opponent, winning_team)
                    #print(csvString)

                    previous_matches.append("{},{}".format(thisTeam, opponent))
                    previous_matches_by_round[roundNumber - 1].append(thisTeam)
                    previous_matches_by_round[roundNumber - 1].append(opponent)

                    file.write(csvString)
                    matchNumbers[roundNumber - 1] += 1

for bracketYear in range(2010, 2017):
    print("Loading bracket: {}".format(bracketYear))
    loadBracketFromHtml(bracketYear)

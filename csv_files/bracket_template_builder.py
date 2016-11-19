relativePath = "C:\\Users\\andrew\\PycharmProjects\\"
file = open("{}project_milo\\csv_files\\bracket_template.csv".format(relativePath), "w")

file.write("Match Number,From Match 1,From Match 2\n")

matchNumbers = [1, 33, 49, 57, 61, 63]
for roundIndex in range(0, 4):
    previousRoundMatchNumber = matchNumbers[roundIndex]
    for currentMatchNumber in range(matchNumbers[roundIndex + 1], matchNumbers[roundIndex + 2]):
        print("Match {} | from matches {} & {}".format(currentMatchNumber, previousRoundMatchNumber, previousRoundMatchNumber + 1))
        file.write("{},{},{}\n".format(currentMatchNumber, previousRoundMatchNumber, previousRoundMatchNumber + 1))
        previousRoundMatchNumber += 2
print("Match 63 | from matches 62 & 61")
file.write("63,62,61\n")

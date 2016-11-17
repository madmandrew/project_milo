"""
    We need to read the appropriate data from database to generate our "test_data"

    For example parse through a bracket and pull for each match-up, both team stats(or ids to team normalized stats), and result of the match up
    and store that as a row of data.

    We should probably normalize all data at this point also.

    This will make it so that we can just feed those rows directly into our algorithm

    example might be
    bracket year | round | team1 normalized data ID | team2 normalized data ID | result
    2016 | 1 | 12 | 34 | 12

    ----------------------------------------------------------------------------------------------
    Later we are going to have to start with just round 1 data and from those results setup the next round of matchups
    so we should probably figure out how we want to do that?
    maybe assign match id's to each round like 1 through 32 and pair result from match 1 to 2, 3 to 4, then 1&2 to 3&4 and so on
"""
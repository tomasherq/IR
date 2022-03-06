queries = []

with open("2019qrels-pass.txt") as file_read:
    for line in file_read:
        queryId = line.split(" ")[0]
        if queryId not in queries:
            queries.append(queryId)

print(len(queries))

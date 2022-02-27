from pyserini.search import SimpleSearcher
import os

# Use optimal from pyserini github and add extensions! from pyserini
K1 = float(0.82)
B = float(0.68)
K = 1000

INDEX = "../indexes/lucene-index-msmarco-passage"
OUTPUT = f"../runs/run_prob_passage_{len(os.listdir('../runs'))}_train.txt"
TOPICS = "../queries/msmarco-test2019-queries.tsv"


def readQueryFile(filename):

    queriesIds = []
    queries = []
    with open(filename, "r") as file_read:
        for line in file_read.readlines():

            frags = line.split("\t")
            queriesIds.append(frags[0].strip())
            queries.append(frags[-1].strip())

    return queriesIds, queries


def writeResults(hits, outputFilename):

    with open(outputFilename, "w") as file_write:
        for results in hits.items():
            queryId = results[0].split("\t")[0]

            i = 0
            for hit in results[1]:
                file_write.write(f'{results[0]}\t{hit.docid}\t{i+1}\n')
                i += 1


queriesIds, queries = readQueryFile(TOPICS)

# Create the searcher giving it the indexes and the BM parameters
searcher = SimpleSearcher(INDEX)
searcher.set_bm25(K1, B)


# Retrieve all the hits
hits = searcher.batch_search(queries, queriesIds, K)

# Iterate through them and save the results

writeResults(hits, OUTPUT)
print("Finished")

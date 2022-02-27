import pyterrier as pt
import os
import json

# Use optimal from pyserini github and add extensions! from pyserini
K1 = float(0.82)
B = float(0.68)
K = 1000

pt.init()


def readQueryFile(filename):

    queriesIds = []
    queries = []
    with open(filename, "r") as file_read:
        for line in file_read.readlines():

            frags = line.split("\t")
            queriesIds.append(frags[0].strip())
            queries.append(frags[-1].strip())

    return queriesIds, queries


def write_eval(dictionary, outputFile):
    with open(outputFile, "w") as file_write:
        file_write.write(json.dumps(dictionary, indent=4))


INDEX = "/home/tomas/Escritorio/IR/project/IR/createIndex/passage_index"
OUTPUT = f"../runs/run_{len(os.listdir('../runs'))}.txt"
TOPICS_FILE = "/home/tomas/Escritorio/IR/project/IR/queries/msmarco-test2019-queries.tsv"
QRELS_FILE = "/home/tomas/Escritorio/IR/project/IR/queries/2019qrels-pass.txt"
OUTPUT_EVAL = f"../evals/run_{len(os.listdir('../runs'))}_eval_per_query.json"
OUTPUT_EVAL_GENERAL = f"../evals/run_{len(os.listdir('../runs'))}_eval_general.json"

topics = pt.io.read_topics(TOPICS_FILE, format="singleline")

# topics = readQueryFile(TOPICS_FILE)
qrels = pt.io.read_qrels(QRELS_FILE)
BM25_br = pt.BatchRetrieve(INDEX, wmodel="BM25")
res = BM25_br.transform(topics)
eval_res = pt.Utils.evaluate(res, qrels, metrics=['map', "ndcg", "recip_rank"], perquery=True)
write_eval(eval_res, OUTPUT_EVAL)
eval_res = pt.Utils.evaluate(res, qrels, metrics=['map', "ndcg", "recip_rank"])
write_eval(eval_res, OUTPUT_EVAL_GENERAL)

pt.io.write_results(res, OUTPUT, format='trec', append=False)


# def writeResults(hits, outputFilename):

#     with open(outputFilename, "w") as file_write:
#         for results in hits.items():
#             queryId = results[0].split("\t")[0]

#             i = 0
#             for hit in results[1]:
#                 file_write.write(f'{results[0]}\t{hit.docid}\t{i+1}\n')
#                 i += 1


# queriesIds, queries = readQueryFile(TOPICS)

# # Create the searcher giving it the indexes and the BM parameters
# searcher = SimpleSearcher(INDEX)
# searcher.set_bm25(K1, B)


# # Retrieve all the hits
# hits = searcher.batch_search(queries, queriesIds, K, 10)

# # Iterate through them and save the results

# writeResults(hits, OUTPUT)
# print("Finished")

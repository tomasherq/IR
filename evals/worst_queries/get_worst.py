import json
from collections import defaultdict


params = ['map', 'ndcg', 'recip_rank']
queriesids = []
all_queries_ids = []


def getAverages(data_per_query):
    averages = {'map': 0, 'ndcg': 0, 'recip_rank': 0}
    for values in data_per_query.values():

        averages["map"] += values["map"]
        averages["ndcg"] += values["ndcg"]
        averages["recip_rank"] += values["recip_rank"]

    total_queries = len(data_per_query)

    averages["map"] = averages["map"]/total_queries
    averages["ndcg"] = averages["ndcg"]/total_queries
    averages["recip_rank"] = averages["recip_rank"]/total_queries
    return averages


QUERIES_FILE = "/home/tomas/Escritorio/IR/project/IR/queries/queries.dev.tsv"
COLLECTION_FILE = "/home/tomas/Escritorio/IR/project/code/collectionandqueries/collection/collection.tsv"
ALL_PASSAGES = "all_passages.json"
RUN_EVALUATE = "../run_large.json"


with open(RUN_EVALUATE, "r") as file_read,\
        open(QUERIES_FILE, "r") as queries_read_file,\
        open(COLLECTION_FILE, "r") as file_collection:
    data_per_query = json.load(file_read)

    averages = getAverages(data_per_query)

    data = defaultdict(float)
    for queryid in data_per_query:
        data[queryid] = data_per_query[queryid]["map"]

    worst_results = sorted(data.items(), key=lambda kv: (kv[1], kv[0]))

    index = 0
    for result in worst_results:
        index += 1

        if result[1] < averages["map"]*0.7:
            if result[0] not in queriesids:
                queriesids.append(result[0])
        if result[0] not in all_queries_ids:
            all_queries_ids.append(result[0])
        if index % 10000 == 0:

            with open(f'worst/ids/map_worst_{index/10000}.json', "w") as file_write:
                file_write.write(json.dumps(queriesids, indent=4))
            with open(f'all/ids/all_ids_{index/10000}.json', "w") as file_write:
                file_write.write(json.dumps(all_queries_ids, indent=4))
            print(index)
            all_queries_ids = []
            queriesids = []
with open(f"worst/queries/queries_{index/10000}.json", "w") as queries_worst_write,\
        open(f"worst/passages/passages_{index/10000}.json", "w") as passages_worst_write,\
        , , open(ALL_PASSAGES, "w") as file_all_pass:

    worst_queries = []
    worst_passages = []
    all_passages = []

    content_file = file_read.read()
    content_passage = file_collection.read()
    for querid in queriesids:

        worst_passages.append((querid, content_passage.split(querid)[1].split("\n")[0].strip()))

        worst_queries.append((querid, content_file.split(querid)[1].split("\n")[0].strip()))

    for querid in all_queries_ids:
        all_passages.append((querid, content_passage.split(querid)[1].split("\n")[0].strip()))

    file_write.write(json.dumps(worst_queries, indent=4))
    file_write_pass.write(json.dumps(worst_passages, indent=4))
    file_all_pass.write(json.dumps(all_passages, indent=4))

with open("worst_ids.json", "w") as file_write:
    file_write.write(json.dumps(queriesids, indent=4))

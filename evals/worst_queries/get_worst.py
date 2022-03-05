import json
from collections import defaultdict


params = ['map', 'ndcg', 'recip_rank']
queriesids = []
all_queries_ids = []


with open("../run_12_eval_general.json", "r") as file_read:
    averages = json.load(file_read)

QUERIES_FILE = "/home/tomas/Escritorio/IR/project/IR/queries/msmarco-test2019-queries.tsv"
COLLECTION_FILE = "/home/tomas/Escritorio/IR/project/code/collectionandqueries/collection/collection.tsv"
ALL_PASSAGES = "all_passages.json"


with open("../run_12_eval_per_query.json", "r") as file_read:
    data_per_query = json.load(file_read)

    data = defaultdict(float)
    for queryid in data_per_query:
        data[queryid] = data_per_query[queryid]["map"]

    worst_results = sorted(data.items(), key=lambda kv: (kv[1], kv[0]))

    for result in worst_results:
        if result[1] < averages["map"]*0.7:
            if result[0] not in queriesids:
                queriesids.append(result[0])
        if result[0] not in all_queries_ids:
            all_queries_ids.append(result[0])

        with open(f'map_worst.json', "w") as file_write:

            file_write.write(json.dumps(worst_results, indent=4))

with open("worst_queries.json", "w") as file_write, open("worst_passages.json", "w") as file_write_pass, open(QUERIES_FILE, "r") as file_read, open(COLLECTION_FILE, "r") as file_collection, open(ALL_PASSAGES, "w") as file_all_pass:

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

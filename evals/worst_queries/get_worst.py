import json
from collections import defaultdict


params = ['map', 'ndcg', 'recip_rank']
docs_ids = []

with open("../run_9_eval_general.json", "r") as file_read:
    averages = json.load(file_read)

QUERIES_FILE = "/home/tomas/Escritorio/IR/project/IR/queries/msmarco-test2019-queries.tsv"

with open("../run_9_eval_per_query.json", "r") as file_read:
    data_per_query = json.load(file_read)

    for param in params:
        data = defaultdict(float)
        for queryid in data_per_query:
            data[queryid] = data_per_query[queryid][param]

        worst_results = sorted(data.items(), key=lambda kv: (kv[1], kv[0]))

        for result in worst_results:
            if result[1] < averages[param]:
                if result[0] not in docs_ids:
                    docs_ids.append(result[0])

        with open(f'{param}_worst.json', "w") as file_write:

            file_write.write(json.dumps(worst_results, indent=4))

with open("worst_queries.json", "w") as file_write, open(QUERIES_FILE, "r") as file_read:

    worst_queries = []
    content_file = file_read.read()
    for doc_id in docs_ids:

        worst_queries.append((doc_id, content_file.split(doc_id)[1].split("\n")[0].strip()))

    file_write.write(json.dumps(worst_queries, indent=4))

with open("worst_ids.json", "w") as file_write:
    file_write.write(json.dumps(docs_ids, indent=4))

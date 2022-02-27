from collections import defaultdict
from math import log


FILE_RATING = "/home/tomas/Escritorio/IR/project/IR/queries/2019qrels-pass.txt"
B = 2


def read_rating():
    ratings = defaultdict(lambda: defaultdict(int))
    with open(FILE_RATING, "r") as file_read:

        for line in file_read:
            fragments = line.split(" ")
            queryid = int(fragments[0])
            document = int(fragments[2])
            score = int(fragments[3])

            ratings[queryid][document] = score

    return ratings


def getIdealDCG(ratings_qid, MAX=0):

    values = list(ratings_qid.values())
    values.sort(reverse=True)

    i = 1
    DCG = 0
    for rating in values:
        DCG += rating/log(i+1, B)
        i += 1
        if MAX and MAX <= i:
            break
    return DCG


def compute_ndcg(qids_candidate, all_scores={}):

    MAX = len(list(qids_candidate.values())[0])
    ratings = read_rating()
    count_queries_viewed = 0
    NDCG = 0

    for qid in ratings:

        if qid in qids_candidate:

            count_queries_viewed += 1
            candidate_pid = qids_candidate[qid]
            DCG = 0
            for i in range(0, MAX):
                pid = candidate_pid[i]

                if pid in ratings[qid]:
                    if i > 0:
                        DCG += ratings[qid][pid]/log(i+1, B)
                    else:
                        DCG += ratings[qid][pid]

            NDCG += DCG/getIdealDCG(ratings[qid], MAX)

    if count_queries_viewed == 0:
        count_queries_viewed = 1

    all_scores[f'NDCG @{MAX}'] = NDCG/count_queries_viewed
    return all_scores

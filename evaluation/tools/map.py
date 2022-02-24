import math

e = 2.71828


def compute_map(qids_relevant, qids_candidate, all_scores={}):

    map = 0
    MAX = len(list(qids_candidate.values())[0])

    for qid in qids_candidate:
        if qid in qids_relevant:
            pids_candidate = list(qids_candidate[qid].values())
            pids_reference = qids_relevant[qid]

            total_documents = len(pids_reference)  # R

            ap = 0
            found = 0

            for pid in pids_reference:
                if pid in pids_candidate:
                    rank = pids_candidate.index(pid)+1
                    found += 1
                    ap += found/rank

            map += ap/total_documents

    all_scores[f"MAP @{MAX}"] = map/len(qids_relevant.keys())
    return all_scores


def compute_gmap(qids_relevant, qids_candidate, all_scores={}):

    map = 0
    MAX = len(list(qids_candidate.values())[0])

    for qid in qids_candidate:
        if qid in qids_relevant:
            pids_candidate = list(qids_candidate[qid].values())
            pids_reference = qids_relevant[qid]

            total_documents = len(pids_reference)  # R

            ap = 0
            found = 0

            for pid in pids_reference:
                if pid in pids_candidate:
                    rank = pids_candidate.index(pid)+1
                    found += 1

                    # Does this make any sense?

                    ap += math.log(found/rank, e)

            map += ap/total_documents

    gmap = e**((1/MAX)*map)

    all_scores[f"GMAP @{MAX}"] = gmap
    return all_scores

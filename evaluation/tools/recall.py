

def compute_recall(qids_relevant, qids_candidate, all_scores={}):

    recall = 0
    MAX = len(list(qids_candidate.values())[0])

    for qid in qids_candidate:
        if qid in qids_relevant:
            pids_candidate = list(qids_candidate[qid].values())
            pids_reference = qids_relevant[qid]

            total_documents = len(pids_reference)  # R
            found = 0
            for pid in pids_reference:
                if pid in pids_candidate:
                    found += 1

            recall += found/total_documents

    all_scores[f"RECALL @{MAX}"] = recall/len(qids_relevant.keys())
    return all_scores

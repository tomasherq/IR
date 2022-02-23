

def compute_mp(qids_relevant, qids_candidate, all_scores={}):

    mp = 0
    MAX = len(list(qids_candidate.values())[0])

    for qid in qids_candidate:
        if qid in qids_relevant:
            pids_candidate = list(qids_candidate[qid].values())
            pids_reference = qids_relevant[qid]

            precise_documents = 0
            total_documents = len(pids_reference)

            for pid in pids_reference:
                if pid in pids_candidate:
                    precise_documents += 1
            mp += precise_documents/total_documents

    all_scores[f"MP @{MAX}"] = mp/len(qids_relevant.keys())
    return all_scores

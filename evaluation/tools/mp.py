

def compute_mp(qids_relevant, qids_candidate, all_scores={}):

    mp = 0
    MAX = len(list(qids_candidate.values())[0])

    for qid in qids_candidate:
        if qid in qids_relevant:
            pids_candidate = list(qids_candidate[qid].values())
            pids_reference = qids_relevant[qid]

            precise_documents = 0
            total_documents = len(pids_reference)
            i = 1
            for pid in pids_candidate:
                if pid in pids_reference:
                    precise_documents += 1
                if total_documents == precise_documents:
                    break
                i += 1
            mp += precise_documents/i

    all_scores[f"MP @{MAX}"] = mp/len(qids_relevant.keys())
    return all_scores

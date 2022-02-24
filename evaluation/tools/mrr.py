

def compute_mrr(qids_relevant, qids_candidate, all_scores={}):

    MRR = 0
    MAX_MRR = len(list(qids_candidate.values())[0])

    for qid in qids_candidate:
        if qid in qids_relevant:

            target_pids = qids_relevant[qid]
            candidate_pid = qids_candidate[qid]
            for i in range(0, MAX_MRR):
                if candidate_pid[i] in target_pids:
                    MRR += 1/(i + 1)
                    break

    MRR = MRR/len(qids_relevant)
    all_scores[f'MRR @{MAX_MRR}'] = MRR

    return all_scores

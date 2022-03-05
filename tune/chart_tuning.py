import json
import matplotlib.pyplot as plt
from collections import defaultdict
import statistics

with open("tune_results.json", "r") as file_read:
    results = json.load(file_read)["data"]


values_tune = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
global counter_plots


def get_values_keys(parameter, stat):

    means = []
    keys = []

    for value in values_tune[parameter]:

        means.append(statistics.fmean(values_tune[parameter][value][stat]))
        keys.append(value)

    return keys, means


def plot_values(stat, counter_plots=1, color="blue"):

    first = True

    for parameter in values_tune:
        plt.subplot(3, 3, counter_plots)

        keys, means = get_values_keys(parameter, stat)
        plt.plot(keys, means, marker="o", color=color)
        plt.xticks(keys)

        diff = max(means)-min(means)

        if first:
            plt.ylabel(stat.upper())
            first = False

        if(counter_plots < 4):
            plt.title(f'{parameter} value')

        counter_plots += 1

    return counter_plots


for result in results:

    c = result["tran_0_c"]
    k1 = result["tran_1_bm25.k_1"]
    k3 = result["tran_2_bm25.k_3"]

    map_value = result["map"]
    ndcg_value = result["ndcg"]
    rr_value = result["recip_rank"]

    values_tune["c"][c]["map"].append(map_value)
    values_tune["c"][c]["ndcg"].append(ndcg_value)
    values_tune["c"][c]["mrr"].append(rr_value)

    values_tune["k1"][k1]["map"].append(map_value)
    values_tune["k1"][k1]["ndcg"].append(ndcg_value)
    values_tune["k1"][k1]["mrr"].append(rr_value)

    values_tune["k2"][k3]["map"].append(map_value)
    values_tune["k2"][k3]["ndcg"].append(ndcg_value)
    values_tune["k2"][k3]["mrr"].append(rr_value)


# Plots for MAP


plt.rc('axes', labelsize=22)  # fontsize of the x and y labels
plt.rc('axes', titlesize=22)  # fontsize of the title
plt.rc('xtick', labelsize=12)  # fontsize of the x tick labels
plt.rc('ytick', labelsize=12)  # fontsize of the y tick labels
plot_counter = plot_values("map", 1)


# Plots for ndcg
plot_counter = plot_values("ndcg", 4, "orange")

plot_values("mrr", plot_counter, "green")


plt.show()

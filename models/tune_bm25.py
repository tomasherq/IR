from models.common import *


BM25 = pt.BatchRetrieve(INDEX, wmodel="BM25", controls={"c": 0.75, "bm25.k_1": 0.75, "bm25.k_3": 0.75})
rtr = pt.GridSearch(BM25, {BM25: {"c": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                                  "bm25.k_1": [0.3, 0.6, 0.9, 1.2, 1.4, 1.6, 2],
                                  "bm25.k_3": [0.5, 2, 4, 6, 8, 10, 12, 14, 20]
                                  }},
                    topics,
                    qrels,
                    "map")

# using rc function
plt.rc('font', size=20)  # controls default text size
plt.rc('axes', titlesize=40)  # fontsize of the title
plt.rc('axes', labelsize=30)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=25)  # fontsize of the x tick labels
plt.rc('ytick', labelsize=25)  # fontsize of the y tick labels
plt.rc('legend', fontsize=20)  # fontsize of the legend

plt.plot(rtr["tran_0_c"], rtr["map"])
plt.xlabel("BM25's b value")
plt.ylabel("MAP")
plt.legend()

plt.show()

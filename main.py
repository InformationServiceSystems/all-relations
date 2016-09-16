'''
parses and plots wiki dataset
@author: iaroslav
'''

import pandas as ps
from backend import relations as rbc
from backend import fitter as fx
from backend import parser as drd

import pickle
import os
import numpy as np

if __name__ == "__main__":
    ### SETTINGS ###

    dataset_csv = "datasets/wiki.csv" # see wiki.csv to understand format used
    results_folder = "results" # this folder should exist
    model_classes = [fx.KNN_approximator, fx.SVR_approximator, fx.AdaBoost_approximator] # fx.ANN_approximator - use if TensorFlow is installed

    ### CODE STARTS HERE ###

    dataset_name = os.path.basename(dataset_csv)[:-4] # remove the .csv at the end of dataset name

    # compute the IRGs
    for model_class in model_classes:

        fname = dataset_name + "_" + model_class

        results_bin = os.path.join(results_folder, fname + ".bin")
        results_csv = os.path.join(results_folder, fname + ".csv")

        # establish relationships if not given
        if not os.path.exists(results_bin):
            rlt = rbc.Extract_1_to_1_Relations(drd.read_dataset(dataset_csv), model_class)

            # store results_paper in a .bin file
            with open(results_bin, 'wb') as handle:
                pickle.dump(rlt, handle)

        # load computed results_paper
        with open(results_bin, 'rb') as handle:
            rlt = pickle.load(handle)

        # 2d array representing csv table
        names = rlt.keys()
        header = [[""] + names]
        rows = header + [[A] + ["%.2f" % rlt[A][B] if not rlt[A][B] is None else "" for B in names] for A in names]

        # convert csv array to string
        csv_result = "\n".join([",".join(row) for row in rows])

        # save the csv
        with open(results_csv, "w") as f:
            f.write(csv_result)

        print csv_result

    # compute the average over IRGs for different classes for all relations
    all_relations = {}

    for model_class in model_classes:

        fname = dataset_name + "_" + model_class
        results_bin = os.path.join(results_folder, fname + ".bin")

        with open(results_bin, 'rb') as handle:
            rlt = pickle.load(handle)

        for A in rlt.keys():
            for B in rlt.keys():
                # relation go from A to B with weight W
                if A == B:
                    continue

                W = rlt[A][B]

                key = A + "->" + B
                if not key in all_relations:
                    all_relations[key] = []

                all_relations[key].append(W)

    # compute average IRG over different predictive classes for relations
    all_relations = [{'relation': key, 'IRG': np.mean(all_relations[key])} for key in all_relations]
    all_relations.sort(key= lambda value: value['IRG'], reverse=True)

    ranking = "\n".join([value['relation'] + "," + str(value['IRG']) for value in all_relations])

    # save the csv
    ranking_csv = os.path.join(results_folder, dataset_name + "_ranking.csv")

    with open(ranking_csv, "w") as f:
        f.write(ranking)

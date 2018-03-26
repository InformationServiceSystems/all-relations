import numpy as np
import pandas as ps

from backend.skapi import pandas_to_concepts, all_1_to_1, all_n_to_1
from datasets import read_gender_discrimination_dataset, read_utaut

data = read_gender_discrimination_dataset()
concepts = pandas_to_concepts(data)

#relations = all_n_to_1(concepts)
relations = all_1_to_1(concepts)

import os
import json

json.dump(
    relations,
    open(os.path.join('results', 'result.json'), 'w'),
    indent=2,
)

from pprint import pprint
relations.sort(reverse=True, key=lambda x: x[-1])
pprint(relations)
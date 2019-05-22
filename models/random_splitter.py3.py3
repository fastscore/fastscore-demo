# fastscore.schema.0: double
# fastscore.schema.1: double
# fastscore.schema.3: double

import numpy as np

def action(datum):
    x = np.random.rand()
    if x > 0.2:
        yield (1, datum)
    else:
        yield (3, datum)

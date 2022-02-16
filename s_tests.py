import some_funcs as sf
import numpy as np


a = np.arange(9).reshape(3,3)

for r in a:
    b = r[[1,2]]
    print(b)
    # c = [4, 5] == b
    # print(all(c))





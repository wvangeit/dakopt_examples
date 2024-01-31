import math
import numpy as np
import pathlib as pl

import dakota.environment as dakenv


def sinc(x=0.0, a=math.pi):
    x = np.atleast_1d(x)
    anx = a * np.linalg.norm(x)
    if anx == 0.0:
        y = 1.0
    else:
        y = math.sin(anx) / anx

    print(f"Evaluated: {x}, output: {y}")

    return [y]


def map_sinc_function(dak_inputs):
    param_sets = [dak_input["cv"] for dak_input in dak_inputs]

    obj_sets = list(map(sinc, param_sets))

    dak_outputs = [{"fns": obj_set} for obj_set in obj_sets]

    return dak_outputs


def main():
    callbacks = {"map": map_sinc_function}

    opt_in_path = pl.Path("opt.in")
    opt_in = opt_in_path.read_text()

    study = dakenv.study(callbacks=callbacks, input_string=opt_in)

    study.execute()


if __name__ == "__main__":
    main()

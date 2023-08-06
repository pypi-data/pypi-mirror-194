from tqdm import tqdm
import multiprocessing
from joblib import Parallel, delayed


def x_on_iter(llist, calc_func, clear_nones=False, n_jobs=-1):
    if n_jobs == 1:
        all_items = [calc_func(i) for i in tqdm(llist, total=len(llist))]

    else:
        all_items = Parallel(n_jobs=n_jobs)(delayed(calc_func)(i) for i in x_tqdm(llist, total=len(llist), n_jobs=n_jobs))

    if clear_nones:
        all_items = [i for i in all_items if i is not None]

    return all_items


def x_on_keys(ddict, keys, func, n_jobs=-1):
    all_keys = list(keys)
    all_vals = Parallel(n_jobs=n_jobs)(delayed(func)(ddict[k]) for k in x_tqdm(all_keys, total=len(all_keys)))
    new_dict = dict(zip(all_keys, all_vals))
    return new_dict


def x_reduce(llist, calc_func, reduce_func=max, n_jobs=-1):
    vals = x_on_iter(llist, calc_func, n_jobs=n_jobs)
    vals = [v for v in vals if v is not None]
    val = reduce_func(vals)
    return val


class x_tqdm(tqdm):
    """
    tqdm that handles parallel jobs better
    """

    def __init__(self, *args, n_jobs=1, **kwargs):
        if n_jobs == -1:
            n_jobs = multiprocessing.cpu_count()

        self.n_jobs = n_jobs
        super().__init__(*args, **kwargs)

    def update(self, n=1):
        super().update(max(n-self.n_jobs, 0))

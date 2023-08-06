from __future__ import print_function
import inspect

import numpy as np
import scipy.stats as stats
import pandas as pd

import loter.pipeline as lt
import loter.initparam as initparam
import loter.initdata as initdata
import loter.opti as opti
import loter.estimatea as esta
import loter.estimateh as esth
import loter.graph as ests

##################################################################
#                                                                #
# Pipeline to optimize H (admixed haplotypes) and S (selection)  #
# given A (ancestral haplotypes) simultaneously                  #
#                                                                #
# Initialization:                                                #
# - init A with ancestral haplotypes                             #
#                                                                #
# Optimization:                                                  #
# - join optimisation of H and S                                 #
#                                                                #
# Computational Complexity:                                      #
# - n, the number of ancestral individuals                       #
# - m, the number of SNPs                                        #
# complexity -> O(n^2 * m)                                       #
#                                                                #
# Remarks:                                                       #
# In practice the pipeline is use as a phase corrector module    #
##################################################################

def init_fix_a(data, param):
    def init_a_fix(A, G):
        return param["A_in"]
    return initdata.init_data(data, init_a_fix, initdata.init_h_rand)

def opti_A_fix_join(data, param):
    data, param = ests.optimize_SHknn(data, param)
    data, param = esth.optimize_H_old(data, param)

    return data, param

fixa_pip_A_join = lt.Pipeline(
    initparam.param_initializers["classic_init"],
    init_fix_a,
    opti_A_fix_join,
)

##################################################################
#                                                                #
# Pipeline to optimize S (selection) given A                     #
# (ancestral haplotypes) and H (admixed haplotypes)              #
#                                                                #
# Initialization:                                                #
# - init A with ancestral haplotypes                             #
# - init H with admixed haplotypes                               #
#                                                                #
# Optimization:                                                  #
# - optimisation of S                                            #
#                                                                #
# Computational Complexity:                                      #
# - n, the number of ancestral individuals                       #
# - m, the number of SNPs                                        #
# complexity -> O(n * m)                                         #
#                                                                #
##################################################################

def init_fix_ah(data, param):
    def init_a_fix(A, G):
        return param["A_in"]
    def init_h_fix(H, G):
        return param["H_in"]
    return initdata.init_data(data, init_a_fix, init_h_fix)

def opti_AH_fix_knn(data, param):
    data["A"] = data["A"].astype(np.uint8)
    data["S"] = data["S"].astype(np.uint32)
    data, param = ests.optimize_Sknn(data, param)
    return data, param

def init_fix_ah_custom(data, param):
    def init_a_fix(A, G):
        return param["A_in"]
    def init_h_fix(H, G):
        return param["H_in"]

    data["anc_pop_id"] = param["anc_pop_id"]

    # trick 1 to pass lambda_ratio without modifying parameter class
    data["lambda_ratio"] = param["lambd_ratio"]

    return initdata.init_data(data, init_a_fix, init_h_fix)

def opti_AH_fix_knn_custom(data, param):

    data["A"] = data["A"].astype(np.uint8)
    data["S"] = data["S"].astype(np.uint32)
    data["anc_pop_id"] = data["anc_pop_id"].astype(np.uint32)

    # trick 2 to pass lambda_ratio without modifying parameter class
    param["lambda_ratio"] = data["lambda_ratio"]

    data, param = ests.optimize_Sknn_custom(data, param)

    return data, param

def init_fix_ah_custom2(data, param):
    def init_a_fix(A, G):
        return param["A_in"]
    def init_h_fix(H, G):
        return param["H_in"]

    data["anc_pop_id"] = param["anc_pop_id"]

    # trick 1 to pass lambda_ratio without modifying parameter class
    data["lambda_ratio"] = param["lambd_ratio"]
    data["mu"] = param["mu"]

    return initdata.init_data(data, init_a_fix, init_h_fix)

def opti_AH_fix_knn_custom2(data, param):

    data["A"] = data["A"].astype(np.uint8)
    data["S"] = data["S"].astype(np.uint32)
    data["anc_pop_id"] = data["anc_pop_id"].astype(np.uint32)

    # trick 2 to pass lambda_ratio without modifying parameter class
    param["lambda_ratio"] = data["lambda_ratio"]
    param["mu"] = data["mu"]

    data, param = ests.optimize_Sknn_custom2(data, param)

    return data, param

fixa_pip_AH_knn = lt.Pipeline(
    initparam.param_initializers["classic_init"],
    init_fix_ah,
    opti_AH_fix_knn
)

fixa_pip_AH_knn_custom = lt.Pipeline(
    initparam.param_initializers["classic_init"],
    init_fix_ah_custom,
    opti_AH_fix_knn_custom
)

fixa_pip_AH_knn_custom2 = lt.Pipeline(
    initparam.param_initializers["classic_init"],
    init_fix_ah_custom2,
    opti_AH_fix_knn_custom2
)

def learn_Sknn(pop, A_in, H_in, weights, anc_pop_id=None,
               penalty=40, lambd_ratio=1, mu=None, num_threads=10):
    G_pop = pop["G"]
    H_pop = H_in

    if mu is not None and lambd_ratio is not None:
        l_res_mix = fixa_pip_AH_knn_custom2(G_pop,
                                           nb_iter=1, nbclust=len(A_in), penalty=penalty,
                                           num_threads=num_threads,
                                           weights=weights,
                                           A_in=A_in,
                                           H_in=H_pop,
                                           anc_pop_id=anc_pop_id,
                                           lambd_ratio=lambd_ratio,
                                           mu=mu
        )
    elif lambd_ratio is not None:
        l_res_mix = fixa_pip_AH_knn_custom(G_pop,
                                           nb_iter=1, nbclust=len(A_in), penalty=penalty,
                                           num_threads=num_threads,
                                           weights=weights,
                                           A_in=A_in,
                                           H_in=H_pop,
                                           anc_pop_id=anc_pop_id,
                                           lambd_ratio=lambd_ratio
        )
    else:
        l_res_mix = fixa_pip_AH_knn(G_pop,
                                    nb_iter=1, nbclust=len(A_in), penalty=penalty,
                                    num_threads=num_threads,
                                    weights=weights,
                                    A_in=A_in,
                                    H_in=H_pop
        )

    return l_res_mix[0]["S"]

def learn_S_join(pop, A_in, penalty=40, small_penalty=0, num_threads=10):
    G_pop = pop["G"]

    l_res_mix = fixa_pip_A_join(G_pop,
                                nb_iter=1, nbclust=len(A_in), penalty=penalty,
                                A_in=A_in,
                                small_penalty=small_penalty,
                                num_threads=num_threads
    )

    return l_res_mix[0]["S"], l_res_mix[0]["H"]

def get_items(dict_object):
    """
    Compatible Python 2 et 3 get item for dictionnary
    """
    for key in dict_object:
        yield key, dict_object[key]

def clusters_to_list_pop(S, l_k):
    """
    From a selection matrix S, compute the origin of each SNP.

    input:
    S -- matrix where we are copying
    l_k -- populations sizes
    """
    res = np.copy(S)

    a = np.repeat(np.arange(len(l_k)), l_k)
    b = np.arange(sum(l_k))
    d = {k: v for v, k in zip(a, b)}
    for k, v in get_items(d): res[S==k] = v
    return res

def locanc_g_knn(l_h, g_adm, penalty=40, small_penalty=0, num_threads=10):
    A_in = np.ascontiguousarray(np.vstack(l_h))
    S_adm, H = learn_S_join({"G": g_adm}, A_in, penalty, small_penalty, num_threads)
    result = clusters_to_list_pop(S_adm, [len(A) for A in l_h])

    return result, S_adm, H

def locanc_h_knn(l_h, h_adm, penalty=40, lambd_ratio=1, mu=None, num_threads=10):
    A_in = np.ascontiguousarray(np.vstack(l_h))
    g_adm = h_adm[::2] + h_adm[1::2]
    n, m = h_adm.shape
    weights = np.ones(m)

    anc_pop_size = [len(A) for A in l_h]
    anc_pop_id = np.repeat(np.arange(len(anc_pop_size)), anc_pop_size)

    S_adm = learn_Sknn({"G": g_adm, "H": h_adm}, A_in, h_adm,
                       weights, anc_pop_id, penalty, lambd_ratio, mu, num_threads)
    result = clusters_to_list_pop(S_adm, anc_pop_size)

    return result, S_adm

def update_counts(counts, arr, k=2):
    for p in range(k):
        counts[p,:,:][arr == p] += 1
    return counts

def mode(counts):
    argmax = np.argmax(counts, axis=0)
    return argmax, argmax.choose(counts)

def encode_haplo(H):
    H1, H2 = H[::2], H[1::2]
    return ((np.maximum(H1, H2) * (np.maximum(H1, H2) + 1)) / 2) + np.minimum(H1, H2)

def loter_multiple_pops(l_H, h_adm, lambd, lambd_ratio=None, mu=None,
                        num_threads=10, verbosity=False):
    """
    Local ancestry inference.

    Args:
        l_H (list of np.array): list of matrices of ancestral individual
            haplotypes from different populations (one matrix of dimension
            `2n_pop x n_snp` per ancestral population, where `n_pop` is the
            size of the population and `n_snp` the number of SNPs).
        h_adm (np.array): matrix of admixed individual haplotypes of
            dimension `2n x n_snp`.
        lambd (float): positive real value, penalty parameter. Default
            value is 1.
        lambda_ratio (float): positive real value. Default is None.
            If not None, two different lambdas (`lambda_inter` and
            `lambda_intra`) are used in the inference algorithm, to allow
            different penalization for intra and inter ancetral population
            switch. In this case, `lambda_inter` is given by `range_lambda`
            and `lambda_intra = lambda_inter * lambda_ratio`.
        mu (float): positive real value. Default is None. If not None, the
            local ancestry inference algorithm includes a phase error
            correction penalization term where `mu` is the penalty parameter.
        threshold (float): real value in [0,1], threshold for the phase
            correction module. Default value is 0.9.
        rate_vote (float): real value in [0,1], threshold for vote
            in bagging. Default value is 0.5.
        nb_bagging (int): positive integer value, number of sub-sampling in
            bagging. Default value is 20.
        nb_threads (int): positive integer, number of threads to use. If =1
            (default value), a single thread is use. If >1, on OpenMP
            compatible system, computations are parallelized.
        verbosity (bool): enable/disable versbosity. Default is False.

    Returns:
        Matrix (np.array) of infered ancestral population id for each SNPs
        and each admixed haplotype (dimension `2n x n_snp`).
    """
    if verbosity:
        print("# Run simple local ancestry inference")
        print("# Input:")
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for i in args: print("## {} = {}".format(i, values[i]))
    res_loter, _ = locanc_h_knn([h.astype(np.uint8) for h in l_H],
                               h_adm.astype(np.uint8),
                               lambd, lambd_ratio, mu, num_threads)
    return res_loter

def boostrap_loter_multiple_pops(l_H, h_adm, lambd, lambd_ratio, mu,
                                 counts, nbrun=20, num_threads=10,
                                 verbosity=False):

    if verbosity:
        print("# Bootstrap local ancestry inference")
        print("# Input:")
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for i in args: print("## {} = {}".format(i, values[i]))

    def shuffle(H):
        n, m = H.shape
        return H[np.random.randint(n, size=n), :]

    if nbrun > 1:
        if verbosity: print("## Multiple run")
        for i in range(nbrun):
            shuffled_H = [shuffle(h) for h in l_H]
            counts = update_counts(counts,
                                   loter_multiple_pops(shuffled_H,
                                                       h_adm,
                                                       lambd,
                                                       lambd_ratio,
                                                       mu,
                                                       num_threads,
                                                       verbosity=False),
                                   len(l_H)
            )
    else:
        if verbosity: print("## Single run")
        counts = update_counts(counts,
                               loter_multiple_pops(l_H,
                                                   h_adm,
                                                   lambd,
                                                   lambd_ratio,
                                                   mu,
                                                   num_threads,
                                                   verbosity=False),
                               len(l_H)
        )

    return counts

def loter_local_ancestry(l_H, h_adm, range_lambda=np.arange(1.5, 5.5, 0.5),
                         lambda_ratio=None, mu=None,
                         rate_vote=0.5, nb_bagging=20,
                         num_threads=10, verbosity=False):
    """
    Local ancestry inference with bagging.

    Args:
        l_H (list of np.array): list of matrices of ancestral individual
            haplotypes from different populations (one matrix of dimension
            `2n_pop x n_snp` per ancestral population, where `n_pop` is the
            size of the population and `n_snp` the number of SNPs).
        h_adm (np.array): matrix of admixed individual haplotypes of
            dimension `2n x n_snp`.
        range_lambda (np.array): vector of (positive real) candidates values
            for the penalty parameter. Default value is
            {1.5,2,2.5,3,3.5,4,4.5,5,5.5}.
        lambda_ratio (float or np.array): positive single value or vector of
            positive real value. Default is None. If not None,
            two different lambdas (`lambda_inter`
            and `lambda_intra`) are used in the inference algorithm,
            to allow different penalization for intra and inter ancetral
            population switch. In this case, `lambda_inter` is given by
            `range_lambda` and `lambda_intra = lambda_inter * lambda_ratio`.
            If `lambda_ratio` is a vector, the different values will be tested
            in the bagging algorithm.
        mu (float or np.array): single positive real value or vector of
            positive real values. Default is None. If not None, the
            local ancestry inference algorithm includes a phase error
            correction penalization term where `mu` is the penalty parameter.
            If `mu` is a vector, the different values will be tested
            in the bagging algorithm.
        rate_vote (float): real value in [0,1], threshold for vote
            in bagging. Default value is 0.5.
        nb_bagging (int): positive integer value, number of sub-sampling in
            bagging. Default value is 20.
        nb_threads (int): positive integer, number of threads to use. If =1
            (default value), a single thread is use. If >1, on OpenMP
            compatible system, computations are parallelized.
        verbosity (bool): enable/disable versbosity. Default is False.

    Returns:
        r (np.array): matrix of infered genotype for each SNPs and each
            admixed haplotype (dimension `n x n_snp`).
        res_loter (tuple): result from boostrap, tuple of two matrices
            (np.array of dimension `2n x n_snp`), first is the matrix of
            ancestral population that was chosen by most of
            boostrap repetitions for each admixed haplotype and each SNP,
            second is the corresponding number of bootstrap repetitions that
            chose it.
    """
    if verbosity:
        print("# Run local ancestry inference (with bagging)")
        print("# Input:")
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for i in args: print("## {} = {}".format(i, values[i]))
    input_loter = (l_H, h_adm)
    n, m = h_adm.shape
    counts = np.zeros((len(l_H), n, m))
    if not isinstance(range_lambda, np.ndarray):
        if isinstance(range_lambda, list) or isinstance(range_lambda, tuple):
            range_lambda = np.array(range_lambda)
        else:
            range_lambda = np.array([range_lambda])
    if not isinstance(lambda_ratio, np.ndarray):
        if isinstance(lambda_ratio, list) or isinstance(lambda_ratio, tuple):
            lambda_ratio = np.array(lambda_ratio)
        else:
            lambda_ratio = np.array([lambda_ratio])
    if not isinstance(mu, np.ndarray):
        if isinstance(mu, list) or isinstance(mu, tuple):
            mu = np.array(mu)
        else:
            mu = np.array([mu])
    for l, lr, m in np.dstack(np.meshgrid(range_lambda, lambda_ratio, mu)).reshape(-1, 3):
        res_boostrap = boostrap_loter_multiple_pops(*input_loter, lambd=l,
                                                    lambd_ratio=lr, mu=m,
                                                    counts=counts, nbrun=nb_bagging,
                                                    num_threads=num_threads,
                                                    verbosity=False)
    res_loter = mode(counts)
    r = vote_and_impute(res_loter, rate_vote)
    return r, res_loter

def diploid_sim(cluster_found, cluster_truth):
    (n,m) = cluster_found.shape
    return np.count_nonzero(cluster_found == cluster_truth) / float(n*m)

def find_lambda(s_in, threshold = 0.90, min_lambda = 1,
                max_lambda = 500, num_threads=10):
    n, m = s_in.shape
    if max_lambda - min_lambda <= 1:
        return locanc_g_knn([np.zeros((1,m)), np.ones((1,m))],
                            s_in, min_lambda, min_lambda, num_threads)
    else:
        mean = (max_lambda - min_lambda) / 2 + min_lambda
        r_g, s_g, h_g = locanc_g_knn([np.zeros((1,m)), np.ones((1,m))],
                                     s_in, mean, mean, num_threads)
        sim = diploid_sim(r_g[::2] + r_g[1::2], s_in)
        if sim > threshold:
            return find_lambda(s_in, threshold, min_lambda = (max_lambda - min_lambda) / 2 + min_lambda,
                               max_lambda = max_lambda, num_threads=num_threads)
        else:
            return find_lambda(s_in, threshold, min_lambda = min_lambda,
                               max_lambda = max_lambda  - ((max_lambda - min_lambda) / 2),
                               num_threads=num_threads)

def vote_and_impute(s, percent_threshold=0.5):
    def select_val(s, percent_threshold):
        max_s, min_s = np.max(s[1]), np.min(s[1])
        threshold = percent_threshold*(max_s - min_s) + min_s
        select = np.logical_and(s[1][::2] >= threshold,
                                s[1][1::2] >= threshold)
        arr = encode_haplo(s[0])
        arr[np.logical_not(select)] = 255
        return arr

    arr = select_val(s, percent_threshold)

    n, m = arr.shape
    res = np.copy(arr)

    for i in range(n):
        serie = pd.Series(arr[i])
        serie.loc[serie == 255] = np.nan
        try:
            res[i] = serie.dropna().reindex(range(m), method='nearest').values
        except:
            res[i] = arr[i]

    return res

def loter_smooth(l_H, h_adm, range_lambda=np.arange(1.5, 5.5, 0.5),
                 lambda_ratio=None, threshold=0.90, rate_vote=0.5,
                 nb_bagging=20, num_threads=10,
                 verbosity=False):
    """
    Local ancestry inference with bagging and phase correction.

    Args:
        l_H (list of np.array): list of matrices of ancestral individual
            haplotypes from different populations (one matrix of dimension
            `2n_pop x n_snp` per ancestral population, where `n_pop` is the
            size of the population and `n_snp` the number of SNPs).
        h_adm (np.array): matrix of admixed individual haplotypes of
            dimension `2n x n_snp`.
        range_lambda (np.array): vector of (positive real) candidates values
            for the penalty parameter. Default value is
            {1.5,2,2.5,3,3.5,4,4.5,5,5.5}.
        lambda_ratio (float or np.array): single value or vector of real value.
            Default is None. If not None, two different lambdas (`lambda_inter`
            and `lambda_intra`) are used in the inference algorithm,
            to allow different penalization for intra and inter ancetral
            population switch. In this case, `lambda_inter` is given by
            `range_lambda` and `lambda_intra = lambda_inter * lambda_ratio`.
            If `lambda_ratio` is a vector, the different values will be tested
            in the bagging algorithm.
        threshold (float): real value in [0,1], threshold for the phase
            correction module. Default value is 0.9.
        rate_vote (float): real value in [0,1], threshold for vote
            in bagging. Default value is 0.5.
        nb_bagging (int): positive integer value, number of sub-sampling in
            bagging. Default value is 20.
        nb_threads (int): positive integer, number of threads to use. If =1
            (default value), a single thread is use. If >1, on OpenMP
            compatible system, computations are parallelized.
        verbosity (bool): enable/disable versbosity. Default is False.

    Returns:
        Matrix (np.array) of infered ancestral population id for each SNPs
        and each admixed haplotype (dimension `2n x n_snp`).
    """
    if verbosity:
        print("# Running local ancestry inference")
        print("# Input:")
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        for i in args: print("## {} = {}".format(i, values[i]))

    if verbosity: print("## Step 1: local ancestry inference (with bagging)")
    res_impute, res_raw = loter_local_ancestry(
                                l_H=l_H, h_adm=h_adm, range_lambda=range_lambda,
                                lambda_ratio=lambda_ratio, mu=None,
                                rate_vote=rate_vote, nb_bagging=nb_bagging,
                                num_threads=num_threads,
                                verbosity=False)
    result = np.copy(res_impute)
    result_hap = []
    if verbosity: print("## Step 2: phase correction")
    for i in range(len(res_impute)):
        arr_input = np.ascontiguousarray(np.array([res_impute[i]])).astype(np.uint8)
        r, _, _ = find_lambda(arr_input, threshold=threshold, num_threads=num_threads)
        result_hap.append(r)
        result[i] = r[::2] + r[1::2]

    return np.vstack(result_hap)

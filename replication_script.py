"""
Replication script for "Quantifying Realism in Urban Simulation: An AHP-Based
Framework for Model Selection and Evaluation".

Author: Babak Mahdavi Ardestani
E-mail: babak.mahdavi@mail.mcgill.ca

Conventions used :
  - The model order is always Bruch & Mare, Fossett, Crooks, Benenson et al., Mahdavi Ardestani et al.
  - Dimension keys: M = Generative Mechanisms, S = Spatial Representation,
    D = Empirical Data Integration, V = Empirical Validation,  W = dimension importance.

Requirements: Python 3.8+, numpy, scipy.
Run with: python replication_script.py

"""

import random

import numpy as np
import scipy.stats as stats

SEED = 20261005      

NAMES = ["Bruch & Mare", "Fossett", "Crooks", "Benenson et al.", "Mahdavi Ardestani et al."]
DIMS = ["M", "S", "D", "V"]

# Saaty scales
SCALE = [1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Saaty's Random Index values
RI = {4: 0.90, 5: 1.12}

# -------------------------
# AHP functions
# ------------------------
def priorities(matrix):
    g = np.prod(matrix, axis=1) ** (1 / len(matrix))
    return g / g.sum()


def consistency_ratio(matrix):
    n = len(matrix)
    w = priorities(matrix)
    lam = np.mean(matrix @ w / w)
    return ((lam - n) / (n - 1)) / RI[n]


def aij(*matrices):
    return np.prod(matrices, axis=0) ** (1 / len(matrices))


def global_scores(mats):
    w = priorities(mats["W"])
    return sum(priorities(mats[k]) * w[i] for i, k in enumerate(DIMS))


def perturb_matrix(matrix):
    n = len(matrix)
    new = np.ones((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            idx = int(np.abs(np.array(SCALE) - matrix[i, j]).argmin())
            idx = max(0, min(len(SCALE) - 1, idx + random.choice([-1, 0, 1])))
            new[i, j] = SCALE[idx]
            new[j, i] = 1 / SCALE[idx]      
    return new


def table(rows, header):
    print(" | ".join(f"{h:<24}" if i == 0 else f"{h:>8}" for i, h in enumerate(header)))
    for r in rows:
        print(" | ".join(f"{c:<24}" if i == 0 else f"{c:>8}" for i, c in enumerate(r)))
    print()


# -------------------------------
# Pairwise comparison matrices 
# -------------------------------
BASELINE = { 
    'M': np.array([[1, 1/4, 4, 1/4, 1/4], [4, 1, 5, 2, 2], [1/4, 1/5, 1, 1/5, 1/5], [4, 1/2, 5, 1, 2], [4, 1/2, 5, 1/2, 1]]),
    'S': np.array([[1, 1/3, 1/8, 1/9, 1/5], [3, 1, 1/5, 1/7, 1/4], [8, 5, 1, 1/2, 3], [9, 7, 2, 1, 3], [5, 4, 1/3, 1/3, 1]]),
    'D': np.array([[1, 1, 1/4, 1/5, 1/4], [1, 1, 1/3, 1/5, 1/5], [4, 3, 1, 1/4, 1/3], [5, 5, 4, 1, 2], [4, 5, 3, 1/2, 1]]),
    'V': np.array([[1, 1, 1, 1/5, 1/4], [1, 1, 1, 1/5, 1/5], [1, 1, 1, 1/5, 1/5], [5, 5, 5, 1, 1], [4, 5, 5, 1, 1]]),
}

ASSESSORS = { 
    1: {
        'M': np.array([[1, 1/3, 2, 1/3, 1], [3, 1, 3, 1, 3], [1/2, 1/3, 1, 1/3, 1/2], [3, 1, 3, 1, 3], [1, 1/3, 2, 1/3, 1]]),
        'S': np.array([[1, 1, 1/2, 1/9, 1/7], [1, 1, 1/2, 1/7, 1/7], [2, 2, 1, 1/3, 1/5], [9, 7, 3, 1, 1], [7, 7, 5, 1, 1]]),
        'D': np.array([[1, 3, 3, 1/3, 1/3], [1/3, 1, 2, 1/5, 1/5], [1/3, 1/2, 1, 1/5, 1/5], [3, 5, 5, 1, 1], [3, 5, 5, 1, 1]]),
        'V': np.array([[1, 1, 3, 1/3, 1/5], [1, 1, 3, 1/3, 1/5], [1/3, 1/3, 1, 1/5, 1/7], [3, 3, 5, 1, 1/2], [5, 5, 7, 2, 1]]),
        'W': np.array([[1, 3, 3, 1/2], [1/3, 1, 1, 1/3], [1/3, 1, 1, 1/3], [2, 3, 3, 1]]),
    },
    2: {
        'M': np.array([[1, 1/7, 4, 1/5, 1/7], [7, 1, 7, 2, 1], [1/4, 1/7, 1, 1/7, 1/7], [5, 1/2, 7, 1, 1/3], [7, 1, 7, 3, 1]]),
        'S': np.array([[1, 1/2, 1/5, 1/9, 1/9], [2, 1, 1/4, 1/7, 1/7], [5, 4, 1, 1/5, 1/5], [9, 7, 5, 1, 1], [9, 7, 5, 1, 1]]),
        'D': np.array([[1, 3, 3, 1/5, 1/7], [1/3, 1, 2, 1/7, 1/9], [1/3, 1/2, 1, 1/9, 1/9], [5, 7, 9, 1, 1/4], [7, 9, 9, 4, 1]]),
        'V': np.array([[1, 1/3, 3, 1/7, 1/9], [3, 1, 5, 1/5, 1/7], [1/3, 1/5, 1, 1/7, 1/9], [7, 5, 7, 1, 1/6], [9, 7, 9, 6, 1]]),
        'W': np.array([[1, 5, 4, 1], [1/5, 1, 1/3, 1/5], [1/4, 3, 1, 1/4], [1, 5, 4, 1]]),
    },
    3: {
        'M': np.array([[1, 1/7, 3, 1, 1/3], [7, 1, 7, 3, 5], [1/3, 1/7, 1, 1/4, 1/3], [1, 1/3, 4, 1, 1], [3, 1/5, 3, 1, 1]]),
        'S': np.array([[1, 1/2, 1/5, 1/6, 1/7], [2, 1, 1/4, 1/4, 1/4], [5, 4, 1, 2, 1/3], [6, 4, 1/2, 1, 1], [7, 4, 3, 1, 1]]),
        'D': np.array([[1, 3, 5, 3, 1], [1/3, 1, 1, 1, 1/5], [1/5, 1, 1, 1/3, 1/8], [1/3, 1, 3, 1, 1/4], [1, 5, 8, 4, 1]]),
        'V': np.array([[1, 2, 5, 1, 1/3], [1/2, 1, 3, 1/4, 1/7], [1/5, 1/3, 1, 1/4, 1/8], [1, 4, 4, 1, 1/3], [3, 7, 8, 3, 1]]),
        'W': np.array([[1, 1, 4, 1], [1, 1, 4, 1], [1/4, 1/4, 1, 1/3], [1, 1, 3, 1]]),
    },
}

BASELINE["W"] = np.ones((4, 4))
PANEL = list(ASSESSORS.values())


if __name__ == "__main__":
    # -----------------------------------
    print("=== LOCAL PRIORITIES (columns: M, S, D, V; rows follow the model order above) ===")
    _agg = {k: aij(*[m[k] for m in PANEL]) for k in DIMS}
    for label, mats in [("Baseline", BASELINE)] + [(f"Assessor {a}", m) for a, m in ASSESSORS.items()] + [("Panel AIJ", _agg)]:
        print(label)
        for i, n in enumerate(NAMES):
            print(f"  {n:<26}" + "  ".join(f"{priorities(mats[k])[i]:.3f}" for k in DIMS))
    print()

    # -------------------------
    print("=== TABLE 2: baseline global priorities (equal weights) ===")
    loc = {k: priorities(BASELINE[k]) for k in DIMS}
    tot = global_scores(BASELINE)
    rows = [[NAMES[i]] + [f"{0.25 * loc[k][i]:.3f}" for k in DIMS] + [f"{tot[i]:.3f}"] for i in np.argsort(-tot)]
    table(rows, ["Model", "Mech", "Space", "Data", "Valid.", "Overall"])
    print("Baseline CRs:", {k: round(consistency_ratio(BASELINE[k]), 3) for k in DIMS}, "\n")

    # ----
    f_, b_ = 1, 3
    a_f = loc["M"][f_] - loc["M"][b_]
    rest = sum(loc[k][f_] - loc[k][b_] for k in "SDV") / 3
    print(f"Break-even weight on Mechanisms for Fossett to overtake Benenson: {rest / (rest - a_f):.2f}\n")

    # ---------------------
    print("=== TABLE C1: consistency ratios ===")
    rows = [[f"Assessor {a}"] + [f"{consistency_ratio(m[k]):.3f}" for k in DIMS + ["W"]] for a, m in ASSESSORS.items()]
    table(rows, ["Assessor", "Mech", "Space", "Data", "Valid.", "Dims"])

    # ------------------
    agg = {k: aij(*[m[k] for m in PANEL]) for k in DIMS + ["W"]}
    scores = {a: global_scores(m) for a, m in ASSESSORS.items()}
    scores["AIJ"] = global_scores(agg)

    print("=== TABLE 3: global priorities ===")
    rows = [[NAMES[i]] + [f"{scores[a][i]:.3f}" for a in (1, 2, 3, "AIJ")] for i in np.argsort(-scores["AIJ"])]
    table(rows, ["Model", "A1", "A2", "A3", "AIJ"])

    print("=== APPENDIX D: dimension priorities (M, S, D, V) ===")
    for a, m in ASSESSORS.items():
        print(f"Assessor {a}:", np.round(priorities(m["W"]), 3))
    print("AIJ       :", np.round(priorities(agg["W"]), 3), "\n")

    eq = sum(priorities(agg[k]) for k in DIMS) / 4
    print("Equal weights applied to the panel's AIJ model judgements:", dict(zip(NAMES, np.round(eq, 3))), "\n")

    # ----------
    print("=== TABLE 5: leave-one-assessor-out AIJ ===")
    for left_out in (3, 2, 1):
        keep = [m for a, m in ASSESSORS.items() if a != left_out]
        s = global_scores({k: aij(*[m[k] for m in keep]) for k in DIMS + ["W"]})
        order = " > ".join(NAMES[i] for i in np.argsort(-s))
        print(f"Assessors {[a for a in ASSESSORS if a != left_out]}: {order}  (Benenson - Fossett = {s[3] - s[1]:+.3f})")
    print()

    # --------
    print("=== SECTION 6.2: Spearman correlations between AIJ local priorities ===")
    p = {k: priorities(agg[k]) for k in DIMS}
    for a, b in [("S", "D"), ("S", "V"), ("D", "V"), ("M", "S"), ("M", "D"), ("M", "V")]:
        print(f"  {a} vs {b}: {stats.spearmanr(p[a], p[b])[0]:.2f}")
    print()

    # ---------
    print(f"=== TABLE 4: Monte Carlo rank frequencies ({N_ITER:,} iterations, seed {SEED}) ===")
    random.seed(SEED)
    counts = np.zeros((5, 5), dtype=int)
    for _ in range(N_ITER):
        pert = {k: [perturb_matrix(m[k]) for m in PANEL] for k in DIMS + ["W"]}
        s = global_scores({k: aij(*pert[k]) for k in pert})
        for rank, model in enumerate(s.argsort()[::-1]):
            counts[model, rank] += 1
    rows = [[NAMES[i]] + [f"{100 * c / N_ITER:.1f}%" for c in counts[i]] for i in np.argsort(-scores["AIJ"])]
    table(rows, ["Model", "1st", "2nd", "3rd", "4th", "5th"])
# Statistiques descriptives du CSA C2-C3
# Usage : python analysis/01_descriptive.py E:/neuropoly/data-multi-subject

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

data = sys.argv[1]

# CSA de chaque sujet + infos des participants
csa = pd.read_csv("results/csa_c2c3_all.csv")
csa["participant_id"] = csa["Filename"].str.extract(r"(sub-[A-Za-z0-9]+)")[0]
csa = csa.rename(columns={"MEAN(area)": "csa"})[["participant_id", "csa"]]
participants = pd.read_csv(f"{data}/participants.tsv", sep="\t")
df = csa.merge(participants, on="participant_id")
print("Sujets :", len(df))

# Exclusions 1 : liste officielle du dataset pour le CSA T2w (un sujet ou un site entier)
exclude = yaml.safe_load(open(f"{data}/exclude.yml"))["csa_t2"]
tech = [s for s in df["participant_id"]
        if any(s == e or s.rstrip("0123456789") == "sub-" + e for e in exclude)]

# Exclusions 2 : sujets non sains (compression), comme Valošek et al. 2024
patho = df.loc[df["pathology"] != "HC", "participant_id"].tolist()

exclus = sorted(set(tech + patho))
pd.Series(exclus, name="participant_id").to_csv("config/excluded_subjects.txt", index=False)
df = df[~df["participant_id"].isin(exclus)]
print(f"Exclus : {len(tech)} techniques, {len(patho)} pathology, {len(exclus)} au total")
print("Sujets gardés :", len(df))

# Statistiques
def resume(x):
    return pd.Series({"n": len(x), "moyenne": x.mean(), "sd": x.std(),
                      "CV_%": 100 * x.std() / x.mean()})

print("\nTous :\n", resume(df["csa"]).round(2))
for col in ["sex", "manufacturer", "institution_id"]:
    print(f"\nPar {col} :\n", df.groupby(col)["csa"].apply(resume).unstack().round(2))

df.to_csv("results/csa_c2c3_clean.csv", index=False)

# Figure : CSA par constructeur, femmes à gauche, hommes à droite
rng = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(7, 4.8))
marques = sorted(df["manufacturer"].unique())
for i, m in enumerate(marques):
    d = df[df["manufacturer"] == m]
    ax.boxplot(d["csa"], positions=[i], widths=0.5, showfliers=False,
               medianprops={"color": "black", "linewidth": 2})
    for dx, sexe, couleur, nom in [(-0.12, "F", "#eb6834", "Femmes"),
                                   (0.12, "M", "#2a78d6", "Hommes")]:
        y = d.loc[d["sex"] == sexe, "csa"]
        x = i + dx + rng.uniform(-0.07, 0.07, len(y))
        ax.scatter(x, y, s=20, alpha=0.75, color=couleur, edgecolor="white",
                   label=nom if i == 0 else None, zorder=3)

ax.set_xticks(range(len(marques)), [f"{m}\n(n = {(df['manufacturer'] == m).sum()})" for m in marques])
ax.set_ylabel("CSA C2-C3 (mm²)")
ax.set_title("CSA à C2-C3 par constructeur IRM", loc="left")
ax.grid(axis="y", color="#e1e0d9")
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="lower right", bbox_to_anchor=(1, 1), ncol=2)
fig.tight_layout()
fig.savefig("results/csa_by_manufacturer.png", dpi=150)

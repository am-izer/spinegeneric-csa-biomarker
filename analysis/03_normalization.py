# Question 3 : quelle normalisation réduit le mieux la variabilité du CSA ?
# On corrige le CSA pour la taille et/ou le constructeur, puis on compare le CV.
# Usage : python analysis/03_normalization.py

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("results/csa_c2c3_clean.csv").dropna(subset=["height"])
FORMULE = "csa ~ age + C(sex) + C(manufacturer, Treatment('Siemens')) + height"


def corriger(train, test, taille, constructeur):
    """Apprend le modèle sur train, retire au CSA de test les effets choisis."""
    m = smf.mixedlm(FORMULE, train, groups=train["institution_id"]).fit(reml=False)
    csa = test["csa"].copy()
    if taille:
        csa -= m.params["height"] * (test["height"] - train["height"].mean())
    if constructeur:
        for marque in ["GE", "Philips"]:
            effet = m.params[f"C(manufacturer, Treatment('Siemens'))[T.{marque}]"]
            csa -= effet * (test["manufacturer"] == marque)
    return csa


def cv(x):
    return 100 * x.std() / x.mean()


def variance_site(x):
    d = df.assign(val=x)
    return smf.mixedlm("val ~ 1", d, groups=d["institution_id"]).fit(reml=False).cov_re.iloc[0, 0]


# 5 groupes au hasard (graine fixe pour retrouver les mêmes résultats)
groupes = np.array_split(np.random.default_rng(0).permutation(df.index), 5)

methodes = {"Brut": (False, False), "Constructeur": (False, True),
            "Taille": (True, False), "Taille + constructeur": (True, True)}
lignes = []
for nom, (t, c) in methodes.items():
    # Application directe : appris et appliqué sur les mêmes sujets
    direct = corriger(df, df, t, c)
    # Validation croisée : chaque sujet corrigé par un modèle appris sans lui
    croise = pd.concat([corriger(df.drop(g), df.loc[g], t, c) for g in groupes])
    croise = croise.loc[df.index]
    lignes.append({"methode": nom, "CV_direct_%": cv(direct), "CV_croise_%": cv(croise),
                   "var_site": variance_site(croise)})

res = pd.DataFrame(lignes).round(2)
print(f"{len(df)} sujets\n")
print(res.to_string(index=False))
res.to_csv("results/normalization.csv", index=False)

# Modèle mixte : qu'est-ce qui fait varier le CSA C2-C3 ?
# CSA ~ âge + sexe + constructeur, avec le site en effet aléatoire
# Usage : python analysis/02_mixed_model.py

import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("results/csa_c2c3_clean.csv")

# Modèle 1 : âge, sexe, constructeur (Siemens = référence car le plus nombreux)
formule = "csa ~ age + C(sex) + C(manufacturer, Treatment('Siemens'))"
m1 = smf.mixedlm(formule, df, groups=df["institution_id"]).fit(reml=False)
print(m1.summary())

# Part de la variance due au site (ICC) : variance site / variance totale
var_site = m1.cov_re.iloc[0, 0]
var_res = m1.scale
print(f"Variance site : {var_site:.2f}   Variance résiduelle : {var_res:.2f}")
print(f"ICC site : {100 * var_site / (var_site + var_res):.1f} %\n")

# Modèle 2 : on ajoute la taille (sujets dont la taille est connue)
d = df.dropna(subset=["height"])
m1b = smf.mixedlm(formule, d, groups=d["institution_id"]).fit(reml=False)
m2 = smf.mixedlm(formule + " + height", d, groups=d["institution_id"]).fit(reml=False)
print(f"Avec la taille ({len(d)} sujets) :")
print(m2.summary().tables[1].loc[["height"]])
print(f"AIC sans taille : {m1b.aic:.1f}   AIC avec taille : {m2.aic:.1f}  (plus petit = meilleur)")

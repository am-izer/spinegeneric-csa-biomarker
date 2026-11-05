# spinegeneric-csa-biomarker

**Résumé (FR) :** Dans ce projet, je calcule l'aire de section de la moelle cervicale (CSA) au niveau C2-C3 avec la Spinal Cord Toolbox, sur les sujets sains du dataset public spine-generic. Le but est d'étudier la variabilité du CSA entre les sujets et entre les sites/constructeurs IRM, et de comparer des méthodes de normalisation. Pour l'instant, le pipeline fonctionne sur 5 sujets de test.

## About

Personal project on the spinal cord cross-sectional area (CSA) as an MRI biomarker.
I compute the CSA at C2-C3 on healthy subjects from the Spine Generic dataset, and I want to study:

- how reliable the automatic measure is
- how much CSA varies between subjects, sites and MRI manufacturers
- which normalization method reduces this variability

## Data

Spine Generic Public Database (Multi-Subject): https://github.com/spine-generic/data-multi-subject
(commit `0ef57a7f9052ec96c141d59d06beb159883ce269`)

I use the T2w images, and the spinal cord segmentations and disc labels from `derivatives/labels`.

## Tools

- Spinal Cord Toolbox (SCT) 7.3
- git-annex
- Git Bash (Windows)

## How to run

```bash
sct_run_batch -script scripts/process_data.sh -path-data <path_to_data-multi-subject> -path-output <output_folder> -include-list $(cat config/subjects_test.txt) -jobs 3
```

The script computes the mean CSA between C2 and C3 for each subject with `sct_process_segmentation`.

## First results (5 test subjects)

| Subject | Scanner | CSA C2-C3 (mm²) |
|---|---|---|
| sub-amu01 | Siemens | 78.3 |
| sub-barcelona01 | Siemens | 73.5 |
| sub-beijingGE01 | GE | 72.1 |
| sub-tokyoIngenia01 | Philips | 84.2 |
| sub-ucl01 | Philips | 66.3 |

The values look normal for healthy adults. With only 5 subjects I can't compare the manufacturers yet.

## Reference

Cohen-Adad J. et al. (2021). Open-access quantitative MRI data of the spinal cord and reproducibility across participants, sites and manufacturers. *Scientific Data*, 8, 219.

---
Amina Izerouel — M2 Bioinformatics, USTHB

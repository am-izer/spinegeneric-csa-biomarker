#!/bin/bash
#
# process_data.sh
#
# Calcule l'aire de section de la moelle épinière (CSA) entre C2 et C3
# pour un sujet de la Spine Generic Public Database (Multi-Subject),
# à partir de la segmentation de la moelle sur l'image T2w et des
# labels des disques intervertébraux fournis dans derivatives/labels.
#
# Ce script est lancé par sct_run_batch, qui fournit :
#   $1               : identifiant du sujet (ex. sub-amu01)
#   PATH_DATA        : chemin du dataset BIDS (data-multi-subject)
#   PATH_RESULTS     : dossier où sont écrits les résultats
#   PATH_LOG         : dossier où sont écrits les fichiers log
#   PATH_QC          : dossier où sont écrits les rapports de contrôle qualité
#
# Exemple :
#   sct_run_batch -script scripts/process_data.sh \
#                 -path-data /e/neuropoly/data-multi-subject \
#                 -path-output /e/neuropoly/output_test \
#                 -include-list sub-amu01 sub-ucl01 -jobs 3
#
# Autrice : Amina Izerouel
# Version de SCT : 7.3

# S'arrêter à la première erreur, et afficher chaque commande avant de l'exécuter (pour le log)
set -e
set -x

# Identifiant du sujet, transmis par sct_run_batch
SUBJECT=$1

# Fichiers d'entrée
FILE_T2W="${PATH_DATA}/${SUBJECT}/anat/${SUBJECT}_T2w.nii.gz"
FILE_SEG="${PATH_DATA}/derivatives/labels/${SUBJECT}/anat/${SUBJECT}_T2w_label-SC_seg.nii.gz"
FILE_DISCS="${PATH_DATA}/derivatives/labels/${SUBJECT}/anat/${SUBJECT}_T2w_label-discs_dlabel.nii.gz"

# Vérifier que les 3 fichiers sont présents (contenu téléchargé avec git-annex)
for f in "$FILE_T2W" "$FILE_SEG" "$FILE_DISCS"; do
  if [ ! -s "$f" ]; then
    echo "ERREUR : fichier manquant ou vide : $f"
    echo "Téléchargez-le avec : git annex get <fichier>"
    exit 1
  fi
done

# Un fichier CSV par sujet (évite que plusieurs sujets traités en parallèle écrivent dans le même fichier)
mkdir -p "${PATH_RESULTS}/per_subject"

# CSA moyen (et autres mesures morphométriques) entre C2 et C3
sct_process_segmentation \
  -i "$FILE_SEG" \
  -discfile "$FILE_DISCS" \
  -vert 2:3 \
  -o "${PATH_RESULTS}/per_subject/${SUBJECT}_csa_c2c3.csv"

echo "Terminé : ${SUBJECT}"

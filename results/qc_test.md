# Visual QC – 5 test subjects

Checked with FSLeyes: T2w image + spinal cord segmentation (red) + disc labels (green).

Commands used (from the `data-multi-subject` folder, with `S` = subject ID, e.g. `S=sub-amu01`):

```bash
# Open the T2w image with the segmentation (red) and the disc labels (green)
fsleyes $S/anat/${S}_T2w.nii.gz \
        derivatives/labels/$S/anat/${S}_T2w_label-SC_seg.nii.gz -cm red -a 40 \
        derivatives/labels/$S/anat/${S}_T2w_label-discs_dlabel.nii.gz -cm green

# List the disc labels (position and value)
sct_label_utils -i derivatives/labels/$S/anat/${S}_T2w_label-discs_dlabel.nii.gz -display
```

For each subject I checked:
- sagittal view: the segmentation follows the cord, no leak into the CSF
- disc labels: 10 labels present (checked with `sct_label_utils -display`)
- axial view at C2-C3: the segmentation fills the cord, no over/under-segmentation

| Subject | Segmentation | Disc labels | Notes |
|---|---|---|---|
| sub-amu01 | OK | OK | |
| sub-barcelona01 | OK at C2-C3 | OK | Manually corrected segmentation (`GeneratedBy` field in `derivatives/labels/sub-barcelona01/anat/sub-barcelona01_T2w_label-SC_seg.json`: `sct_deepseg_sc` then `Manual`, 2021), stops in the lower cervical cord. Labels 1-2 are on sagittal slice x=30, the others on x=31 |
| sub-beijingGE01 | OK | OK | FSLeyes orientation warning: header affine differs at the 6th decimal between T2w and segmentation (rounding), same voxel grid. Oblique acquisition |
| sub-tokyoIngenia01 | OK | OK | Highest CSA (84.2 mm²), no leak into the CSF. Labels 3-10 are on slice x=30 |
| sub-ucl01 | OK | OK | Lowest CSA (66.3 mm²), no under-segmentation. Same orientation warning as sub-beijingGE01 |

All 5 subjects passed QC.

Note: SCT disc label convention: 2 = C1-C2, 3 = C2-C3, 4 = C3-C4. The CSA at levels C2-C3 is computed between labels 2 and 4.

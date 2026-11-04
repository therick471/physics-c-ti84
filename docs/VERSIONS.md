# Versions and patches

Dates below follow the chat chronology in America/New_York. They are development dates, not invented semantic-version tags or Git history. Existing filenames and program contents are preserved; incidental `.DS_Store` metadata was removed from two download ZIPs. Some early ZIP filenames now contain later patched files; consult the actual contents and hashes, not the name alone.

| Date / edition | What changed | Download / status |
|---|---|---|
| Oct 7 · original full-course packed edition | 13 units, 160 equations, 566 unknown targets, 15 multi-step tools; compressed loader | [Original ZIP](../downloads/AP_Physics_C_Evo.zip). **Historical**: startup/memory issues reported; use corrected release |
| Oct 7 · corrected plain-source / Lite | Removes compressed loader, lazy-loads units, fixes import-style launch; 22 core files and four optional tools | [Corrected ZIP](../downloads/AP_Physics_C_Evo_Fixed.zip). Recommended full-course Evo edition |
| Oct 7 · v3 string-method repair | Replaces unsupported `isalnum`/related checks; APCHECK v3 marker | [APC_v3_Patch.zip](../downloads/APC_v3_Patch.zip). Two-file patch for an older corrected install; already folded into the current corrected bundle |
| Oct 29–30 · E-Field Studio / E&M edition | Removes Mechanics from the active E&M install; adds five field models, derivations, limits/extrema, sketches and inverses | [EField_Studio_Evo.zip](../downloads/EField_Studio_Evo.zip). Preserved snapshot; sharing package is the clearer fresh install |
| Oct 30 · navigation/readability v2 | Arrow navigation, wrapped and paginated guides, expanded coverage and checks | [v2 patch](../downloads/EField_Studio_v2_Patch.zip) and [Navigation Fix](../downloads/EField_Navigation_Fix.zip). Current saved archives have eight files; early chat descriptions of seven are stale |
| Oct 30 · keyboard v3 | Evo key codes, blocking get_key(1), calibration launcher | [Keyboard patch](../downloads/EField_Studio_v3_Keyboard_Patch.zip), two files |
| Oct 30 · plain UI / highlight repair | Removes colored bars and corrects Evo text-baseline highlight alignment | [Plain UI patch](../downloads/EField_Plain_UI_Update.zip), one EFGUI file. Later full packages incorporate the result |
| Oct 30 · final formulas | Adds answer-only formula browsing in APC, EFIELD and each model | [Final formulas patch](../downloads/EField_Final_Formulas_Update.zip), three files |
| Oct 30 · Mechanics restore | Saves locally generated Mechanics sources and older launcher after Mechanics removal | [Restore source folder](../calculator/Mechanics_Restore_2026-10-30). **Recovery snapshot**; use the complete corrected toolkit for a fresh install |
| Nov 2 · dual-model sharing package | Separate Evo and CE Python UI/keyboard profiles; 34 files each; installs, troubleshooting, manifests | [Sharing ZIP](../downloads/Share_AP_Physics_C_EM.zip). Recommended E&M / Quiz 8.4 download |
| Nov 3 · Exam 2 rebuild | Adds EXAM2, E2APP, E2CALC, E2PHYS, E2NOTES, E2CHECK; Gauss/energy/charge solvers and study cards | [Exam2_Evo.zip](../downloads/Exam2_Evo.zip), 40-file complete Evo install; eight-file update for existing studio |
| Nov 3 · Exam 2 banner repair | Reserves 32 pixels above content, four body rows, preserves text through extra pages | [Exam2_Banner_Fix.zip](../downloads/Exam2_Banner_Fix.zip), one file; already included in the current Exam 2 ZIP |

## Safe choices

For a fresh Evo Exam 2 install, send all 40 files from `Exam2_Evo/TRANSFER`. For CE Python, use only its 34-file sharing profile. For full Mechanics + E&M on Evo, choose the corrected full-course ZIP. These are separate complete installs with overlapping filenames.

For an existing compatible Evo E-Field Studio install, Exam 2 `UPDATE` contains the six E2/EXAM2 modules plus APC and EFGUI: **eight files**. Sending only the seven files mentioned in an earlier reply would omit the banner repair. Restart Python after any update.

Do not apply old E-Field patches over Exam 2 or copy Evo EFGUI over the CE Python profile. An older APC patch can remove the Exam 2 entry. Do not combine UPDATE and TRANSFER for the same release.

## Preserved development layouts

`calculator/APC_EVO` is the original generated source; `APC_INSTALL` is its packed transfer build. `APC_LITE_SOURCE` and `APC_LITE` hold the corrected plain-source development and compact builds. `AP_Physics_C_Evo` and `AP_Physics_C_Evo_Fixed` preserve original packaged trees. `EFIELD_SOURCE` is the editable field-studio source, while `EField_EM/TRANSFER` is the E&M transfer snapshot. `Exam2_Evo/TRANSFER` is the latest complete Evo exam snapshot. `calculator/dev` holds builders and regression tests, not calculator launch files.

File-level copies and original SHA-256 hashes are recorded in [source-manifest.json](../source-manifest.json). Older test logs may contain historical failures; current check results are in [Validation](VALIDATION.md).

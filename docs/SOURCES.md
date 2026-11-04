# Sources and project review

Prepared November 3, 2026. Reviewed all available turn pages in the seven existing AP Physics C project chats and the separate Exam 2 chat using the same study folder. Active and archived Codex history were checked; no archived chats were returned. No separate AP Physics C ChatGPT project was listed by the app. This covers the available project record, not inaccessible or deleted conversations. Private transcripts are not published.

| Reviewed chat | Turns reviewed | Contribution |
|---|---:|---|
| Build AP Physics C TI-84 Program | 14 | Original toolkit, memory/startup repair, Lite/v3, Mechanics removal, field studio, keyboard/layout repairs, formulas, dual-model share package |
| Build an electrostatics study guide | 17 | First-exam scope revisions; final class-note alignment to charge/forces and circuits |
| Create electric field proof practice | 4 | Quiz 8.4 finite-rod/ring scope and corrected proof methods |
| Untitled screenshot-based project chat | 2 | Ring/arc comparison problems and two-ring cancellation example; app listing title consists of attachment text |
| Explain V and X relationship | 4 | Potential graph and electrode-map lab relevance |
| Solve a problem | 11 | Charge-sharing system, Coulomb vectors, numeric-solver use; no new program release |
| Explain how to solve AM4 | 2 | Circuit junction/ideal-ammeter reasoning |
| Build Exam 2 study guide | 4 | Confirmed exam description, new Exam 2 modules, banner fix |

The code inventory includes every ordinary file in the project's `calculator` and sharing-package trees, excluding OS metadata and Python caches. Saved ZIP versions are in `downloads`; incidental `.DS_Store` metadata was removed from the corrected full-course and Exam 2 archives before publication, while their program/documentation entries were preserved. Original and published archive hashes are recorded in the manifest. One historical failure log has its machine-specific project prefix replaced by `<project>`; its original and published hashes are both recorded. No attempt is made to reconstruct source versions that were overwritten and no longer exist. ZIP snapshots sometimes preserve earlier content than the adjacent extracted folder.

## Official installation references

- [TI Connect Evo](https://connectevo.ti.com/) and [Evo / Evo-T connectivity guide](https://education.ti.com/en/product-resources/eguides/eguide-84-evo/evo-connect-user-guide).
- [TI Connect CE download and current system requirements](https://education.ti.com/en/products/computer-software/ti-connect-ce-sw).
- [TI Python conversion, filenames and RAM instructions](https://education.ti.com/html/eguides/connectivity/TI-Connect-CE/EN/Content/EG_84_TIConnect/M_UsePython/M_UsePython.HTML).
- [TI Connect CE model compatibility](https://education.ti.com/html/eguides/graphing/84plusce/en/content/eg_84tic/m_introtic-ce/tc_intrototiconnect.HTML) and [legacy model support](https://education.ti.com/en/customer-support/knowledge-base/ti-83-84-plus-family/product-usage/37036).
- [CE OS and apps](https://education.ti.com/en/software/update/84-ce-software-update).

These TI pages were checked during repository assembly. Instructions are paraphrased. Regional-device compatibility beyond the tested target is explicitly labeled as unverified. Existing source documents retain their original dates and claims; this repository's guide distinguishes those historical claims from current validation.

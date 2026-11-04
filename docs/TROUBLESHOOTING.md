# Troubleshooting

| Symptom | What to do |
|---|---|
| Computer does not detect calculator | Check power, USB data cable, adapter and supported browser/software. Use Connect Evo for Evo and Connect CE for CE Python. Reconnect and grant the calculator connection. |
| ZIP will not send | Extract it on the computer. Select `.py` files from exactly one transfer folder. |
| Missing module / import error | Transfer every file in the matching complete folder, preserve names, then restart Python. Do not run support modules such as E2PHYS or APCORE directly. |
| Old menu appears after update | Reinitialize/restart the Python shell; imported modules can remain cached. Then launch EXAM2, EFIELD or APC as appropriate. |
| Arrow keys do nothing / wrong row opens | Use the correct model profile. On the sharing release run EFKEY and finish its navigation test; learned codes last for the session. Do not apply the Evo GUI to CE Python. |
| Text hidden behind Python banner on Exam 2 Evo | Current Exam 2 bundle includes the fix. On a matching older Exam 2 install, replace only EFGUI with Exam2_Banner_Fix/EFGUI.py, restart Python, and check on the screen. |
| Silent APC or APCHECK on original toolkit | Use the corrected full-course bundle; the original launcher did not handle TI's import-style startup properly. |
| `str` has no attribute `isalnum` | Use the current corrected full-course bundle; v3 removes unsupported character-predicate calls. Historical two-file patch is for that toolkit only. |
| MemoryError | Restart Python and run the target launcher directly. Use one install, keep only needed optional groups, and back up your own files before removing anything. Source bytes do not measure runtime heap. |
| Missing ti_draw / ti_plotlib / Python | Obtain model-appropriate OS/apps/modules from TI. Text fallback exists for some views; graphs need ti_plotlib. See [TI CE updates](https://education.ti.com/en/software/update/84-ce-software-update) and the bundled sharing troubleshooting guide. |
| CE file sent but not shown in Python | TI's Python app loads/runs Python AppVars in RAM. Check names and RAM/Archive in Calculator Explorer or calculator memory management. |
| Numerical solver cannot find root | Supply a continuous sign-changing bracket and respect physical domains. Some equations have multiple roots; a bracket selects one. |
| Result differs by powers of ten / sign | Convert all quantities to SI, enter scientific notation carefully, distinguish full rod length from radius, and use the specified coordinate origin. |

For the two sharing profiles, see the original [detailed troubleshooting guide](../Share_AP_Physics_C_EM/TROUBLESHOOTING.txt). Report the model, OS/Python version, bundle, launcher, selected menu and exact error line so a failure can be reproduced.

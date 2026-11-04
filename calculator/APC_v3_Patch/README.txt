AP Physics C - v3 patch for the corrected plain-Python edition

1. Transfer APCORE.py and APCHECK.py, replacing the matching calculator files.
2. Restart or reinitialize the Python shell. Otherwise it may keep old imports.
3. Run APCHECK. Expect APCHECK START v3, SELF CHECK PASS, and 8 numeric checks passed.
4. Restart the shell again, then run APC.

The missing str.isalnum operation is replaced with ASCII letter/digit comparisons. No character-predicate methods remain in the calculator sources. The check reports its stage on failure.

This two-file patch was verified against the previously delivered corrected release. The full v3 release also passed 29 desktop test groups, including all 566 formula targets. It remains unverified on a physical Evo.

If you still have the original compressed APLOAD edition, use AP_Physics_C_Evo_Fixed.zip instead and follow its README. The two-file patch is intended for the corrected plain-Python install.

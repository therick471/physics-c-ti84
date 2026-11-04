import sys
import gc

def release(names):
    if hasattr(sys, 'modules'):
        for name in names:
            if name in sys.modules:
                del sys.modules[name]
    gc.collect()

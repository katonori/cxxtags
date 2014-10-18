import commands
import os
import sys

result = "func|" + os.path.abspath(os.path.dirname(__file__)) + "/b/b.h|3|20|static inline void func()"

commands.getstatusoutput("rm -rf _db")
(rv, out) = commands.getstatusoutput("cxxtags_run_proj -t vs _db proja.sln")
assert rv == 0
print out
(rv, out) = commands.getstatusoutput("cxxtags_query def _db a/a.cpp 10 12")
assert rv == 0
print out
assert out == result

sys.exit(0)

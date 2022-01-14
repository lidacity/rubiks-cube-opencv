import logging

from rubiks_cube_opencv import GetRecognize
from rubiks_cube_opencv import STRING


# logging.basicConfig(filename='rubiks-rgb-solver.log',
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)5s: %(message)s"
)
log = logging.getLogger(__name__)

desc = "recognize"
expected = "OGRYOYYOOBBOOWOGWYBBGWBGRBRWRBWYBGGOWRWWGYGYYBRWRRORGY"

results = []

log.warning("Test: %s" % desc)

try:
 output = GetRecognize(Get=STRING)
except Exception as e:
 print(e)
 log.exception(str(e))
 #output = "Exception"
 output = e

if output == expected:
 results.append("\033[92mPASS\033[0m: %s" % desc)
else:
 results.append("\033[91mFAIL\033[0m: %s" % desc)
 results.append("   expected %s" % expected)
 results.append("   output   %s" % output)

gc.collect()

print("\n".join(results))

# Configure path for py.test
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
print sys.path

os.environ["CCTNG_CONFIG_FILE"] = os.path.join(os.path.dirname(__file__), "unittest.json.config")

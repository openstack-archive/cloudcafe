# Configure path for py.test
import os

os.environ["CCTNG_CONFIG_FILE"] = os.path.join(
    os.path.dirname(__file__),
    "unittest.json.config"
)

# Configure path for py.test
import os

os.environ["OPENCAFE_ENGINE_CONFIG_FILE"] = os.path.join(
    os.path.dirname(__file__),
    "unittest.engine.config"
)

os.environ["MOCK"] = 'True'

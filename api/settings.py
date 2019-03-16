import yaml
from pathlib import Path

API_ROOT = Path(__file__).parent
PROJECT_ROOT = API_ROOT.parent

SETTINGS_DIR = Path(PROJECT_ROOT / 'settings')
SETTINGS_CONFIG_FILE = Path(SETTINGS_DIR / 'config.yaml')

SETTINGS = yaml.load(SETTINGS_CONFIG_FILE.read_text(), Loader=yaml.SafeLoader)

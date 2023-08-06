import yaml
import os

TWNEO_CONFIG = []
config_path = os.environ['twneo_config_path']
if not os.path.exists(config_path):
    print("config path does not exist using default config_yaml")
    config_path = "config.yaml"

with open (config_path ) as f :
    TWNEO_CONFIG = yaml.load(f)


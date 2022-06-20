import yaml
import os


# Load configuration (Precedence: ENV, config_file)
if os.getenv('CLOUDFLARE_INPUT_DATA'):
    config_file = os.getenv('CLOUDFLARE_INPUT_DATA')
else:
    path = os.path.dirname(os.path.realpath(__file__))
    config_file = '{}/input.yaml'.format(path)
info = yaml.load(open(config_file), Loader=yaml.Loader)

# Loading Input Data
DNS_DATA = info['dns']


def init():
    # Cisco global variable
    global DNS_DATA

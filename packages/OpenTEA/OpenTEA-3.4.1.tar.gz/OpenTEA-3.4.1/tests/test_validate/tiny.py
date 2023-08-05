import yaml
from opentea.noob.validate_light import (
    validate_light)
with open("schema_validate.yaml", "r") as fin:
    schema = yaml.load(fin, Loader=yaml.FullLoader)
with open("setup_test.yaml", "r") as fin:
    setup = yaml.load(fin, Loader=yaml.FullLoader)

validate_light(setup, schema)
from blueprint_generator import Blueprint
import blueprint_import_export

import json

bp = Blueprint()

bp.generate_rom_entities(4)

json_stf = json.dumps(bp.json_dict)


# create

compressed_bp = blueprint_import_export.bp_compress(json_stf)

done_bp = blueprint_import_export.bp_encode_base64(compressed_bp)

print(done_bp)

# import (to json)

large_bp = ""

print(blueprint_import_export.bp_decompress(blueprint_import_export.bp_decode_base64(large_bp)))

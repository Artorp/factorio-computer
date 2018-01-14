# Imports and exports to the blueprint format used by Factorio
# https://wiki.factorio.com/Blueprint_string_format

import sys
import base64
import zlib

SUPP_BP_VERSION = "0"


def bp_decode_base64(blueprint: str) -> bytes:
    global SUPP_BP_VERSION
    blueprint_version = blueprint[0]
    if blueprint_version is not SUPP_BP_VERSION:
        warning_msg = "Warning: Expected Factorio blueprint version {}, was version {}\n"
        print(warning_msg.format(SUPP_BP_VERSION, blueprint_version), file=sys.stderr)

    blueprint = blueprint[1:]
    return base64.b64decode(blueprint.encode("utf-8"))


def bp_encode_base64(bp_compressed: bytes) -> str:
    global SUPP_BP_VERSION
    return SUPP_BP_VERSION + base64.b64encode(bp_compressed).decode("utf-8")


def bp_decompress(bp_compressed: bytes) -> str:
    return zlib.decompress(bp_compressed).decode("utf-8")


def bp_compress(bp_json: str) -> bytes:
    return zlib.compress(bp_json.encode("utf-8"))

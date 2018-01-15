# creates the JSON structure of a blueprint
# the resulting blueprint is meant to be used as program ROM within a Factorio computer

# see https://wiki.factorio.com/Blueprint_string_format for JSON structure

import json
import constants

map_version = 64427130880  # copied from random blueprint, probably insignificant


class Blueprint:
    """Contains the json dict, and a list of constant combinator entities which can have values"""

    def __init__(self):
        # setup instance variables
        self.e_num = counter(1)
        self.json_dict = dict()
        self.json_dict["blueprint"] = dict()
        self.bp_dict = self.json_dict["blueprint"]

        # connection entity ids
        self.prev_index_entity = None
        self.prev_PC_entity = None
        self.prev_OUT_entity = None

        # constant combinators, will later be populated with signals
        self.constant_combinators = list()

        # setup metadata
        global map_version
        self.bp_dict["label"] = "Program - PROM"
        self.bp_dict["item"] = "blueprint"
        self.bp_dict["version"] = map_version

        # setup icons
        self.bp_dict["icons"] = [{"signal": {"type": "virtual", "name": "signal-P"}, "index": 1},
                                 {"signal": {"type": "virtual", "name": "signal-R"}, "index": 2},
                                 {"signal": {"type": "virtual", "name": "signal-O"}, "index": 3},
                                 {"signal": {"type": "virtual", "name": "signal-M"}, "index": 4}]
        # setup entities entry
        self.bp_dict["entities"] = list()
        self.entities = self.bp_dict["entities"]

        # generate stone wall entities
        stone_walls_positions = [(-4, -1), (-4, 0), (-3, -1), (2, -1), (3, 0), (3, -1)]
        for x, y in stone_walls_positions:
            ent_n = next(self.e_num)
            stone_wall = generate_entity(ent_n, "stone-wall", x, y)
            assert isinstance(self.entities, list)
            self.entities.append(stone_wall)

        # generate initial lamp entities (input and output connections)
        self.prev_PC_entity = generate_entity(next(self.e_num), "small-lamp", -1, -2)
        self.prev_OUT_entity = generate_entity(next(self.e_num), "small-lamp", 2, -2)
        self.entities.append(self.prev_PC_entity)
        self.entities.append(self.prev_OUT_entity)

    def generate_rom_entities(self, number_of_lines):
        if number_of_lines < 0:
            raise ValueError("Number of lines must be non-negative, was {}".format(number_of_lines))
        if number_of_lines == 0:
            return
        with open(constants.PROM_SINGLE_LINE_TEMPLATE) as f:
            single_line_json = f.read()

        i = 0
        while i < number_of_lines:
            # code here
            std_entities = json.loads(single_line_json)["entities"]
            arith, lamp, const_comb, decider = std_entities
            for e in std_entities:
                e["entity_number"] = next(self.e_num)
                e["position"]["y"] = i
            self.constant_combinators.append(const_comb)

            # manage connections
            # red circuit
            if self.prev_index_entity is not None:
                entities_connect(arith, self.prev_index_entity, "red", "1", "2")
            self.prev_index_entity = arith

            entities_connect(arith, lamp, "red", "1", "1")
            entities_connect(lamp, decider, "red", "1", "1")
            entities_connect(const_comb, decider, "red", "1", "1")

            # PC circuit
            entities_connect(lamp, self.prev_PC_entity, "green", "1", "1")
            self.prev_PC_entity = lamp
            entities_connect(lamp, decider, "green", "1", "1")

            # ROM out circuit
            prev_side = "1" if i == 0 else "2"
            entities_connect(decider, self.prev_OUT_entity, "green", "2", prev_side)
            self.prev_OUT_entity = decider

            self.entities += std_entities
            i += 1

    def insert_signals(self, signals):
        item_signals = ["copper-ore", "copper-plate", "iron-ore", "iron-plate"]
        for i, combinator in enumerate(self.constant_combinators):
            if "control_behavior" not in combinator:
                combinator["control_behavior"] = dict()
            # clear any previous signal(s)
            combinator["control_behavior"]["filters"] = list()
            c_signals = combinator["control_behavior"]["filters"]
            sig_count = counter(1)
            for signal in signals[i]:
                sig_type = {
                                "type": "item" if signal in item_signals else "virtual",
                                "name": signal
                            }
                new_signal = {"signal": sig_type, "count": signals[i][signal], "index": next(sig_count)}
                c_signals.append(new_signal)
            # print(json.dumps(combinator))


def counter(start_index):
    n = start_index
    while True:
        yield n
        n += 1


def generate_entity(n, name, x, y):
    entity = dict()
    entity["entity_number"] = n
    entity["name"] = name
    entity["position"] = {"x": x, "y": y}
    return entity


def entities_connect(entity1, entity2, color, side1="1", side2="1"):
    """Assumes connection between these entities does not already exist"""
    con = "connections"
    e1_tuple = entity1, side1, side2, entity2["entity_number"]
    e2_tuple = entity2, side2, side1, entity1["entity_number"]
    for e, side_mine, side_their, n in e1_tuple, e2_tuple:
        if con not in e:
            e[con] = dict()
        if side_mine not in e[con]:
            e[con][side_mine] = dict()
        if color not in e[con][side_mine]:
            e[con][side_mine][color] = list()
        wire = {"entity_id": n, "circuit_id": int(side_their)}
        e[con][side_mine][color].append(wire)

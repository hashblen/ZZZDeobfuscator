import tools


class Deobf:
    def __init__(self, name):
        self.name = name
        self.obfuscated = tools.read_obfuscated(self.name + ".json")
        self.example = tools.read_example(self.name + "Example.json")
        self.deobfuscated = None
        self.key_mapping = None

    def _create_key_mapping(self, obfuscated_item, example_item):
        key_mapping = {}
        for obfuscated_key, deobfuscated_key in zip(obfuscated_item.keys(), example_item.keys()):
            if isinstance(obfuscated_item[obfuscated_key], dict) and isinstance(example_item[deobfuscated_key], dict):
                key_mapping[obfuscated_key] = deobfuscated_key
                key_mapping.update(
                    self._create_key_mapping(obfuscated_item[obfuscated_key], example_item[deobfuscated_key]))
            elif isinstance(obfuscated_item[obfuscated_key], list) and isinstance(example_item[deobfuscated_key], list):
                key_mapping[obfuscated_key] = deobfuscated_key
                for obfuscated_subitem, example_subitem in zip(obfuscated_item[obfuscated_key],
                                                               example_item[deobfuscated_key]):
                    if isinstance(obfuscated_subitem, dict) and isinstance(example_subitem, dict):
                        key_mapping.update(self._create_key_mapping(obfuscated_subitem, example_subitem))
            else:
                key_mapping[obfuscated_key] = deobfuscated_key
        return key_mapping

    def create_key_mapping(self):
        self.key_mapping = self._create_key_mapping(self.obfuscated[next(iter(self.obfuscated.keys()))][0],
                                                    self.example)

    def deobfuscate(self, makeID=None):
        if self.key_mapping is None:
            self.create_key_mapping()
        deobfuscated_data = {}
        for item in self.obfuscated[next(iter(self.obfuscated.keys()))]:
            deobfuscated_item = self._deobfuscate_item(item)
            if makeID is not None:
                id = deobfuscated_item.get(makeID)
                if id is None:
                    raise ValueError("ID was not found!")
                deobfuscated_data[id] = deobfuscated_item
            else:
                deobfuscated_data.update(deobfuscated_item)
        self.deobfuscated = deobfuscated_data

    def _deobfuscate_item(self, item):
        deobfuscated_item = {}
        for obfuscated_key, value in item.items():
            deobfuscated_key = self.key_mapping[obfuscated_key]
            if isinstance(value, dict):
                deobfuscated_item[deobfuscated_key] = self._deobfuscate_item(value)
            elif isinstance(value, list):
                deobfuscated_item[deobfuscated_key] = [self._deobfuscate_item(i) if isinstance(i, dict) else i for i in
                                                       value]
            else:
                deobfuscated_item[deobfuscated_key] = value
        return deobfuscated_item

    def save_deobfuscated(self, makeID=None):
        if self.deobfuscated is None:
            self.deobfuscate(makeID=makeID)
        tools.write_deobfuscated(self.deobfuscated, self.name + ".json")
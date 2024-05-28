import json
import yaml
import xml.etree.ElementTree as ET


class Converter:
    def convert(self, input_path, output_path):
        input_format = input_path.split(".")[-1].lower()

        if input_format == "json":
            data = self.read_json(input_path)
        elif input_format in ["yml", "yaml"]:
            data = self.read_yaml(input_path)
        elif input_format == "xml":
            data = self.read_xml(input_path)
        else:
            raise ValueError("Unsupported input format")

        output_format = output_path.split(".")[-1].lower()

        if output_format == "json":
            self.write_json(data, output_path)
        elif output_format in ["yml", "yaml"]:
            self.write_yaml(data, output_path)
        elif output_format == "xml":
            self.write_xml(data, output_path)
        else:
            raise ValueError("Unsupported output format")

    def read_json(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def read_yaml(self, file_path):
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    def read_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for child in root:
            item = {}
            for subchild in child:
                item[subchild.tag] = subchild.text
            data.append(item)
        return data

    def write_json(self, data, file_path):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    def write_yaml(self, data, file_path):
        with open(file_path, "w") as file:
            yaml.dump(data, file, default_flow_style=False)

    def write_xml(self, data, file_path):
        root_name = "data"
        root = ET.Element(root_name)

        for item in data:
            child = ET.SubElement(root, "item")
            for key, value in item.items():
                subchild = ET.SubElement(child, key)
                subchild.text = value

        tree = ET.ElementTree(root)
        tree.write(file_path)

import json
import yaml
import xml.etree.ElementTree as ET
import argparse


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path, data):
    with open(file_path, "w") as file:
        file.write(data)


def convert_to_dict(data, input_format):
    if input_format == "json":
        return json.loads(data)
    elif input_format in ["yml", "yaml"]:
        return yaml.safe_load(data)
    elif input_format == "xml":
        root = ET.fromstring(data)
        return {root.tag: {child.tag: child.text for child in root}}


def convert_from_dict(data_dict, output_format):
    if output_format == "json":
        return json.dumps(data_dict, indent=2)
    elif output_format in ["yml", "yaml"]:
        return yaml.dump(data_dict, default_flow_style=False)
    elif output_format == "xml":
        root_tag = list(data_dict.keys())[0]
        root = ET.Element(root_tag)
        for key, value in data_dict[root_tag].items():
            child = ET.SubElement(root, key)
            child.text = value
        return ET.tostring(root, encoding="unicode")


def get_file_format(file_path):
    return file_path.split(".")[-1].lower()


def convert_file(input_path, output_path):
    input_format = get_file_format(input_path)
    output_format = get_file_format(output_path)

    data = read_file(input_path)
    data_dict = convert_to_dict(data, input_format)
    converted_data = convert_from_dict(data_dict, output_format)

    write_file(output_path, converted_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert data between XML, JSON, and YAML formats."
    )
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("output_file", help="Path to the output file.")

    args = parser.parse_args()

    convert_file(args.input_file, args.output_file)

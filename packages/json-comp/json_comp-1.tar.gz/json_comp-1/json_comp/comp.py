import json


def read_json(file_path):
        try:
            with open(file_path) as json_file:
                a = json.load(json_file)
            return a
        except ValueError as e:
            print('invalid json: %s' % e)
            print('Please check your file name or file data')
            return None  # or: raise

def ordered_file(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered_file(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered_file(x) for x in obj)
    else:
        return obj

def compare_files(first_file_path,second_file_path):
    print(ordered_file(read_json(first_file_path)) == ordered_file(read_json(second_file_path)))





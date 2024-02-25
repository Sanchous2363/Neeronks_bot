import json
def load_user_data(data_path):
    try:
        with open(data_path, "r", encoding='utf-8') as file:
            return json.load(file)
    except:
        return {}
def save_user_data(user_data, data_path):
    with open(data_path, "w") as file:
        json.dump(user_data, file, ensure_ascii=False, indent=2)
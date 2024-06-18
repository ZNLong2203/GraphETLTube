import json
import os

XDG_DATA_HOME = os.getenv("XDG_DATA_HOME", "/usr/share/")

def default_search_folders(app_name):
    return [
        "%s/cdis/%s" % (XDG_DATA_HOME, app_name),
        "/usr/share/cdis/%s" % app_name,
        "%s/gen3/%s" % (XDG_DATA_HOME, app_name),
        "/usr/share/gen3/%s" % app_name,
        "/var/www/%s" % app_name,
        "/etc/gen3/%s" % app_name,
    ]

def find_paths(file_name, app_name, search_folders=None):
    search_folders = search_folders or default_search_folders(app_name)
    possible_files = [os.path.join(folder, file_name) for folder in search_folders]
    return [path for path in possible_files if os.path.exists(path)]

def load_json(file_name, app_name, search_folders=None):
    actual_files = find_paths(file_name, app_name, search_folders)
    if not actual_files:
        return None
    with open(actual_files[0], "r") as reader:
        return json.load(reader)

def get_database_url():
    app_name = os.getenv('APP_NAME', 'default_app')
    conf_data = load_json("creds.json", app_name)
    if conf_data:
        return "postgresql://%s:%s@%s:5432/%s" % (
            conf_data.get("db_username"),
            conf_data.get("db_password"),
            conf_data.get("db_host"),
            conf_data.get("db_database"),
        )
    return os.getenv("DATABASE_URL", "postgresql://postgres:5432/postgres")

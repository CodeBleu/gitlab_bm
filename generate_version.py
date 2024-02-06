#!/usr/bin/env python
"""
Generate App Info ( Version )
"""

import os
import tomlkit

def generate_app_info():
    """
    Retrieve application information from pyproject.toml.
    """
    pyproject_path = "pyproject.toml"
    with open(pyproject_path, "r", encoding="utf-8") as file:
        doc = tomlkit.parse(file.read())

    app_version = doc["tool"]["poetry"]["version"]
    app_path = doc["tool"]["poetry"]["name"].replace('-', '_')
    app_name = doc["tool"]["poetry"]["name"]

    app_info_path = os.path.join(os.path.dirname(__file__), 'src', app_path, 'app_info.py')
    with open(app_info_path, 'w', encoding="utf-8") as file:
        file.write(f"__version__ = '{app_version}'\n")
        file.write(f"__app_name__ = '{app_name}'\n")

    print("Generated Version file")
    print(f"App Name: {app_name}")
    print(f"App Version: {app_version}")

generate_app_info()

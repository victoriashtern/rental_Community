import json
import mysql.connector

class Database:

    def __init__(self, config_path="config.json"):
        # Load credentials from JSON
        with open(config_path, "r") as config_file:
            config = json.load(config_file)["mysql"]

        # Establish connection using JSON credentials
        self.connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            port=config.get("port", 3306)
        )

    def get_connection(self):
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
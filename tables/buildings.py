from  tables.table import Table
import csv

class Buildings(Table):
    def __init__(self, connection):
        self.connection = connection
    
    def truncate(self):
        try:
            super().truncate("buildings")
        except ValueError as e:
            raise ValueError(f"Buildings.truncate: {e}")


    def delete(self):
            try:
                super().delete("buildings")
            except ValueError as e:
                raise ValueError(f"Buildings.delete: {e}")
            
    def create(self):
        try:
            sql = """    
                    CREATE TABLE `buildings` (
                        `building_id` varchar(10) NOT NULL,
                        `name` varchar(100) NOT NULL,
                        `address` varchar(255) NOT NULL,
                        `total_floors` int NOT NULL,
                        PRIMARY KEY (`building_id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                """
            super().create(sql)
        except ValueError as e:
            raise ValueError(f"Buildings.create: {e}")
            
    def upload_data(self,filename):

        try:
            # 1. Openning csv file
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)            
                cursor = self.connection.cursor()

                for row in reader:
                    building =(row["building_id"],
                                row["name"],
                                row["address"],
                                int(row["total_floors"]),
                            )
                
                    sql ="""
                            insert into buildings (building_id, name,address, total_floors)  values 
                            (%s, %s,%s,%s);
                        """

                    cursor.execute(sql, building)
            
            # commit data
            self.connection.commit()
        except (ValueError, KeyError) as e:
            # Error in a file formatting
            self.connection.rollback()
            raise ValueError(f"Buildings.upload_data: CSV file reading formating {e}")
        except Exception as db_error:
            # Handle database execution errors
            self.connection.rollback()
            raise ValueError(f"Buildings.upload_data: Database connection error {db_error}")
        finally:
            # Close the cursor
            cursor.close()

def main():
    import mysql.connector
    from pathlib import Path
    import sys
    # Force Python to look in the parent folder (rental_community)
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from logger.log import  AppLogger
    
    logger = AppLogger(name="Buildings", log_file="logs/buildings.log")
    logger.info("Application started successfully.")
    
    
    try:
        connection = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="secret555!",
                                database="community_management_prod"
                                )
        file_path = Path("data/buildings.csv").resolve()
        table = Buildings(connection)
        table.upload_data(file_path)
    except Exception as e:
        logger.error(f" Error in updating data. {e}")
        
    logger.info("Buildings completed.")   


if __name__=="__main__":
    main()
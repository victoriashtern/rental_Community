from  tables.table import Table
import csv

class Apartments(Table):
    def __init__(self, connection):
        self.connection = connection

    def truncate(self):
        try:
            super().truncate("apartments")
        except ValueError as e:
            raise ValueError(f"Apartments.truncate: {e}")

    def delete(self):
        try:
            super().delete("apartments")
        except ValueError as e:
            raise ValueError(f"Apartments.delete: {e}")

    def create(self):
        try:
            sql = """    
                    CREATE TABLE `apartments` (
                    `apartment_id` int NOT NULL AUTO_INCREMENT,
                    `building_id` varchar(10) NOT NULL,
                    `flour_number` int NOT NULL DEFAULT '0',
                    `unit_number` varchar(20) NOT NULL,
                    `bedrooms` int DEFAULT '0',
                    `square_footage` int NOT NULL,
                    `monthly_rent` decimal(10,2) NOT NULL DEFAULT '0.00',
                    PRIMARY KEY (`apartment_id`),
                    KEY `building_frg_idx` (`building_id`),
                    CONSTRAINT `building_frg` FOREIGN KEY (`building_id`) REFERENCES `buildings` (`building_id`) ON DELETE CASCADE ON UPDATE CASCADE
                    ) ENGINE=InnoDB AUTO_INCREMENT=501 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                """
            super().create(sql)
        except ValueError as e:
            raise ValueError(f"Apartments.create: {e}")
        

    def upload_data(self,filename):

        try:
            # 1. Openning csv file
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)            
                cursor = self.connection.cursor()

                for row in reader:
                    lease=( int(row["apartment_id"]),
                            row["building_id"],
                            row["flour_number"], 
                            row["unit_number"],
                            float(row["bedrooms"]),
                            row["square_footage"], 
                            row["monthly_rent"]
                            )

                    sql = """    
                            insert into apartments (apartment_id, building_id,flour_number, unit_number,
                            bedrooms,square_footage,monthly_rent
                            ) 
                            values 
                            (%s, %s,%s, %s, %s,%s,%s);
                            """
                    cursor.execute(sql, lease)
                    
                # commit data
                self.connection.commit()
                                        
        except (ValueError, KeyError) as e:
            # Error in a file formatting
            self.connection.rollback()
            raise ValueError(f"Apartments.upload_data: CSV file reading formating {e}")
        except Exception as db_error:
            # Handle database execution errors
            self.connection.rollback()
            raise ValueError(f"Apartments.upload_data: Database connection error {db_error}")
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
    
    logger = AppLogger(name="Leases", log_file="logs/appartments.log")
    logger.info("Application started successfully.")
    

    try:
        connection = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="secret555!",
                                database="community_management_prod"
                                )
        file_path = Path("data/apartments.csv").resolve()
        table = Apartments(connection)
        table.upload_data(file_path)
    except Exception as e:
        logger.error(f" Error in updating data. {e}")
        
    logger.info("Apartments completed.")   


if __name__=="__main__":
    main() 

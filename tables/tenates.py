from tables.table import Table
import csv

class Tenates(Table):
    def __init__(self, connection):
            self.connection = connection

    def truncate(self):
        try:
            super().truncate("tenants")
        except ValueError as e:
            raise ValueError(f"Tenates.truncate: {e}")

    def delete(self):
        try:
            super().delete("tenants")
        except ValueError as e:
            raise ValueError(f"Tenants.delete: {e}")


    def create(self):
        try:
            sql = """    
                    CREATE TABLE `tenants` (
                        `tenant_id` int NOT NULL AUTO_INCREMENT,
                        `first_name` varchar(50) NOT NULL,
                        `last_name` varchar(50) NOT NULL,
                        `email` varchar(100) NOT NULL,
                        `phone_number` varchar(20) NOT NULL,
                        `emergency_contact_name` varchar(100) DEFAULT NULL,
                        `emergency_contact_phone` varchar(20) DEFAULT NULL,
                        `is_active` tinyint(1) DEFAULT '1',
                        PRIMARY KEY (`tenant_id`),
                        UNIQUE KEY `email` (`email`),
                        KEY `idx_tenant_email` (`email`)
                        ) ENGINE=InnoDB AUTO_INCREMENT=490 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

                """
            super().create(sql)
        except ValueError as e:
            raise ValueError(f"Tenates.create: {e}")
    
    def upload_data(self,filename):
        
        try:
            # 1. Openning csv file
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)            
                cursor = self.connection.cursor()
                for row in reader:
                    tenat=( 
                        int(row["tenant_id"]),
                        row["first_name"],
                        row["last_name"],
                        row["email"], 
                        row["phone_number"],
                        row["emergency_contact_name"],
                        row["emergency_contact_phone"], 
                        row["is_active"]
                        )

                    sql ="""
                        insert into tenants (tenant_id,first_name,last_name,email,phone_number,
                                emergency_contact_name, emergency_contact_phone,is_active)
                        values 
                        (%s, %s, %s,%s,%s,%s,%s,%s);
                        """
                    cursor.execute(sql, tenat)
            
            # commit data
            self.connection.commit()
        except (ValueError, KeyError) as e:
            # Error in a file formatting
            self.connection.rollback()
            raise ValueError(f"Tenates.upload_data: CSV file reading formating {e}")
        except Exception as db_error:
            # Handle database execution errors
            self.connection.rollback()
            raise ValueError(f"Tenates.upload_data: Database connection error {db_error}")
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
    
    logger = AppLogger(name="Tenates", log_file="logs/tenates.log")
    logger.info("Application started successfully.")
    
    
    try:
        connection = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="secret555!",
                                database="community_management_prod"
                                )
        file_path = Path("data/tenates.csv").resolve()
        table = Tenates(connection)
        table.upload_data(file_path)
    except Exception as e:
        logger.error(f" Error in updating data. {e}")
        
    logger.info("Tenates completed.")   


if __name__=="__main__":
    main()
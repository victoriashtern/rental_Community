from tables.table import Table
import csv

class Leases(Table):
    def __init__(self, connection):
        self.connection = connection

    def truncate(self):
        try:
            super().truncate("leases")
        except ValueError as e:
            raise ValueError(f"Leases.truncate: {e}")
    
    def delete(self):
        try:
            super().delete("leases")
        except ValueError as e:
            raise ValueError(f"Leases.delete: {e}")

    def create(self):
        try:
            sql = """    
                    CREATE TABLE `leases` (
                        `lease_id` int NOT NULL AUTO_INCREMENT,
                        `apartment_id` int NOT NULL,
                        `tenant_id` int NOT NULL,
                        `start_date` date NOT NULL,
                        `end_date` date NOT NULL,
                        `security_deposit` decimal(10,2) NOT NULL,
                        `lease_status` enum('Pending','Active','Terminated','Expired') DEFAULT 'Pending',
                        PRIMARY KEY (`lease_id`),
                        KEY `idx_lease_dates` (`start_date`,`end_date`),
                        KEY `fg_appartment_idx` (`apartment_id`),
                        KEY `fg_tenats_idx` (`tenant_id`),
                        CONSTRAINT `fk_lease_appartment` FOREIGN KEY (`apartment_id`) REFERENCES `apartments` (`apartment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
                        CONSTRAINT `fk_lease_tenat` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`) ON DELETE CASCADE ON UPDATE CASCADE
                        ) ENGINE=InnoDB AUTO_INCREMENT=490 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                """
            super().create(sql)
        except ValueError as e:
            raise ValueError(f"Leases.create: {e}")

                

    def upload_data(self,filename):

        try:
            # 1. Openning csv file
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)            
                cursor = self.connection.cursor()

                for row in reader:
                    lease=( 
                            int(row["lease_id"]),
                            int(row["apartment_id"]),
                            int(row["tenant_id"]),
                            row["start_date"], 
                            row["end_date"],
                            float(row["security_deposit"]),
                            row["lease_status"] 
                            )

                    sql = """    
                            insert into leases (lease_id,apartment_id, tenant_id,start_date, end_date, security_deposit,lease_status) 
                            values 
                            (%s, %s, %s,%s, %s, %s,%s);
                            """
                    cursor.execute(sql, lease)
                    
                # commit data
                self.connection.commit()
                                        
        except (ValueError, KeyError) as e:
            # Error in a file formatting
            self.connection.rollback()
            raise ValueError(f"Leases.upload_data: CSV file reading formating {e}")
        except Exception as db_error:
            # Handle database execution errors
            self.connection.rollback()
            raise ValueError(f"Leases.upload_data: Database connection error {db_error}")
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
    
    logger = AppLogger(name="Leases", log_file="logs/leases.log")
    logger.info("Application started successfully.")
    

    try:
        connection = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="secret555!",
                                database="community_management_prod"
                                )
        file_path = Path("data/leases.csv").resolve()
        table = Leases(connection)
        table.upload_data(file_path)
    except Exception as e:
        logger.error(f" Error in updating data. {e}")
        
    logger.info("Invoices completed.")   


if __name__=="__main__":
    main() 

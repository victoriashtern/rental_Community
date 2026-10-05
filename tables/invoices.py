from tables.table import Table
import csv

class Invoices(Table):    
    def __init__(self, connection):
        self.connection = connection

    def truncate(self):
        try:
            super().truncate("invoices")
        except ValueError as e:
            raise ValueError(f"Invoices.truncate: {e}")
        
    def delete(self):
        try:
            super().delete("invoices")
        except ValueError as e:
            raise ValueError(f"Invoices.delete: {e}")

    def create(self):
        try:
            sql = """    
                    CREATE TABLE `invoices` (
                        `invoice_id` int NOT NULL AUTO_INCREMENT,
                        `lease_id` int NOT NULL,
                        `amount` decimal(10,2) NOT NULL,
                        `due_date` date NOT NULL,
                        `paid_date` date DEFAULT NULL,
                        `invoice_type` enum('Rent','Utilities','Maintenance Fee','Penalty') DEFAULT 'Rent',
                        PRIMARY KEY (`invoice_id`),
                        KEY `lease_fk_idx` (`lease_id`),
                        CONSTRAINT `lease_fk` FOREIGN KEY (`lease_id`) REFERENCES `leases` (`lease_id`) ON DELETE CASCADE ON UPDATE CASCADE
                        ) ENGINE=InnoDB AUTO_INCREMENT=236 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

                """
            super().create(sql)
        except ValueError as e:
            raise ValueError(f"Invoices.create: {e}")
        
    def upload_data(self,filename):

        self.delete()
        try:
            # 1. Openning csv file
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)            
                cursor = self.connection.cursor()
                
                for row in reader:
                    invoice =( 
                            int(row["invoice_id"]) ,
                            int(row["lease_id"]) ,
                            float(row["amount"]) if row["amount"] else None,
                            row["due_date"] if row["due_date"] else None,
                            row["paid_date"] if row["paid_date"] else None,
                            row["invoice_type"] if row["invoice_type"] else None,
                            
                        )
                    sql = """
                        insert into invoices (invoice_id,lease_id,amount,due_date, paid_date, invoice_type) values 
                        (%s ,%s , %s,  %s, %s, %s)

                      """
                    cursor.execute(sql, invoice)
                            
            # commit data
            self.connection.commit()
        except (ValueError, KeyError) as e:
            # Error in a file formatting
            self.connection.rollback()
            raise ValueError(f"Invoices.upload_data: CSV file reading formating {e}")
        except Exception as db_error:
            # Handle database execution errors
            self.connection.rollback()
            raise ValueError(f"Invoices.upload_data: Database connection error {db_error}")
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
    
    logger = AppLogger(name="Invoices", log_file="logs/invoices.log")
    logger.info("Application started successfully.")
    

    try:
        connection = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="secret555!",
                                database="community_management_prod"
                                )
        file_path = Path("data/invoices.csv").resolve()
        table = Invoices(connection)
        table.upload_data(file_path)
    except Exception as e:
        logger.error(f" Error in updating data. {e}")
        
    logger.info("Invoices completed.")   


if __name__=="__main__":
    main()
from tables.table import Table
import csv

class Maintanances(Table):
    def __init__(self, connection):
        self.connection = connection
        super().__init__(connection)
        
    def truncate(self):
        try:
            super().truncate("maintenance")
        except ValueError as e:
            raise ValueError(f"Maintanance.truncate: {e}")

    def delete(self):
        try:
            super().delete("maintenance")
        except ValueError as e:
            raise ValueError(f"maintenance.delete: {e}")

    def create(self):
        try:
            sql = """    
                    CREATE TABLE `maintenance` (
                        `request_id` int NOT NULL AUTO_INCREMENT,
                        `apartment_id` int NOT NULL,
                        `tenant_id` int NOT NULL,
                        `category` enum('Plumbing','Electrical','HVAC','Appliance','Structural') NOT NULL,
                        `title` varchar(100) NOT NULL,
                        `description` text NOT NULL,
                        `priority` enum('Low','Medium','High','Emergency') DEFAULT 'Medium',
                        `status` enum('Submitted','Assigned','In Progress','Resolved','Cancelled') DEFAULT 'Submitted',
                        `cost` decimal(10,2) DEFAULT '0.00',
                        `resolved_at` datetime DEFAULT NULL,
                        PRIMARY KEY (`request_id`),
                        KEY `idx_maint_status` (`status`) /*!80000 INVISIBLE */,
                        KEY `fg_appartment_idx` (`apartment_id`),
                        KEY `fg_tenats_idx` (`tenant_id`),
                        CONSTRAINT `fg_appartment` FOREIGN KEY (`apartment_id`) REFERENCES `apartments` (`apartment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
                        CONSTRAINT `fg_tenats_mantanace` FOREIGN KEY (`tenant_id`) REFERENCES `tenants` (`tenant_id`) ON DELETE CASCADE ON UPDATE CASCADE
                        ) ENGINE=InnoDB AUTO_INCREMENT=731 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

                """
            super().create(sql)
        except ValueError as e:
            raise ValueError(f"Maintanace.create: {e}")

    def upload_data(self, filename):
        self.delete()
        try:
            # 1. Openning csv file
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)            
                cursor = self.connection.cursor()
                
                try:
                    # 2. Upload records to the database
                    for row in reader:
                        maintenance = (
                            int(row["request_id"]),
                            int(row["apartment_id"]),
                            int(row["tenant_id"]),
                            row["category"],
                            row["title"],
                            row["description"],
                            row["priority"],
                            row["status"],
                            float(row["cost"]) if row["cost"] else None,
                            row["resolved_at"] if row["resolved_at"] and row["resolved_at"] != 'NULL' else None,
                        )

                        sql = """
                            INSERT INTO maintenance
                            (
                                request_id,
                                apartment_id,
                                tenant_id,
                                category,
                                title,
                                description,
                                priority,
                                status,
                                cost,
                                resolved_at
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(sql, maintenance)

                    # commit data
                    self.connection.commit()
                    
                except (ValueError, KeyError) as e:
                    # Error in a file formatting
                    self.connection.rollback()
                    raise ValueError(f"Maintanance.upload_data: CSV file reading formating {e}")
                    
                except Exception as db_error:
                    # Handle database execution errors
                    self.connection.rollback()
                    raise ValueError(f"Maintanance.upload_data: Database connection error {db_error}")
                finally:
                    # Close the cursor
                    cursor.close()

        except FileNotFoundError:
            raise ValueError(f"Maintanance.upload_data: File {filename} not found")
        except OSError as e:
            raise ValueError(f"Maintanance.upload_data: Writing to a file {filename} error {e}")


def main():
    import mysql.connector
    from pathlib import Path
    import sys
    # Force Python to look in the parent folder (rental_community)
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from logger.log import  AppLogger
    
    logger = AppLogger(name="Maintenance", log_file="logs/maintenances.log")
    logger.info("Application started successfully.")
    

    
    try:
        connection = mysql.connector.connect(
                                host="localhost",
                                user="root2",
                                password="secret555!",
                                database="community_management_prod"
                                )
        file_path = Path("data/maintenances.csv").resolve()
        table = Maintanances(connection)
        table.upload_data(file_path)
    except Exception as e:
        logger.error(f" Error in updating data. {e}")
        
    logger.info("Maintananmce completed.")   


if __name__=="__main__":
    main()
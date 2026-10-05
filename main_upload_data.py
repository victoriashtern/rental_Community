from database.connection import Database
from tables.buildings import Buildings
from tables.apartments import Apartments
from tables.tenates import Tenates
from tables.leases import Leases
from tables.maintanances import Maintanances
from tables.invoices import Invoices


from logger.log import  AppLogger
import os
from pathlib import Path
import csv


def if_file_exist(filename):
    if not filename.is_file():
        print(f"file not exists {filename}")
        return -1
    return 1

def clear_tables(connection):
    try:
        building = Buildings(connection)
        building.delete()
        
        apartments = Apartments(connection)
        apartments.delete()
        
        leases = Leases(connection)
        leases.delete()
        
        tenates = Tenates(connection)
        tenates.delete()
        
        maintanances = Maintanances(connection)
        maintanances.delete()
    except Exception as e:
        raise ValueError(f"Clear_tables Error in clear tables. {e}")
        

def upload_all_data(connection,configuration):

    try:
        table = Buildings(connection)
        filename = Path(f"data/{configuration["buildings"]}").resolve()
        if (if_file_exist(filename)):
            table.upload_data(filename)

        table = Apartments(connection)
        filename = Path(f"data/{configuration["apartments"]}").resolve()
        if (if_file_exist(filename)):
            table.upload_data(filename)

        table = Tenates(connection)
        filename = Path(f"data/{configuration["tenates"]}").resolve()
        if (if_file_exist(filename)):
            table.upload_data(filename)

        table = Leases(connection)
        filename = Path(f"data/{configuration["leases"]}").resolve()
        if (if_file_exist(filename)):
            table.upload_data(filename)

        table = Maintanances(connection)
        filename = Path(f"data/{configuration["maintenances"]}").resolve()
        if (if_file_exist(filename)):
            table.upload_data(filename)

        table = Invoices(connection)
        filename = Path(f"data/{configuration["invoices"]}").resolve()
        if (if_file_exist(filename)):
            table.upload_data(filename)

    except Exception as e:
            raise ValueError(f"Upload_all_data Error uploading data. {e}")

def main():
    logger = AppLogger(name="Rental-Property", log_file="logs/rental.log")
    # Log various types of messages
    logger.info("Rental Community started successfully.")

    configuration ={
                    "invoices":"invoices.csv",
                    "apartments":"apartments.csv",
                    "maintenances":"maintenances.csv",
                    "tenates":"tenates.csv",
                    "leases":"leases.csv",
                    "buildings":"buildings.csv",
                    }
    try:
        #create database
        database = Database("config/config.json")
        #clear tablea
        clear_tables(database.get_connection())
        #upload all data
        upload_all_data(database.get_connection(),configuration)
    except Exception as e:
        logger.error(f"Main_upload_data.clear_tables Error in clear tables. {e}")

    logger.info(f"Rental_community.Completed uploading")
    

    


    exit()


    

    print("done")

if __name__=="__main__":
    main()
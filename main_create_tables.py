from database.connection import Database
from tables.buildings import Buildings
from tables.apartments import Apartments
from tables.tenates import Tenates
from tables.leases import Leases
from tables.maintanances import Maintanances
from tables.invoices import Invoices

from logger.log import  AppLogger
import os

def create_tables(connection):
    try:
        building = Buildings(connection)
        building.create()
        
        apartments = Apartments(connection)
        apartments.create()
        
        tenates = Tenates(connection)
        tenates.create()
        
        leases = Leases(connection)
        leases.create()
        
        maintanances = Maintanances(connection)
        maintanances.create()

        invoices = Invoices(connection)
        invoices.create()
    except Exception as e:
        raise ValueError(f"Create_tables Error in clear tables. {e}")
        

    except Exception as e:
            raise ValueError(f"Upload_all_data Error uploading data. {e}")

def main():
    logger = AppLogger(name="Rental-Property-Create-Tables", log_file="logs/rental.log")
    # Log various types of messages
    logger.info("Rental Community Create Tables started successfully.")

    try:
        #create database
        database = Database("config/config.json")
        #clear tablea
        create_tables(database.get_connection())
        
    except Exception as e:
        logger.error(f"Main_create_tables.main Error in creating tables. {e}")

    logger.info(f"Rental Community.Completed ")
    

    



    

    print("done")

if __name__=="__main__":
    main()
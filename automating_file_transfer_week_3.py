''' You work at a company that receives daily data files from external partners. These files need to be processed and analyzed, but first, they need to be transferred to the company's internal network.

The goal of this project is to automate the process of transferring the files from an external FTP server to the company's internal network.

Here are the steps you can take to automate this process:

    Use the ftplib library to connect to the external FTP server and list the files in the directory.

    Use the os library to check for the existence of a local directory where the files will be stored.

    Use a for loop to iterate through the files on the FTP server and download them to the local directory using the ftplib.retrbinary() method.

    Use the shutil library to move the files from the local directory to the internal network.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the files that have been transferred and any errors that may have occurred during the transfer process. '''
from ftplib import FTP, error_perm
import os
import shutil
import logging
import time
import schedule


# Ftp server's domain name or ip address
FTP_SERVER = 'test.rebex.net'
# Ftp port number
PORT = '21'
# The directory where the daily files located in the ftp server
FTP_REMOTE_DIRECTORY = 'pub/example'
# Get the user and password from the environment variables FTP_USER and PASS. Protecting the credentials from being stored in the script
FTP_USER = os.getenv('FTP_USER') 
FTP_PASS = os.getenv('PASS')
# The local directory where the downloaded ftp files should be stored temporary
LOCAL_DIRECTORY = 'backup_directory'
# The shared directory for other systems in the internal network
NETWORK_SHARED_DIRECTORY = "nfs_shared_directory"


def download_files_by_ftp_to_local_directory():
    # Connect to FTP server
    print("Connecting to the ftp server")
    ftp_connection = FTP(FTP_SERVER)
    # Login to FTP server
    print("Logging in to the ftp server")
    ftp_connection.login(FTP_USER,FTP_PASS)
    # Get the welcome message from the server
    print("Welcome message: " + ftp_connection.getwelcome())
    # Change the FTP working directory 
    print(f"Changing the ftp working directory to {FTP_REMOTE_DIRECTORY}")
    ftp_connection.cwd(FTP_REMOTE_DIRECTORY)
    # Get the list of files
    filelist = ftp_connection.nlst()

    for filename in filelist:
        # Open the file for writing in the binary mode because "retrbinary" retrieve the data from ftp server in binary mode
        # os.path.join to join the path segments intelligently for different operating system
        with open(os.path.join(LOCAL_DIRECTORY,filename), 'wb') as downloaded_file:
            # Retrieve the file from the ftp server
            print(f"Downloading {filename} to {LOCAL_DIRECTORY}")
            logger.info(f"Downloading {filename} to {LOCAL_DIRECTORY}")
            ftp_connection.retrbinary("RETR " + filename ,downloaded_file.write)

    # Close the ftp connection
    print("Closing the ftp connection")
    ftp_connection.close()



def move_file_by_shutil_to_network_shared_directory():

    # Walk through all file in local directory
    for _, _, filenames in os.walk(LOCAL_DIRECTORY):
        # Move all files in the filenames to network shared directory
        for filename in filenames:
            print(f"Moving {filename} to {NETWORK_SHARED_DIRECTORY}") 
            logger.info(f"Moving {filename} to {NETWORK_SHARED_DIRECTORY}") 
            shutil.move(os.path.join(LOCAL_DIRECTORY, filename), os.path.join(LOCAL_DIRECTORY, NETWORK_SHARED_DIRECTORY))

def transfer_daily_files_from_ftp_to_local_network():
    print("Task has Started")
    logger.info("Task has Started")
    try:
        # check if the local directory exists. Create it if doesn't exist
        if not os.path.exists(LOCAL_DIRECTORY):
            os.mkdir(LOCAL_DIRECTORY)
        # Start downloading file from ftp server
        download_files_by_ftp_to_local_directory()
        # Check if the network shared folder exist
        if not os.path.exists(NETWORK_SHARED_DIRECTORY):
            # Create the directory if it doesn't exist
            os.mkdir(NETWORK_SHARED_DIRECTORY)
        # Start moving files
        move_file_by_shutil_to_network_shared_directory()

    except error_perm as e:
        # Ftp user cannot log in error
        print(e)
        logging.error(e)    
    except Exception as e:
        print(e)
        logging.error(e)
    else:
        print("Task finished successfully")
        # If there is no exception, write to log file with INFO log level
        logger.info("Task finished successfully")


# Schedule the task to be run every day at 7:46 PM
schedule.every().day.at("19:46").do(transfer_daily_files_from_ftp_to_local_network)

# Configure logging to log events to events.log file with the specified format.
logging.basicConfig(filename='events.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

# Loggers should NEVER be instantiated directly, but always through the module-level function logging.getLogger. A good convention to use when naming loggers is to use a module-level logger
logger=logging.getLogger(__name__)

# Keep the script running 
while True:
    # Run all jobs that are scheduled to run
    schedule.run_pending()
    time.sleep(1)





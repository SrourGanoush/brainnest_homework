''' You work at a company that sends daily reports to clients via email. The goal of this project is to automate the process of sending these reports via email.

Here are the steps you can take to automate this process:

    Use the smtplib library to connect to the email server and send the emails.

    Use the email library to compose the email, including the recipient's email address, the subject, and the body of the email.

    Use the os library to access the report files that need to be sent.

    Use a for loop to iterate through the list of recipients and send the email and attachment.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the emails that have been sent and any errors that may have occurred during the email sending process. '''


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import schedule
import time
import logging
import os


def create_message(sender_email, receiver_name, receiver_email):
    # Create MIME Multipart email. Allowing for attachments to be included in the email
    message = MIMEMultipart()
    message["Subject"] = "Daily Report"
    message["From"] = sender_email
    message["To"] = receiver_email
    # Body of the message
    body = f"""Hi {receiver_name},\n\nHere is the daily report. \n\nBest Regards """
    message.attach(MIMEText(body,'plain'))

    # Attach all reports in specific folder
    # Get all filenames
    file_list = os.listdir("generated_reports_folder")
    for report_file_name in file_list:
        # Add each file in the folder to the message
        part = add_attachment(os.path.join("generated_reports_folder", report_file_name))
        message.attach(part)

    return message.as_string()

def add_attachment(report_file_path):

    # Get the filename part of the path
    report_file_name = os.path.basename(report_file_path)
    # Open the binary file
    with open(report_file_path, "rb") as attachment:
        # Add the binary file with application/octet-stream content-type
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode the binary file into printable ASCII characters
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {report_file_name}",
    )

    return part



def send_daily_report_by_email():
    print("Task has Started")
    logger.info("Task has Started")
    try: # To catch errors and handle them by writing to a log file
        port = 587 # Default mail submission port
        smtp_server = "" # mail server's domain name or IP address
        sender_email = ""   
        receiver_email = ""
        # Get the password from the environment variable PASS. Protecting the password from being stored in the script
        password = os.getenv('PASS')

        # Warning. This is only for test. Creating unverified context to bypass 'ssl.SSLCertVerificationError'
        context = ssl._create_unverified_context()
        # Create SMTP object and passing the server's domain name or IP address, plus the port number
        with smtplib.SMTP(smtp_server, port) as server:
            # Establish a connection to the server
            server.ehlo()
            # Start TLS Encryption. Put the SMTP connection in TLS mode
            server.starttls(context=context)
        
            # Logging In to the server
            server.login(sender_email, password)
             # Read csv file containing names with emails
            with open('email_list.csv','r') as email_list_csv:
                email_list = csv.reader(email_list_csv)

                for receiver_name, receiver_email in email_list:
                    # Create email message with attachments
                    message = create_message(sender_email, receiver_name, receiver_email)
                    
                    # Send the email
                    send_result = server.sendmail(sender_email, receiver_email, message) 
                    # If the server responded with reception doesn't exist 
                    if len(send_result):
                        logger.error("{receiver_email} does not exist")



    except smtplib.SMTPAuthenticationError as e:
    # Handling incorrect password exception
        print(f'Wrong Credentials.\n{e.smtp_error}')
        logger.error(e)
        # Stop the script completely because of the authentication problem
        exit(1)

    except Exception as e:
        print(e)
        # Write to log file with ERROR log level
        logger.error(e)

    else:
        print("Task finished successfully")
        # If there is no exception, write to log file with INFO log level
        logger.info("Task finished successfully")


# Schedule the task to be run every day at 8:25 PM
schedule.every().day.at("20:25").do(send_daily_report_by_email)

# Configure logging to log events to messages.log file with the specified format.
logging.basicConfig(filename='messages.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

# Loggers should NEVER be instantiated directly, but always through the module-level function logging.getLogger. A good convention to use when naming loggers is to use a module-level logger
logger=logging.getLogger(__name__)
# Keep the script running 
while True:
    # Run all jobs that are scheduled to run
    schedule.run_pending()
    time.sleep(1)


# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Email details
# EMAIL_FROM = "rajatnirmalkar35@gmail.com"  # Replace with your email
# EMAIL_PASSWORD = "wuasmpxkeykbemjy "  # Replace with your email password
# EMAIL_TO = "rajatnirmalkar5@gmail.com"  # Replace with recipient email

# def send_email(subject, body, attachment_path=None):
#     """
#     Send an email with the report as an attachment.
#     """
#     try:
#         # Create the email
#         msg = MIMEMultipart()
#         msg["From"] = EMAIL_FROM
#         msg["To"] = EMAIL_TO
#         msg["Subject"] = subject

#         # Attach the body
#         msg.attach(MIMEText(body, "plain"))

#         # Attach the report file
#         if attachment_path:
#             with open(attachment_path, "r") as file:
#                 attachment = MIMEText(file.read(), "plain")
#                 attachment.add_header("Content-Disposition", "attachment", filename=attachment_path)
#                 msg.attach(attachment)

#         # Send the email
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(EMAIL_FROM, EMAIL_PASSWORD)
#             server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
#         logging.info("Email sent successfully.")
#     except Exception as e:
#         logging.error(f"Failed to send email: {str(e)}")

# if __name__ == "__main__":
#     # Replace with the path to your report file
#     report_filename = "mongodb_report_20250316_112812.txt"

#     # Send the email
#     send_email(
#         subject="MongoDB Resource Allocation Report",
#         body="Please find the attached MongoDB resource allocation report.",
#         attachment_path=report_filename
#     )

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
import os
import argparse
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_email(email_from, email_password, email_to, report_dir):
    """
    Send an email with attachments.
    """
    try:
        # Read the list of generated files
        with open(os.path.join(report_dir, "generated_files.txt"), "r") as f:
            report_files = f.read().splitlines()

        msg = MIMEMultipart()
        msg["From"] = email_from
        msg["To"] = ", ".join(email_to.split(","))  # Handle multiple recipients
        msg["Subject"] = "MongoDB Resource Allocation Report"

        # Attach the body
        msg.attach(MIMEText("Please find the attached MongoDB resource allocation report and visualizations.", "plain"))

        # Attach files
        for attachment in report_files:
            with open(attachment, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
                msg.attach(part)

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_from, email_password)
            server.sendmail(email_from, email_to.split(","), msg.as_string())
        logging.info("Email sent successfully.")

        # Clean up the reports folder
        shutil.rmtree(report_dir)
        logging.info(f"Reports folder {report_dir} cleaned up.")
    except Exception as e:
        logging.error(f"Failed to send email or clean up reports folder: {str(e)}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Send MongoDB resource allocation reports via email.")
    parser.add_argument("--email_from", required=True, help="Sender email address")
    parser.add_argument("--email_password", required=True, help="Sender email password")
    parser.add_argument("--email_to", required=True, help="Comma-separated list of recipient email addresses")
    parser.add_argument("--report_dir", default="reports", help="Directory containing report files (default: 'reports')")
    args = parser.parse_args()

    send_email(args.email_from, args.email_password, args.email_to, args.report_dir)
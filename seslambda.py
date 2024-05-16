import boto3
import csv

# Initialize the boto3 clients for S3 and SES
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

def lambda_handler(event, context):
    # Specify the name of the S3 bucket containing the CSV file and email template
    bucket_name = 'email-marketing-3'

    try:
        # Retrieve the CSV file from S3
        csv_file = s3_client.get_object(Bucket=bucket_name, Key='contacts.csv')
        lines = csv_file['Body'].read().decode('utf-8').splitlines()
        
        # Retrieve the HTML email template from S3
        email_template = s3_client.get_object(Bucket=bucket_name, Key='email_template.html')
        email_html = email_template['Body'].read().decode('utf-8')
        
        # Parse the CSV file to extract contact information
        contacts = csv.DictReader(lines)
        
        # Iterate over each contact in the CSV file
        for contact in contacts:
            # Replace placeholders in the email template with contact-specific information
            personalized_email = email_html.replace('{{Name}}', contact['FirstName'])
            
            # Send the personalized email to the contact's email address using SES
            response = ses_client.send_email(
                Source='tiplegroup@gmail.com',  # Sender's email address
                Destination={'ToAddresses': [contact['Email']]},  # Recipient's email address
                Message={
                    'Subject': {'Data': 'Your Weekly Tiny Tales Mail!', 'Charset': 'UTF-8'},  # Email subject
                    'Body': {'Html': {'Data': personalized_email, 'Charset': 'UTF-8'}}  # Email body
                }
            )
            # Print confirmation message
            print(f"Email sent to {contact['Email']}: Response {response}")
    except Exception as e:
        # Handle any errors that occur during execution
        print(f"An error occurred: {e}")

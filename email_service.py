"""For managing email related services."""

import os
import traceback
import airtable
from apscheduler.schedulers.background import BackgroundScheduler


AIRTABLE_BASE = os.getenv('AIRTABLE_BASE')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')

minute_jobs = []

class BaseEmailConfig:
  MAIL_SERVER = os.getenv('MAIL_SERVER', 'smpt.gmail.com')
  # MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mailgun.org')
  MAIL_PORT = os.getenv('MAIL_SERVER_PORT', 2525)
  MAIL_USERNAME = os.getenv('MAIL_USERNAME')
  MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

def start_email_service():
  """Get emails specifications based on Airtable EMAILS Table"""
  airtable_emails = airtable.Airtable(AIRTABLE_BASE, 'emails', AIRTABLE_API_KEY)
  email_specs = airtable_emails.get_all(view='Grid view')
  # TODO: add message specifically when error is because of templeting error
  # print(email_specs)

  for record in email_specs:
    if int(record['fields']['Frequency in Minutes']) == 1:
      minute_jobs.append(record)

  sched = BackgroundScheduler(daemon=True)
  sched.add_job(each_minute,'interval',seconds=10)
  sched.start()

def each_minute():
  print("Minute Scheduler is alive!")
  for record in minute_jobs:
    table_name = record['fields']['Table Name']
    message = record['fields']['Message']
    variables = record['fields']['Variables'].split(',')
      
    send_confirmation_emails(table_name, message, variables)

def send_confirmation_emails(table_name: str, message_template: str, variables_arr: []):
  """Send confirmation emails to all the To Process folks.

  Should look something like:
      1. get all records which haven't gotten emails or errors
      2. iterate through the records
      2a. send the emails
      2a1. try: sending the email
      2a2. except: error sending the email
      2a3. mark the error that was found
      2b. mark the records as processed
    
  """
  table = airtable.Airtable(AIRTABLE_BASE, table_name, AIRTABLE_API_KEY)
  to_process = table.get_all(view='To process')
  # print(to_process)

  for record in to_process:
    try:
      print(record)
      email = record['fields']['Email']
      msg = build_confirmation_msg(message_template, variables_arr, record)
      print(msg)
      send_email(email, msg)
        # verify this works to mark the record as processed:
      fields = {'Processed': True}
      table.update(record['id'], fields)
    except Exception as e:
      print(f"Error sending email: {traceback.print_tb(e.__traceback__)}")
      fields = {'Error': str(traceback.format_exc())}
      table.update(record['id'], fields)

def build_confirmation_msg(message_template: str, variables_arr: [], record):
  """Returns the full confirmation email as a string
  Note: some email services also support sending HTML for future purposes.
  """
  inserts = []
  for variable in variables_arr:
    inserts.append(record['fields'][variable.strip()])
  message = message_template.format(*inserts)
  # print(message)

  return message

def send_email(to: str, msg: str):
  """Send an email with the provided msg to the given address from: TODO:(default `from` email here)
  """

  # send email
  pass
  
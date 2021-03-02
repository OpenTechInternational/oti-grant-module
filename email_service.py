"""For managing email related services."""


def build_confirmation_msg(name: str):
  """Returns the full confirmation email as a string
  
  Note: some email services also support sending HTML for future purposes.
  """

  return f"This is a default confirmation email for {name}"

def send_email(to: str, msg: str):
  """Send an email with the provided msg to the given address from: TODO:(default `from` email here)
  """

  # send email
  pass
  
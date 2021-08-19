import smtplib
import os
from get_docker_secret import get_docker_secret


def send_activation_link(to_email, token):
    gmail_user = get_docker_secret(os.environ['EMAIL_ADDRESS'])
    sent_from = get_docker_secret(os.environ['EMAIL_ADDRESS'])
    gmail_password = get_docker_secret(os.environ['EMAIL_PASSWORD'])

    to = [to_email]
    subject = 'Parkr Activation Link'
    body = """\
    Hello and thanks for registration!\n
    Here is your activation link:\n
    %s\n\n
    """ % ('http://localhost:5000/api/users/activate/' + token)

    email_text = '\r\n'.join(['To: %s' % ','.join(to),
                              'From: %s' % sent_from,
                              'Subject: %s' % subject,
                              '', body])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
    except:
        raise Exception("Sending email failed")


def send_activation_link_with_password(to_email, token, password):
    gmail_user = get_docker_secret(os.environ['EMAIL_ADDRESS'])
    sent_from = get_docker_secret(os.environ['EMAIL_ADDRESS'])
    gmail_password = get_docker_secret(os.environ['EMAIL_PASSWORD'])

    to = [to_email]
    subject = 'Parkr Activation Link'
    body = f"""\
    Hello and thanks for registration!\n
    Your password is: {password}
    Here is your activation link:\n
    %s\n\n
    """ % ('http://localhost:5000/api/users/activate/' + token)

    email_text = '\r\n'.join(['To: %s' % ','.join(to),
                              'From: %s' % sent_from,
                              'Subject: %s' % subject,
                              '', body])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
    except:
        raise Exception("Sending email failed")

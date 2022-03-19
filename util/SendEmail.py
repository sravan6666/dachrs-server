import sendgrid
from os import environ as env
from sendgrid.helpers.mail.content import Content
from sendgrid.helpers.mail.email import Email
from sendgrid.helpers.mail.mail import Mail
from sendgrid.helpers.mail.to_email import To

sg = sendgrid.SendGridAPIClient(api_key=env['SENDGRID_API_KEY'])


class SendEmail(object):

    def sendEmail(to_email, subject, body):
        from_email = Email("no-reply-kanban@aiceresoft.com")
        to_email = To(to_email)
        content = Content("text/html", body)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return response
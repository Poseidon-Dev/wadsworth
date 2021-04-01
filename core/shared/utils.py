import discord
import core.config
import smtplib, ssl
from email.message import EmailMessage

def pretty_ping(ctx, name):
    """
    Returns an embed for pings for a prettier discord format
    """
    embed = discord.Embed(color=0x333333,
        timestamp=ctx.message.created_at)
    embed.set_footer(text=f"'{name}' ping request by {ctx.message.author}")
    return embed

def send_email(subject, message, to=core.config.EMAIL_TO):
    port = core.config.EMAIL_SMTP_PORT
    smtp_server = core.config.EMAIL_SMTP
    sender = core.config.EMAIL_UID
    password = core.config.EMAIL_PWD
    recipient = core.config.EMAIL_TO

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    print(to)
    msg.set_content(message)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print('Email Message Sent')
    except Exception as e:
        print(f'Email did not send: {e}')
        
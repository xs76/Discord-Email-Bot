import discord
from discord.ext import commands
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtpserver.provider.com"
SMTP_PORT = providerport  
SMTP_USERNAME = "you@domain.com"  
SMTP_PASSWORD = "youremailpassword"  


intents = discord.Intents.default()
bot = commands.Bot(intents=intents, command_prefix="!", description="Email Bot")

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game("commands")
    )
    print(f"Sucessfully launched Discord Email Bot Logged in as: {bot.user}")


def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)


@bot.slash_command(name="email", description="Send an email using an template")
async def already(ctx, reason: str, person_name: str, person_email: str):
    await ctx.defer()  
    
    subject = f"Reply - {person_name}"
    body = f"""
Hello, {person_name}!

Sorry I havent replied, I was out of state for {reason}

- My Dearest Apoligies!
"""
    success, error = send_email(person_email, subject, body)
    if success:
        await ctx.send(f"Mail successfully sent to **{person_email}**.")
    else:
        await ctx.send(f"Failed to send email. Error: **{error}**")


bot.run("bottoken")

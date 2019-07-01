import smtplib
import requests
import csv
from bs4 import BeautifulSoup as soup
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random as rand


fs_blog = "https://fs.blog/mental-models/"
page_response = requests.get(fs_blog, timeout = 5)
page_content = soup(page_response.content, "html.parser")

#get paragraphs, headers and header links and store in dataframe?
paragraphs = page_content.find_all("p")
strongs = page_content.find_all("strong")

row_number, titles, links, count = [], [], [], 0
for i in strongs:
        try:
            count += 1
            row_number.append(count)
            titles.append(i.text)
            try:
                links.append(i.find('a')["href"])
            except:
                links.append("No link available")
        except:
            break

textContent = []
for i in paragraphs:
    try:
        textContent.append(i.text)
    except:
        break
print (len(titles), len(textContent), len(links)) #120, 234, 120


f = open("EmailAuthentication.txt", 'r')
lines = f.read().splitlines()

#delete first 9 paragraphs/only send paragraphs from 10 onwards
sender_email = lines[0]
receiver_email = lines[0]
password = lines[1]

print (sender_email, password)

message = MIMEMultipart("alternative")
message["Subject"] = "Daily Mental Models"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
{title1} {title2} {link1}
{p1}
{p2}
{p3}
""".format(title1 = titles[rand.randint(0, len(titles))], title2 = titles[rand.randint(0, len(titles))],
    link1 = links[rand.randint(0, len(links))], p1 = textContent[rand.randint(10, len(textContent))],
    p2 = textContent[rand.randint(10, len(textContent))], p3 = textContent[rand.randint(10, len(textContent))])
html = """\
<html>
  <body>
    <p>
        <strong>Lollapalooza</strong>
        <br>
        {title1}
        <br>{title2}
        <br>{link1}
    </p>
        {p1}
        <br>
        
        </br>
        {p2}
        <br>

        </br>
        {p3}
    </p
  </body>
</html>
""".format(title1 = titles[rand.randint(0, len(titles))], title2 = titles[rand.randint(0, len(titles))],
    link1 = links[rand.randint(0, len(links))], p1 = textContent[rand.randint(10, len(textContent))],
    p2 = textContent[rand.randint(10, len(textContent))], p3 = textContent[rand.randint(10, len(textContent))])

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create connection with server and send email
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#server.starttls()
server.login(sender_email, password)
server.sendmail(sender_email, receiver_email, message.as_string())
server.quit()

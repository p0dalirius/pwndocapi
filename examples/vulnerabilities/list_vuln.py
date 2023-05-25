import pwndocapi

p = pwndocapi.pwndoc("192.168.1.19", 8443, verbose=True)
p.login("username", "password")

langs = p.data.languages()

for lang in langs:
    print(p.vulnerabilities.list(lang))
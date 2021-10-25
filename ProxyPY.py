def settings (file):
    print("\nConfiguring settings ...")
    #   The option below identifies how the ProxyList is treated.
    #   only one option should be uncommented at time,
    #   otherwise the last appearing option will be accepted

    file.write("dynamic_chain\n");print("dynamic_chain");
    #   Dynamic - Each connection will be done via chained proxies
    #   all proxies chained in the order as they appear in the list
    #   at least one proxy must be online to play in chain
    #   (dead proxies are skipped)
    #   otherwise EINTR is returned to the app

    #file.write("strict_chain\n");print("strict_chain\n")
    #   Strict - Each connection will be done via chained proxies
    #   all proxies chained in the order as they appear in the list
    #   all proxies must be online to play in chain
    #   otherwise EINTR is returned to the app

    file.write("random_chain\n");print("random_chain");
    #   Random - Each connection will be done via random proxy
    #   (or proxy chain, see  chain_len) from the list.
    #   this option is good to test your IDS :)

    #   Make sense only if random_chain 
    #file.write("chain_len = "+chain_len+"\n");print("chain_len = "+chain_len+"\n")

    #   Quiet mode (no output from library) 
    #file.write("quiet_mode\n");print("quiet_mode\n")

    #   Proxy DNS requests - no leak for DNS data
    file.write("proxy_dns \n");print("proxy_dns");

    #   Some timeouts in milliseconds   
    file.write("tcp_read_time_out 15000\n");print("tcp_read_time_out 15000");
    file.write("tcp_connect_time_out 8000\n");print("tcp_connect_time_out 8000");

    #   ProxyList format
    #   type  host  port [user pass]
    #   (values separated by 'tab' or 'blank')
    #       Examples:
    #       socks5	192.168.67.78	1080	lamer	secret
    #       http	192.168.89.3	8080	justu	hidden
    #       socks4	192.168.1.49	1080
    #       http	192.168.39.93	8080	
    #   proxy types: http, socks4, socks5
    #   ( auth types supported: "basic"-http  "user/pass"-socks )
    file.write("[ProxyList]");

def getProxy (file, localproxy):
    url = "https://api.getproxylist.com/proxy"
    connection = urllib.request.urlopen(url)
    print("Connection extablished")
    data = json.loads(connection.read())
    try:
        protocol = str(data["protocol"])
        ip = str(data["ip"])
        port = str(data["port"])
        print("Packets recieved")
        proxy = protocol+"\t"+ip+"\t"+port
        print(proxy+"\n")
        file.write("\n"+proxy)
    except:
        print (data["error"])
        exit()

import urllib.requests, json 
print("Creating proxychains.conf")
file = open("proxychains.conf", 'w')
settings(file)
print("\nAdding proxies ...")
max_chain_len=10
localproxy = {}
for x in range(0, max_chain_len):
    localproxy = getProxy(file, localproxy)
file.close()

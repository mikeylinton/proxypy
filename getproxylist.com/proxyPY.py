import urllib.request, json 

def settings (file):
    # proxychains.conf  VER 4
    #
    #        HTTP, SOCKS4, SOCKS5 tunneling proxifier with DNS.
    #
    print("\nConfiguring settings ...")
    #   The option below identifies how the ProxyList is treated.
    #   only one option should be uncommented at time,
    #   otherwise the last appearing option will be accepted

    file.write("dynamic_chain\n");print("dynamic_chain")
    #   Dynamic - Each connection will be done via chained proxies
    #   all proxies chained in the order as they appear in the list
    #   at least one proxy must be online to play in chain
    #   (dead proxies are skipped)
    #   otherwise EINTR is returned to the app

    # file.write("strict_chain\n");print("strict_chain\n")
    #   Strict - Each connection will be done via chained proxies
    #   all proxies chained in the order as they appear in the list
    #   all proxies must be online to play in chain
    #   otherwise EINTR is returned to the app

    # file.write("random_chain\n");print("random_chain") 
    #   Random - Each connection will be done via random proxy
    #   (or proxy chain, see  chain_len) from the list.
    #   this option is good to test your IDS :)

    #   Make sense only if random_chain 
    #chain_len=2;file.write("chain_len = "+str(chain_len)+"\n");print("chain_len = "+str(chain_len)+"\n")

    #   Quiet mode (no output from library) 
    # file.write("quiet_mode\n");print("quiet_mode\n")

    #   Proxy DNS requests - no leak for DNS data
    file.write("proxy_dns \n");print("proxy_dns")

    
    # set the class A subnet number to usefor use of the internal remote DNS mapping
    # we use the reserved 224.x.x.x range by default,
    # if the proxified app does a DNS request, we will return an IP from that range.
    # on further accesses to this ip we will send the saved DNS name to the proxy.
    # in case some control-freak app checks the returned ip, and denies to 
    # connect, you can use another subnet, e.g. 10.x.x.x or 127.x.x.x.
    # of course you should make sure that the proxified app does not need
    # *real* access to this subnet. 
    # i.e. dont use the same subnet then in the localnet section
    # file.write("remote_dns_subnet 127\n");print("remote_dns_subnet 127") 
    # file.write("remote_dns_subnet 10\n");print("remote_dns_subnet 10") 
    file.write("remote_dns_subnet 224\n");print("remote_dns_subnet 224")

    #   Some timeouts in milliseconds   
    file.write("tcp_read_time_out 15000\n");print("tcp_read_time_out 15000")
    file.write("tcp_connect_time_out 8000\n");print("tcp_connect_time_out 8000")

        
    # By default enable localnet for loopback address ranges
    # RFC5735 Loopback address range
    file.write("localnet 127.0.0.0/255.0.0.0\n");print("localnet 127.0.0.0/255.0.0.0") 
    # RFC1918 Private Address Ranges
    # file.write("localnet 10.0.0.0/255.0.0.0\n");print("localnet 10.0.0.0/255.0.0.0")
    # file.write("localnet 172.16.0.0/255.240.0.0\n");print("localnet 172.16.0.0/255.240.0.0")
    # file.write("localnet 192.168.0.0/255.255.0.0\n");print("localnet 192.168.0.0/255.255.0.0")


    # Example for localnet exclusion
    ## Exclude connections to 192.168.1.0/24 with port 80
    # file.write("localnet 192.168.1.0:80/255.255.255.0\n");print("localnet 192.168.1.0:80/255.255.255.0")

    ## Exclude connections to 192.168.100.0/24
    # file.write("localnet 192.168.100.0/255.255.255.0\n");print("localnet 192.168.100.0/255.255.255.0")

    ## Exclude connections to ANYwhere with port 80
    # file.write("localnet 0.0.0.0:80/0.0.0.0\n");print("localnet 0.0.0.0:80/0.0.0.0")


    ### Examples for dnat
    ## Trying to proxy connections to destinations which are dnatted,
    ## will result in proxying connections to the new given destinations.
    ## Whenever I connect to 1.1.1.1 on port 1234 actually connect to 1.1.1.2 on port 443
    # file.write("dnat 1.1.1.1:1234  1.1.1.2:443\n");print("dnat 1.1.1.1:1234  1.1.1.2:443")

    ## Whenever I connect to 1.1.1.1 on port 443 actually connect to 1.1.1.2 on port 443
    ## (no need to write :443 again)
    # file.write("dnat 1.1.1.2:443  1.1.1.2\n");print("dnat 1.1.1.2:443  1.1.1.2")

    ## No matter what port I connect to on 1.1.1.1 port actually connect to 1.1.1.2 on port 443
    # file.write("dnat 1.1.1.1  1.1.1.2:443\n");print("dnat 1.1.1.1  1.1.1.2:443")

    ## Always, instead of connecting to 1.1.1.1, connect to 1.1.1.2
    # file.write("dnat 1.1.1.1  1.1.1.2\n");print("dnat 1.1.1.1  1.1.1.2")

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
    file.write("[ProxyList]") 

def getProxy (file):
    url = "https://api.getproxylist.com/proxy?anonymity[]=high%20anonymity&allowsHttps=1"
    connection = urllib.request.urlopen(url)
    print("Connection extablished")
    data = json.loads(connection.read())
    try:
        protocol = str(data["protocol"])
        ip = str(data["ip"])
        port = str(data["port"])
        print("Packets recieved")
        proxy = protocol+" "+ip+" "+port
        print(proxy+"\n")
        file.write("\n"+proxy)
    except:
        print (data["error"])
        exit()

if __name__ == "__main__":
    print("Creating proxychains.conf")
    file = open("proxychains.conf", 'w')
    settings(file)
    print("\nAdding proxies ...")
    max_chain_len=10
    for x in range(0, max_chain_len):
        getProxy(file)
    file.write("\nsocks4 127.0.0.1 9050")
    file.close()
import urllib.request


def readDataFrom(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read()
    data = data.decode('utf-8')

    data=data.replace('\n','')
    return data


def run():
    print("Running task")
    with open("resource.res","r") as f:
        content=f.read().split("\n")
        result=""
        head = "https://www.walletexplorer.com/wallet/"
        tail = "&format=csv"
        for c in content:
            if(c!=""):
                file = readDataFrom(c)
                filename=c.replace(head,"").replace(tail,"")+".csv"
                with open(filename,"w",encoding="utf-8") as ff:
                    ff.write(file)
                result+=(c)+"\n"
    print("finish task")
    return result

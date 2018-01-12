from socket import socket, AF_INET, SOCK_STREAM


class TaskClient:
    def __init__(self):
        with open("client.config", "r") as f:
            content = f.read()
            content = content.strip().split("\n")
            self.serverAddress = content[0].split(":")[1]
            self.serverPort = int(content[1].split(":")[1])
            self.bufferSize = int(content[2].split(":")[1])
            self.localTaskFile = content[3].split(":")[1]
            self.clientID = content[4].split(":")[1]
            self.requestTaskCommand = content[5].split(":")[1]

            self.taskResourceSpliter = content[6].split(":")[1]
            self.resourceSpliter = content[7].split(":")[1]
            self.resourceNameContentSpliter = content[8].split(":")[1]

            self.protocalSpliter = content[9].split(":")[1]
            self.resultBuffer = content[10].split(":")[1]
            self.reportTaskCommand = content[11].split(":")[1]
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.connected = False

    def connect(self):

        self.socket.connect((self.serverAddress, self.serverPort))
        try:
            result = self.__sentMsg(self.clientID).split(self.protocalSpliter)

            self.taskResourceSpliter = result[0]
            self.resourceSpliter = result[1]
            self.resourceNameContentSpliter = result[2]

            print("Successfully connected")
            self.connected = True
        except:
            print("Connection Failed")

    def __sentMsg(self, strMsg, resultType="str"):

        self.socket.send(bytes(strMsg, encoding="utf-8"))
        if (resultType == "str"):
            return self.socket.recv(self.bufferSize).decode("utf-8")
        else:
            return self.socket.recv(self.bufferSize)

    def requestTask(self):

        if self.connected:
            result = self.__sentMsg(self.requestTaskCommand).split(self.taskResourceSpliter)
            task = result[0]
            with open(self.localTaskFile, "w") as f:
                f.write(task)
            print("task received")
            resource = result[1].split(self.resourceSpliter)
            for res in resource:
                r = res.split(self.resourceNameContentSpliter)
                name = r[0]
                content = r[1]
                with open(name, "w") as f:
                    f.write(content)
                print("resource file:" + name + " received")
            print("All resource received")

        else:
            raise Exception("Client haven't connected to server, please call connect function first")

    def executeTask(self):
        # no need to keep connecting to the server

        try:
            import TaskFile
        except:
            return

        result = TaskFile.run()
        with open(self.resultBuffer, "a") as f:
            f.write(result)

        print("Client finish task")

    def reportResult(self):
        with open(self.resultBuffer, "r") as f:
            content = f.read()
        command = self.reportTaskCommand + content
        result = self.__sentMsg(command)
        print(result)


def reportOnly():
    client = TaskClient()

    client.connect()

    client.reportResult()


if __name__ == "__main__":

    client = TaskClient()

    client.connect()
    if client.connected:
        client.requestTask()
        client.executeTask()
        exit(-1)

        try:
            client.connect()
        except:
            pass
        client.reportResult()



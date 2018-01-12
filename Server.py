from socketserver import BaseRequestHandler, ThreadingTCPServer


subTask_number=5

with open("server.config") as f:
    content=f.read().split("\n")
    SERVER_PORT = int(content[0].split(":")[1])
    BUFFER_SIZE = int(content[1].split(":")[1])
    ALL_CLIENT_ID = content[2].split(":")[1].split(",")
    REQUEST_TASK_COMMAND = content[3].split(":")[1]

    TASK_RESOURCE_SPLIT = content[4].split(":")[1]
    RESOURCE_SPLIT = content[5].split(":")[1]
    RESOURCE_NAME_CONTENT_SPLIT = content[6].split(":")[1]
    PROTOCAL_SPLIT = content[7].split(":")[1]
    REPORT_TASK_COMMAND = content[8].split(":")[1]

with open("resource.res","r") as f:
        all_task={}
        for line in f:
            all_task[line.strip()]=0



class EchoHandler(BaseRequestHandler):

    def handle(self):

        global all_task
        print('Got connection from', self.client_address)
        self.connected=False
        while True:
            msg = self.request.recv(BUFFER_SIZE)
            if not msg:
                break
            msg = msg.decode("utf-8")
            if (msg in ALL_CLIENT_ID):
                print("Hear from "+str(msg))

                content = TASK_RESOURCE_SPLIT+PROTOCAL_SPLIT+RESOURCE_SPLIT+PROTOCAL_SPLIT+RESOURCE_NAME_CONTENT_SPLIT
                content=bytes(content,encoding="utf-8")
                self.request.send(content)
                self.connected=True

            elif(msg == REQUEST_TASK_COMMAND):
                if self.connected:
                    with open("TestFile.py","r") as f:
                        content = f.read()

                    resourceName="resource.res"
                    with open(resourceName,"r") as f:
                        all=f.read().split("\n")
                        resource=""
                        task_num=0
                        for line in all:
                            print(line,all_task[line])
                            if(all_task[line]==0):
                                resource+=line+"\n"
                                task_num+=1
                                all_task[line]=1
                                if(task_num>=subTask_number):
                                    break
                    the_resource = resourceName+RESOURCE_NAME_CONTENT_SPLIT+resource
                    content+=TASK_RESOURCE_SPLIT+the_resource
                    content = bytes(content,encoding="utf-8")
                    self.request.send(content)

            elif(msg[0:len(REPORT_TASK_COMMAND)]==REPORT_TASK_COMMAND):
                taskresult=msg[len(REPORT_TASK_COMMAND):]
                f=open("result.txt","a")
                f.write(taskresult+"\n")
                f.close()
                t=taskresult.split("\n")
                for line in t:
                    if(line!=""):
                        all_task[line]=2
                        print("finish:"+line)
                self.request.send(bytes("Successfully received", encoding="utf-8"))
            else:
                print(msg)

                content = bytes(content, encoding="utf-8")
                self.request.send(bytes("Unknown command", encoding="utf-8"))


if __name__ == '__main__':
    serv = ThreadingTCPServer(('', SERVER_PORT), EchoHandler)
    serv.serve_forever()
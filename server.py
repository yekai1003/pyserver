import socket
import datetime
import pymysql
from multiprocessing import Process
class webserver:
    def init(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("",8081))
        self.server_socket.listen(100)
        self.cnt = 0
    def start(self):
        print("cnt = %d"%self.cnt)
        client_socket, client_address = self.server_socket.accept()
        self.cnt += 1
        print("connected from[%s, %s]" % client_address)
        start_client_process = Process(target=self.client_server, args=(client_socket,client_address))
        start_client_process.start()
        client_socket.close()
    def client_server(self,client_socket, client_addr):
        request_data = client_socket.recv(1024)
        reqinfo = request_data.split()[1]
        print(reqinfo)
        reqline = reqinfo.split(b'/')
        print('reqline = ',reqline)
        dbfino = ''
        if len(reqline) > 1 :
            if reqline[1] == b'user':
                username = str(reqline[2], encoding = 'utf8')
                dbinfo = self.queryUserInfo(username)
            if b'favicon.ico' == reqline[1]:
                return
        print('dbinfo = ', dbinfo)
        # 打印日志
        self.log(request_data)
        # 构造响应数据
        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = "Server: My server\r\n"
       	filename = "index.html"
        with open(filename, encoding='utf-8') as f:
            body = f.read()
            f.close()
        response = response_start_line + response_headers +"\r\n" + dbinfo
        client_socket.send(bytes(response,"utf-8"))    
        client_socket.close()
    def mysql_init(self):
        self.db = pymysql.connect(host="0.0.0.0",port = 3306, user="root", passwd="root", db="docker")
    def queryUserInfo(self, username):
        cursor = self.db.cursor()
        print('username====', username)
        cursor.execute("select concat(name, ' age:', age, ' job:', job) from userinfo where name = '%s'"% (username))
        data = cursor.fetchone()
        return str(data)
        print(data)
    def main(self):
        self.init()
        self.mysql_init()
        self.queryUserInfo('yekai')
        while True:
            self.start()
    def log(self, data):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("log.txt",'a+') as f:
            f.write("\n%s\n%s" %(now_time, data))

if __name__ == '__main__':
    res = webserver()
    res.main()

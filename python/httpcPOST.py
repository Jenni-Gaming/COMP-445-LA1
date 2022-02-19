import socket
import argparse 
import sys

def run_httpclient(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    request_line = ("POST /post HTTP/1.0\r\n")
    header_lines=("Host:httpbin.org\r\nUser-Agent:Concordia-HTTP/1.0\r\nContent-Type:application/json\r\n")
    body =('{"Assignment": 1}')
    header_lines+=("Content-length:" + str(len(body)) + "\r\n\r\n")
    full_request = (request_line+header_lines+body).encode("utf-8")

    sock.sendall(full_request)

    response = sock.recv(1024, socket.MSG_WAITALL)
    sys.stdout.write(response.decode("utf-8"))

run_httpclient("httpbin.org",80)

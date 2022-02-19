import socket
import argparse
import sys
from argparse import RawTextHelpFormatter


def run_httpclient(httpc, port, url, verbosity, header, data, file):
    try:
        filler, fluff, host, path = url.split("/", 3)
        path = "/" + path
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((host, port))

        request_line = (httpc.upper() + " " + path + " HTTP/1.0\r\n")
        header_lines = ("Host:" + host + "\r\n")

        if httpc == "get":
            if (header != None):
                header_lines += header + "\r\n"
            header_lines += "\r\n"  # End header
            full_request = (request_line + header_lines).encode("utf-8")

        elif httpc == "post":
            body = data # Work under the assumption that data will be provided from either -d or -f
            # In case where both -d & -f are present, -d is given priority
            if data == None and file != None:
                current_file = open(file, "r")
                body = current_file.read()
                current_file.close()
            header_lines += "Content-Type:application/json\r\n"
            if (header != None):
                header_lines += header + "\r\n"
            header_lines += "Content-Length:" + str(len(body)) + "\r\n\r\n"
            full_request = (request_line + header_lines + body).encode("utf-8")

        sock.sendall(full_request)
        response = sock.recv(1024, socket.MSG_WAITALL)
        response = response.decode("utf-8")

        if not verbosity:
            response = response.split("\r\n\r\n")[1]
        sys.stdout.write(response)

    finally:
        sock.close()


general_help = '''httpc is a curl-like application but supports HTTP protocol only. 
Usage: 
    httpc command [arguments]
The commands are: 
    get executes a HTTP GET request and prints the response.
    post executes a HTTP POST request and prints the response.
    help prints this screen.

Use "httpc help [command]" for more information about a command.
'''

get_help = '''usage: httpc get [-v] [-h key:value] URL
Get executes a HTTP GET request for a given URL. 
-v Prints the detail of the response such as protocol, status, and headers.
-h key:value Associates headers to HTTP Request with the format 'key:value'.
'''

post_help = '''usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL
Post executes a HTTP POST request for a given URL with inline data or from file.

-v Prints the detail of the response such as protocol, status, and headers.
-h key:value Associates headers to HTTP Request with the format 'key:value'.
-d string Associates an inline data to the body HTTP POST request.
-f file Associates the content of a file to the body HTTP POST request.
Either [-d] or [-f] can be used but not both.
'''
parser = argparse.ArgumentParser(description=(general_help + get_help + post_help),
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument("--port", help="server port", type=int, default=80)

parser.add_argument("httpc", help="get or post, string. request type.", type=str)
parser.add_argument("URL", help="given URL to send requests to", type=str)
parser.add_argument("-v", help="sets verbosity to true", action="store_true")
parser.add_argument("-header", help="additional header line for the request, host is autogenerated", type=str, default=None)
parser.add_argument("-d", help=" inline data to be used as body of request", type=str, default=None)
parser.add_argument("-f", help="fielpath for body data", type=str, default=None)
args = parser.parse_args()

run_httpclient(args.httpc, args.port, args.URL, args.v, args.header, args.d, args.f)
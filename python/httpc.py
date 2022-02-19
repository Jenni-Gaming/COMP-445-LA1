import json
import argparse
import sys
import socket
import urllib.parse

request_types = ['get', 'post']

def runClient(request, URL, verbose, headersList, file, dataBody):
    if request == request_types[0]:
        if file is not None or dataBody is not None:
            print(500, "GET operation cannot contain -f or -d")
            sys.exit()
        runRequest(request_types[0], verbose, headersList, None, URL)
    elif request == request_types[1]:
        if dataBody is None and file is None:
            print(500, "POST operation needs to include -d or -f. Write --help for more information")
        if dataBody is not None:
            runRequest(request_types[1], verbose, headersList, str(dataBody), URL)
        if file is not None:
            try:
                f = open(file)
            except OSError:
                print("Could not open/read file: ", file)
                sys.exit()
            file_data = json.load(f)
            formatted_data = json.dumps(file_data)
            runRequest(request_types[1], verbose, headersList, formatted_data, URL)

def runRequest(request_type, isVerbose, headersList, data, URL):
    parsedURL = urllib.parse.urlparse(URL)
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_client.connect((parsedURL.netloc, 80))
        query = buildQuery(request_type, parsedURL, headersList, data)
        socket_client.send(query.encode())
        http_response = socket_client.recv(4096, socket.MSG_WAITALL)
        verbose_output, response_output = splitVerboseResponse(http_response.decode())

        if isVerbose:
            print(verbose_output, "\r\n")
        print(response_output)
    except:
        print("Connection failed")
    finally:
        socket_client.close()
        print("Connection closed.")

def splitVerboseResponse(httpResponse):
    responseList = httpResponse.split("\r\n\r\n")
    verbose_output = responseList[0].strip()
    response_output = responseList[1].strip()
    return verbose_output, response_output

def buildQuery(request_type, parsedURL, headersList, data):
    params = ""
    if parsedURL.query:
        params = "?" + parsedURL.query
    query = request_type.upper() + " " + parsedURL.path + params + " HTTP/1.0\r\n" + "Host: " + parsedURL.netloc + "\r\n"

    if headersList is not None:
        for header in headersList:
            query += (header + "\r\n")
    if request_type == 'post':
        query += "Content-Length: " + str(len(data))
        query += ("\r\n\r\n" + data)
    query += "\r\n\r\n"
    return query

#-f file name & -d body request are mutually exclusive
headerFileParser = argparse.ArgumentParser(add_help=False)
group = headerFileParser.add_mutually_exclusive_group()
group.add_argument('-f', help='file name')
group.add_argument('-d', help='body request')

#write --help to get all documentation
parser = argparse.ArgumentParser(prog='httpc', conflict_handler='resolve', parents=[headerFileParser])
parser.add_argument('request', choices=['get', 'post'], default='get', help='GET or POST')
parser.add_argument('URL', default='www.python.org', help='server host')
parser.add_argument('-v', action='store_true', help='verbose')
parser.add_argument('-h', nargs='*', action='extend', help='headers')
args = parser.parse_args()
runClient(args.request, args.URL, args.v, args.h, args.f, args.d)

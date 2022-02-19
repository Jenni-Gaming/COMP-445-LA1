# COMP-445-LA1
# Running 
Python 3

# Run httpc.py
- To run detailed usage: python httpc.py --help or python httpc.py -h
- To run GET with query parameters: python httpc.py get 'http://httpbin.org/get?course=networking&assignment=1'
- To run GET with verbose option: python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'
- To run POST with inline data: python httpc.py post -header "Content-Type:application/json" -d "{"Assignment": 1, "Course": "Networking"}" "http://httpbin.org/post"

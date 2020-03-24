# Cloud Provider X (CPX)

## CLI tool
A CLI tool was created in order to consume data from CPX. This tool was created with python3
anc it is using the Click framework to provide the CLI functionality. I created this trying to
be user friendly, and following a common pattern of really used cli's as `kubectl`

    `cpxctl.py`

## Requirements
 - Python 3
 - Dependencies : `pip3 install -r requirements.txt`
 - Give the python file permissions with `chmod +x cpxctl.py`

## Running the CLI

`cpxctl` will point for a default server on `http://localhost:9999` or you can set a Flag
`--server=<address>` pointing to your current server address

1. Show all running services on stdout with `get all`

    `./cpxctl.py get all`

1. Show specific running services on stdout with `get <service_name>`

    `./cpxctl.py get MLService`

2. Print out average CPU/Memory of services of the same type with `get average`. It will also shows
how many servers we have in a healthy state (mamory or cpu grater than 90%) and if we have less than 
2 servers healthy it will show an action flag

    `./cpxctl.py get average`


4. With all commands you have the ability to track and print CPU/Memory of all instances of a given service over
time (until the command is stopped, e.g. ctrl + c) with the flag `--watch==True`

    `./cpxctl.py get MLService --watch=True`

### Unit test
You can run unit test with the command below. There are a few unit tests missing and edge cases that shoud be addresses in the future.

    `python3 -m unittest`

### Trade-offs
 - The watch flag has some delay due to the request and the table creation in the same place.
Probably a some different approaches should tested in order to improve performance.

### Improvements
 - More unit test and edge cases validation
 - Remove duplicated code
 - Try to make to code more readable, maybe split it in more methods, and being more auto explainable

### Assumptions
A server is unhealthy where its CPU or Memory is grater than 90%
import socket

modes = [0,1,2]


#Create socket and connect
def initialize_socket(host, port):
    s = socket.socket()
    print("Socket successfully created")
    s.connect((host, port))
    print("socket connected to %s" % (host))

    return s

#----------------------------------------------------------------------

#Does treatment to the input
def scan_command(cmd) :
    cmd = cmd.split("'")
    cmd.pop()
    return cmd

#----------------------------------------------------------------------

def isInt (code) :
    isInt = True
    try:
    # converting to integer
        int(code)
    except ValueError:
         isInt = False
    
    return isInt


#Checks if the input is valid
def check_validity(code) : 

    if not isInt(code) :
        print("\nERROR INVALID COMMAND : CHOSE 0 for DIRECT (default); 1 for RANDOM; 2 for CUSTOM")
        return False

    if int(code) not in modes :
        print("Invalid code: by default DIRECT MODE")
        code = 0
    else :
        code = int(code)
    

    if code == 0 :
        print('DIRECT MODE : Sending request to master ...')
    elif code == 1 :
        print('RANDOM MODE : Sending request to a random node of the cluster ...')
    else :
        print("CUSTOM MODE : Sendin the request to the node with the fastest ping answer ...")
    return True

#----------------------------------------------------------------------

def main() :
    client_socket = initialize_socket('3.92.245.174',5001)
    print("\nCHOSE 0 for DIRECT (default); 1 for RANDOM; 2 for CUSTOM and then add a query")
    print("EXAMPLE : 0 'SELECT COUNT(*) FROM film'")

    while True :
        cmd = input("\n> ")
        if "stop" in cmd : break #CLose the socket if input is 'stop'
        cmd = scan_command(cmd)
        valid = check_validity(cmd[0])

        #Loops until vvalid query
        while not valid :
            cmd = input("ERROR : Enter a valid code: ")
            cmd = scan_command(cmd)
            if check_validity(cmd[0]) :
                valid = True

        #Check if in default mode
        concat_cmd = ''
        if int(cmd[0]) not in modes :
            concat_cmd = '0 ' + cmd[1]
        else :
            concat_cmd = cmd[0] + cmd[1]

        #Communicating with the proxy
        print(concat_cmd)
        client_socket.send(concat_cmd.encode())
        data = client_socket.recv(4096).decode()
        print("\n"+data)

    client_socket.close()
main()
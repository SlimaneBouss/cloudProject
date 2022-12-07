import socket

modes = [0,1,2]

def initialize_socket(host, port):
    s = socket.socket()
    print("Socket successfully created")
    host = socket.gethostname()
    s.connect((host, port))
    print("socket connected to %s" % (host))

    return s

def scan_command(cmd) :
    cmd = cmd.split("'")
    cmd.pop()
    return cmd

def check_validity(code) :
    #check if valid code
    if code not in modes :
        print("CHOSE 0 for DIRECT; 1 for RANDOM; 2 for CUSTOM")
        return False
    if code == 0 :
        print('DIRECT MODE : Sending request to master ...')
    elif code == 1 :
        print('RANDOM MODE : Sending request to a random node of the cluster ...')
    else :
        print("CUSTOM MODE : Sendin the request to the node with the fastest ping answer ...")
    return True


def main() :
    client_socket = initialize_socket('',5001)
    print("CHOSE 0 for DIRECT; 1 for RANDOM; 2 for CUSTOM")

    while True :
        cmd = input("\n>")
        if "stop" in cmd : break
        cmd = scan_command(cmd)
        valid = check_validity(int(cmd[0]))

        while not valid :
            cmd = input("ERROR : Enter a valid query: ")
            cmd = scan_command(cmd)
            if check_validity(int(cmd[0])) :
                valid = True

        concat_cmd = cmd[0] + cmd[1]
        client_socket.send(concat_cmd.encode())  # send message
        data = client_socket.recv(4096).decode()
        print(data)

    client_socket.close()
main()
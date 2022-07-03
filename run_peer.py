from bcb_server.peer import app
from bcb_server.peer import join_to_network
from bcb_server.utils import get_ip
from bcb_server.peer import ordererIP, ordererPort, caIP, caPort
import time

if __name__ == '__main__':
    from argparse import ArgumentParser

    myIP = get_ip()
    
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-c', '--ca', default='0.0.0.0', type=str, help='port to listen on')
    parser.add_argument('-o', '--orderer', default='0.0.0.0', type=str, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    caIP = args.ca
    ordererIP = args.orderer

    print('My ip address : ' + get_ip())
    
    # time.sleep(5)
    # join_to_network(ordererIP + ':' + ordererPort, caIP + ':' + caPort, myIP, port)
    while not join_to_network(ordererIP + ':' + ordererPort, caIP + ':' + caPort, myIP, port):
        print("Let me sleep for 5 seconds")
        time.sleep(5)

    app.run(host='0.0.0.0', port=port, debug = True, threaded = True)


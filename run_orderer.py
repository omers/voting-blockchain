from bcb_server.orderer import app
from bcb_server.utils import get_ip

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5002, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    print('My ip address : ' + get_ip())

    app.run(host='0.0.0.0', port=port, debug = True, threaded = True)

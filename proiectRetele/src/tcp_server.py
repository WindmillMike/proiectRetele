import socket
import logging
import time

logging.basicConfig(format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '0.0.0.0'  # Acceptă conexiuni externe
server_address = (adresa, port)
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portul %d", adresa, port)
sock.listen(5)

while True:
    logging.info('Asteptam conexiuni...')
    conexiune, address = sock.accept()
    logging.info("Handshake cu %s", address)

    while True:
        data = conexiune.recv(1024)
        if not data:
            break
        logging.info('Content primit: "%s"', data.decode())
        conexiune.send(b"[SERVER] Am primit: " + data)

    conexiune.close()

sock.close()

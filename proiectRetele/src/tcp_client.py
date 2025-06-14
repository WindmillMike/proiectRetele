import socket
import logging
import time
import sys

logging.basicConfig(format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10000
adresa = '198.7.0.2'  # IP-ul serverului
server_address = (adresa, port)

try:
    logging.info('Handshake cu %s', str(server_address))
    sock.connect(server_address)
    time.sleep(1)
    mesaj = sys.argv[1]
    
    while True:
        logging.info('Trimit: "%s"', mesaj)
        sock.send(mesaj.encode('utf-8'))
        data = sock.recv(1024)
        logging.info('Content primit: "%s"', data.decode())
        time.sleep(2)
        
        
        

except Exception as e:
    logging.error("Eroare: %s", e)

finally:
    logging.info('closing socket')
    sock.close()

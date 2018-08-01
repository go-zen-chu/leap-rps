#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import threading
import signal
from websocket_server import WebsocketServer
from logging import getLogger, DEBUG, StreamHandler

class RpsWsServer:
    host = '127.0.0.1'
    port = 9090
    signal_stop = False
    rps_file_name = 'rps.txt'
    rps_status = 'null'
    server = None
    logger = None

    def __init__(self, logger):
        # handle signal for stopping thread
        # signal.signal(signal.SIGINT, self.sigint_handler)
        self.server = WebsocketServer(self.port, host=self.host, loglevel=DEBUG)
        self.server.set_fn_new_client(self.new_client)
        self.logger = logger

    def sigint_handler(self, signum, frame):
        self.signal_stop = True

    def new_client(self, client, server):
        server.send_message_to_all("New client joined, id:{}".format(client['id']))

    def send_message_every(self, server):
        while self.signal_stop == False:
            if os.path.exists(self.rps_file_name):
                # process while file exists
                with open(self.rps_file_name, 'r') as f:
                    result = f.readline()
                    # 初回しか送らない
                    if self.rps_status != result:
                        self.rps_status = result
                        server.send_message_to_all(result)
            else:
                self.rps_status = 'null'
            print(self.rps_status)
            time.sleep(0.01) # wait 10ms
        print('bye')
        return # finish thread process

    def run(self):
        if self.server == None:
            self.logger.error('Server is None', exc_info=True)

        th = threading.Thread(target=self.send_message_every, args=(self.server,))
        th.daemon = True
        th.start()
        self.server.run_forever()

if __name__ == "__main__":
    logger = getLogger(__name__)
    logger.setLevel(DEBUG)
    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)
    logger.addHandler(stream_handler)
    logger.propagate = False

    server = RpsWsServer(logger)
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Server terminated.")
    except Exception as e:
        logger.error(str(e), exc_info=True)
        exit(1)

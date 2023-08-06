from unittest import TestCase
from ifd.repository import AmqpImageRepository
import time

class postImageOnAmqp_test(TestCase):
    
    connection : AmqpImageRepository
    
    def __init__(self, data):

        self.connection = AmqpImageRepository(
                user='guest',
                password='guest',
                dns='127.0.0.1',
                exchange='exchange'
            )

    def test_post_image_on_local_server_amqp(self):
        self.connection.sendMessageToChannel(message="this is a test ! :)")

    def test_post_image_on_local_server_amqp_after_15_seconde(self):
        time.sleep(25)
        self.connection.sendMessageToChannel(message="the test waits 25 second ! :)")
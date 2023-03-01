from bot.utils import get_ip
class Task:

    def __init__(self):
        self.public_ip = get_ip.get_public_ip()


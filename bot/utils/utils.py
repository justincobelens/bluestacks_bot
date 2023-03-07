import requests as req


def get_host_public_ip():
    url: str = 'https://checkip.amazonaws.com'
    request = req.get(url)
    ip: str = request.text.strip()

    return ip

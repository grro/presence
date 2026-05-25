import sys
import logging
from typing import Dict
from webthing import (MultipleThings, WebThingServer)
from presence import  IpPresence, Presences
from redzoo.math.display import duration
from presence_web import PresenceWebServer
from presence_mcp import PresenceMCPServer
from presence_webthing import PresenceThing



def run_server(description: str, port: int, name_address_map: Dict[str, str], timeout_sec :int):
    if len(name_address_map) < 2:
        presences = [IpPresence(dev_name, name_address_map[dev_name], timeout_sec) for dev_name in name_address_map.keys()]
    else:
        presences = [IpPresence(dev_name, name_address_map[dev_name], timeout_sec) for dev_name in name_address_map.keys()]
        presences = [Presences("any", presences, timeout_sec)] + presences

    web_server = PresenceWebServer(presences, port=port+1)
    mcp_server = PresenceMCPServer("presence", port+2, presences)
    webthing_server = WebThingServer(MultipleThings([PresenceThing(description, presence) for presence in presences], "presence"), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server http://localhost:' + str(port) + " (absent threshold: " + duration(timeout_sec) + ")")
        [presence.start() for presence in presences]
        web_server.start()
        mcp_server.start()
        webthing_server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        [presence.stop() for presence in presences]
        web_server.stop()
        mcp_server.stop()
        webthing_server.stop()
        logging.info('done')


def parse_devices(config: str) -> Dict[str, str]:
    name_address_map = {}
    for device in config.split("&"):
        name, address = device.split('=')
        name_address_map[name.strip()] = address.strip()
    logging.info("configured devices: " + ", ".join([f"{name} ({address})" for name, address in name_address_map.items()]))
    return name_address_map


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger('tornado.access').setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    logging.getLogger('starlette.middleware.base').setLevel(logging.WARNING)
    logging.getLogger('fastmcp').setLevel(logging.WARNING)
    logging.getLogger('mcp').setLevel(logging.WARNING)
    logging.getLogger('mcp.server').setLevel(logging.WARNING)
    logging.getLogger('mcp.server.lowlevel.server').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').disabled = True
    logging.getLogger('uvicorn.error').setLevel(logging.WARNING)
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    run_server("description", int(sys.argv[1]), parse_devices(sys.argv[2]), int(sys.argv[3]))


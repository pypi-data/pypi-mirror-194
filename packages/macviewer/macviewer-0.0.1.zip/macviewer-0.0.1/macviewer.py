import time
import select
import socket
import logging
from typing import Set
from threading import Thread, Event
from collections import defaultdict
from dataclasses import dataclass, field

from rich.logging import RichHandler
from rich.spinner import Spinner
from rich.status import Status
from rich.table import Table
from rich.console import Group
from rich.live import Live

logging.basicConfig(level=logging.DEBUG, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
_logger = logging.getLogger(__name__)

EMPTY = tuple()
REFRESH = 5

def sniff(packet_cb, stop_cb, eth_p=0x0003, select_timeout=2, dgram_size=65535):
    s = socket.socket(socket.AF_PACKET , socket.SOCK_RAW, socket.htons(eth_p))
    while not stop_cb():
        sock_ready, *_ = select.select([s], EMPTY, EMPTY, select_timeout)
        if sock_ready:
            packet_cb(*s.recvfrom(dgram_size))
    s.close()


def bytes_to_mac(b: bytes):
    # hyphen is used to easily escape rich emojis, can also technically use chr(42889)
    # but it breaks the table lines ever so slightly.
    return b.hex('-')

KNOWN_ETHER_TYPES = {
    0x800: "IP",
    0x806: "ARP",
    0x86DD: "IPv6",
    0x8035: "RARP",
    0x880B: "PPP",
    0x9000: "ETHLOOPBACK",
}

MAC_HARDWARE_TYPE = 1

g_silenced_hardware_types = set()

# this can be automated with some MacAddrMetadata class method, I can't bother:
TABLE_COLUMNS = [
    "[purple]idx",
    "[blue]mac address",
    "[green]ifnames",
    "[green]ether types",
    "[green]inbound",
    "[green]outbound",
    "[green]broadcast",
    "[green]multicast",
    "[green]promiscuous",
    "[green]unknown",
]

def make_pkt_meta(metadata):
    """
    given the recvfrom peer tuple return a tuple consisting of
    (ifname, str parsed ether type, str parsed packet type, and str parsed mac addr)
    """
    ifname, ether_type, pkt_type, hardware_type, hardware_addr = metadata

    # Deal only with mac addresses for now, assume non ether is some localhost 00:00:00:00:00:00 magic
    if hardware_type != MAC_HARDWARE_TYPE:
        if hardware_type not in g_silenced_hardware_types:
            _logger.debug(f"Silencing non MAC/ETHERNET hardware addr type {hardware_type}")
            g_silenced_hardware_types.add(hardware_type)
    hardware_addr = bytes_to_mac(hardware_addr)
    if ether_type >= 0x600:
        ether_type = KNOWN_ETHER_TYPES.get(ether_type, str(ether_type))
    else:
        ether_type = "RAW_ETHER_SIZE"
    return ifname, ether_type, pkt_type, hardware_addr


@dataclass
class MacAddrMetadata:
    ifnames: Set[str] = field(default_factory=set)
    ether_types: Set[str] = field(default_factory=set)
    inbound: int = 0
    outbound: int = 0
    broadcast: int = 0
    multicast: int = 0
    promiscuous: int = 0
    unknown: int = 0


class AfPacketRawSniffParser:
    def __init__(self):
        self._total_packets = 0
        self._macs = defaultdict(MacAddrMetadata)

    def on_pkt(self, data, metadata):
        self._total_packets += 1
        ifname, ether, pkt, mac = make_pkt_meta(metadata)
        meta = self._macs[mac]
        meta.ifnames.add(ifname)
        meta.ether_types.add(ether)

        if pkt == socket.PACKET_HOST:
            meta.inbound += 1
        elif pkt == socket.PACKET_OUTGOING:
            meta.outbound += 1
        elif pkt == socket.PACKET_BROADCAST:
            meta.broadcast += 1
        elif pkt == socket.PACKET_MULTICAST:
            meta.multicast += 1
        elif pkt == socket.PACKET_OTHERHOST:
            meta.promiscuous += 1
        else:
            meta.unknown += 1


    @property
    def total_packets(self):
        return self._total_packets

    @property
    def macs(self):
        return self._macs

def main():
    should_stop = Event()
    status = Spinner("earth")
    sniffer = AfPacketRawSniffParser()

    def _make_group():
        table = Table(*TABLE_COLUMNS)
        for i, (mac, meta) in enumerate(sniffer.macs.items()):
            table.add_row(
                str(i), mac,
                " ".join(meta.ifnames),
                " ".join(meta.ether_types),
                str(meta.inbound),
                str(meta.outbound),
                str(meta.broadcast),
                str(meta.multicast),
                str(meta.promiscuous),
                str(meta.unknown),
            )
        status.update(text=f"Sniffing packets... ({sniffer.total_packets} total)")
        group = Group(table, status)
        return group

    # for now can use a minimal dgram size because I only care about the metadata
    t = Thread(target=sniff, args=(sniffer.on_pkt, should_stop.is_set), kwargs={'dgram_size': 1}, daemon=False)
    t.start()

    with Live("", auto_refresh=False) as live:
        try:
            while True:
                live.update(_make_group(), refresh=True)
                time.sleep(1/REFRESH)
        except KeyboardInterrupt:
            pass

    with Status("Waiting for the raw socket to close...") as status:
        should_stop.set()
        t.join()


if __name__ == "__main__":
    main()

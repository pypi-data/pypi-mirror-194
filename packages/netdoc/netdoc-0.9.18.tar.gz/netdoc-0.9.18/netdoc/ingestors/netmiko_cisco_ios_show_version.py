"""Ingestor for netmiko_cisco_ios_show_version."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-07"
__version__ = "0.9.18"

from netdoc.schemas import device
from netdoc import utils


def ingest(log):
    """Processing parsed output."""
    device_o = log.discoverable.device

    # Show version contains only one item
    item = next(iter(log.parsed_output))

    # See https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_ios/show_version # pylint: disable=line-too-long
    data = {
        "serial": utils.normalize_serial(next(iter(item.get("serial")), None)),
    }
    device.update(device_o, **data)

    # Update the log
    log.ingested = True
    log.save()

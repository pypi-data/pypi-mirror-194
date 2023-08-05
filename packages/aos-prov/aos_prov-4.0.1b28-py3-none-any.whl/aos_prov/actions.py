#
#  Copyright (c) 2018-2023 Renesas Inc.
#  Copyright (c) 2018-2023 EPAM Systems Inc.
#
import time

from aos_prov.commands.command_provision import run_provision
from aos_prov.commands.command_vm_multi_node_manage import new_vm, start_vms
from aos_prov.commands.download import download_and_save_multinode
from aos_prov.communication.cloud.cloud_api import CloudAPI
from aos_prov.utils.common import DOWNLOADS_PATH
from aos_prov.utils.user_credentials import UserCredentials


def create_new_unit(
    vm_name: str,
    uc: UserCredentials,
    disk_location: str,
    do_provision=False,
    nodes_count=2
) -> []:
    """Create a new VirtualBox multi-node Unit.

    Args:
        vm_name (str): Name of the group of units.
        uc (UserCredentials): UserCredentials instance.
        disk_location (str): Full path to the folder with nodes images.
        do_provision (Boolean): Provision unit after creation or not.
        nodes_count (int): Count of nodes to create. Supported 1 or 2 nodes.
    Raises:
        AosProvError: If any error occurred.
    Returns:
        [provisioning_port, node0_ssh_port, node1_ssh_port]: Forwarded ports.
    """
    cloud_api = CloudAPI(uc)

    if do_provision:
        cloud_api.check_cloud_access()

    provisioning_port, node0_ssh_port, node1_ssh_port = new_vm(vm_name, disk_location, nodes_count)

    if do_provision:
        start_vms(f'/AosUnits/{vm_name}')
        time.sleep(10)
        run_provision(f'127.0.0.1:{provisioning_port}', cloud_api, reconnect_times=40)

    return [provisioning_port, node0_ssh_port, node1_ssh_port]


def start_vm(name: str) -> None:
    """Start all VMs in the group.

    Args:
        name (str): Name of the group to start
    Raises:
        AosProvError: If no VMs to start found.
    Returns:
        None
    """
    start_vms(f'/AosUnits/{name}', check_virtualbox=True)


def download_image(download_url: str, force: bool = False) -> None:
    """Download unit image.
    Args:
        download_url (str): URL to download from.
        force (bool): If set downloaded image will overwrite existing one.
    Raises:
        AosProvError: If error occurred.
    Returns:
        None
    """
    download_and_save_multinode(download_url, DOWNLOADS_PATH, force)
    print('Download finished. You may find Unit images in: ' + str(DOWNLOADS_PATH.resolve()))

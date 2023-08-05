#
#  Copyright (c) 2018-2022 Renesas Inc.
#  Copyright (c) 2018-2022 EPAM Systems Inc.
#

import random
import string
from pathlib import Path

from rich.console import Console

CONTENT_ENCRYPTION_ALGORITHM = 'aes256_cbc'
DOWNLOADS_PATH = Path.home() / '.aos' / 'downloads'
AOS_DISK_PATH = DOWNLOADS_PATH / 'aos-disk.vmdk'
AOS_DISKS_PATH = DOWNLOADS_PATH
VBOX_SDK_PATH = DOWNLOADS_PATH / 'vbox-sdk.zip'


NODE0_IMAGE_FILENAME = 'aos-vm-node0-genericx86-64.wic.vmdk'
NODE1_IMAGE_FILENAME = 'aos-vm-node1-genericx86-64.wic.vmdk'


DISK_IMAGE_DOWNLOAD_URL = 'https://aos-prod-cdn-endpoint.azureedge.net/vm/R4.0.3.tar.gz?0b423ffb33d4cc5e1c32d5e76' \
                          '9fd8198f4256b90eceb55a5373df5f107003ead4348269c86b0b79679c6f4360c1a54cffc5f958d49ecbdaa' \
                          '99a9055e4f'
VIRTUAL_BOX_DOWNLOAD_URL = 'https://download.virtualbox.org/virtualbox/6.1.42/VirtualBoxSDK-6.1.42-155177.zip'

console = Console()
allow_print = True

def print_message(formatted_text, end="\n"):
    if allow_print:
        console.print(formatted_text, end=end)

def generate_random_password() -> str:
    """
    Generate random password from letters and digits.

    Returns:
        str: Random string password
    """
    dictionary = string.ascii_letters + string.digits
    password_length = random.randint(10, 15)
    return ''.join(random.choice(dictionary) for _ in range(password_length))

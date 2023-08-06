"""Timeweb Cloud public API SDK."""

__all__ = ["TimewebCloud"]


import json

import requests

from twc.__version__ import __version__, __pyversion__
from .exceptions import (
    NonJSONResponseError,
    UnauthorizedError,
    UnexpectedResponseError,
)

API_BASE_URL = "https://api.timeweb.cloud"
API_PATH = "/api/v1"
DEFAULT_TIMEOUT = 100
DEFAULT_USER_AGENT = f"TWC-SDK/{__version__} Python {__pyversion__}"


def raise_exceptions(func):
    def wrapper(self, *args, **kwargs):
        response = func(self, *args, **kwargs)
        status_code = response.status_code

        try:
            is_json = response.headers.get("content-type").startswith(
                "application/json"
            )
        except AttributeError:
            is_json = False

        if status_code in [200, 201, 400, 403, 404, 409, 429, 500]:
            if is_json:
                return response  # Success
            raise NonJSONResponseError

        if status_code == 204:
            return response  # Success

        if status_code == 401:
            raise UnauthorizedError

        raise UnexpectedResponseError(status_code)

    return wrapper


class TimewebCloudMeta(type):
    """This metaclass decorate all methods with raise_exceptions decorator."""

    def __new__(mcs, name, bases, namespace):
        namespace = {
            k: v if k.startswith("__") else raise_exceptions(v)
            for k, v in namespace.items()
        }
        return type.__new__(mcs, name, bases, namespace)


class TimewebCloud(metaclass=TimewebCloudMeta):
    """Timeweb Cloud API client class. Methods returns `requests.Request`
    object. Raise exceptions class `TimewebCloudException`.
    """

    # pylint: disable=too-many-public-methods

    def __init__(
        self,
        api_token: str,
        api_base_url: str = API_BASE_URL,
        api_path: str = API_PATH,
        headers: dict = None,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.api_token = api_token
        self.api_base_url = api_base_url
        self.api_path = api_path
        self.api_url = self.api_base_url + self.api_path
        self.timeout = timeout
        self.headers = requests.utils.default_headers()
        if headers:
            self.headers.update(headers)
        self.headers.update({"User-Agent": user_agent})
        self.headers.update({"Authorization": f"Bearer {self.api_token}"})

    # -----------------------------------------------------------------------
    # Account

    def get_account_status(self):
        """Return Timeweb Cloud account status."""
        url = f"{self.api_url}/account/status"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_account_finances(self):
        """Return finances."""
        url = f"{self.api_url}/account/finances"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_account_restrictions(self):
        """Return account access restrictions info."""
        url = f"{self.api_url}/auth/access"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    # -----------------------------------------------------------------------
    # Cloud Servers

    def get_servers(self, limit: int = 100, offset: int = 0):
        """Get list of Cloud Server objects."""
        url = f"{self.api_url}/servers?limit={limit}&offset={offset}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_server(self, server_id: int):
        """Get Cloud Server object."""
        url = f"{self.api_url}/servers/{server_id}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def create_server(
        self,
        configuration: dict = None,
        preset_id: int = None,
        os_id: int = None,
        software_id: int = None,
        bandwidth: int = None,
        name: str = None,
        comment: str = None,
        avatar_id: str = None,
        ssh_keys_ids: list = None,
        is_local_network: bool = False,
        is_ddos_guard: bool = False,
    ):
        """Create new Cloud Server.
        `configuration` must have following structure::

            configuration: {
                'configurator_id': 11,
                'disk': 15360,
                'cpu': 1,
                'ram': 2048
            }

        For `confugurator_id` see `get_server_configurators()`. `disk` and
        `ram` must be in megabytes. Values must values must comply with the
        configurator constraints.

        `configuration` and `preset_id` cannot be used in same time. One of
        parameters is required.

        Server location depends on `configuration` or `preset_id`.

        `ssh_keys_ids` must contain IDs of uploaded SSH-keys. First
        upload key (https://timeweb.cloud/my/sshkeys) and get key ID.
        """

        url = f"{self.api_url}/servers"
        self.headers.update({"Content-Type": "application/json"})
        if not configuration and not preset_id:
            raise ValueError(
                "One of parameters is required: configuration, preset_id"
            )

        # Add required keys
        if configuration:
            payload = {
                "configuration": configuration,
                "os_id": os_id,
                "bandwidth": bandwidth,
                "name": name,
                "is_ddos_guard": is_ddos_guard,
                "is_local_network": is_local_network,
            }
        else:
            payload = {
                "preset_id": preset_id,
                "os_id": os_id,
                "bandwidth": bandwidth,
                "name": name,
                "is_ddos_guard": is_ddos_guard,
                "is_local_network": is_local_network,
            }

        # Add optional keys
        if comment:
            payload["comment"] = comment
        if software_id:
            payload["software_id"] = software_id
        if avatar_id:
            payload["avatar_id"] = avatar_id
        if ssh_keys_ids:
            payload["ssh_keys_ids"] = ssh_keys_ids

        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def delete_server(self, server_id: int):
        """Delete Cloud Server by ID."""
        url = f"{self.api_url}/servers/{server_id}"
        return requests.delete(url, headers=self.headers, timeout=self.timeout)

    def update_server(self, server_id: int, payload: dict):
        """Update Cloud Server.

        Resize RAM, CPU, Disk, reinstall operation system and/or
        change Cloud server information. Example payload::

            {
                "configurator": {
                    "configurator_id": 11,
                    "disk": 15360,
                    "cpu": 1,
                    "ram": 2048
                },
                "os_id": 188,
                "software_id": 199,
                "preset_id": 81,
                "bandwidth": 200,
                "name": "name",
                "avatar_id": "avatar",
                "comment": "comment"
            }
        """
        url = f"{self.api_url}/servers/{server_id}"
        self.headers.update({"Content-Type": "application/json"})
        return requests.patch(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def do_action_with_server(self, server_id: int, action: str = None):
        """Do action with Cloud Server. API returns HTTP 204 No Content
        status code on success."""
        url = f"{self.api_url}/servers/{server_id}/action"
        self.headers.update({"Content-Type": "application/json"})
        if isinstance(action, str):
            if action.lower() in [
                "hard_reboot",
                "hard_shutdown",
                "install",
                "reboot",
                "remove",
                "reset_password",
                "shutdown",
                "start",
                "clone",
            ]:
                payload = {"action": action.lower()}
            else:
                raise ValueError(f"Invalid action '{action}'")
        else:
            raise TypeError(
                f"action must be string, not {type(action).__name__}"
            )
        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def get_server_configurators(self):
        """List configurators."""
        url = f"{self.api_url}/configurator/servers"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_server_presets(self):
        """List available server configuration presets."""
        url = f"{self.api_url}/presets/servers"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_server_os_images(self):
        """List available prebuilt operating system images."""
        url = f"{self.api_url}/os/servers"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_server_software(self):
        """List available software."""
        url = f"{self.api_url}/software/servers"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_server_logs(
        self,
        server_id: int,
        limit: int = 100,
        offset: int = 0,
        order: str = None,
    ):
        """View server action logs. Logs can be ordered by datetime."""
        if order not in ["asc", "desc"]:
            raise ValueError(f"Invelid order type '{order}'")
        url = (
            f"{self.api_url}/servers/{server_id}"
            + f"/logs?limit={limit}&offset={offset}&order={order}"
        )
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def set_server_boot_mode(self, server_id: int, boot_mode: str = None):
        """Change Cloud Server boot mode."""
        url = f"{self.api_url}/servers/{server_id}/boot-mode"
        self.headers.update({"Content-Type": "application/json"})
        if boot_mode in ["default", "single", "recovery_disk"]:
            payload = {"boot_mode": boot_mode}
        else:
            raise ValueError(f"Invalid boot mode '{boot_mode}'")
        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def set_server_nat_mode(self, server_id: int, nat_mode: str = None):
        """Change Cloud Server NAT mode. Available only for servers in
        local networks.
        """
        url = f"{self.api_url}/servers/{server_id}/local-networks/nat-mode"
        self.headers.update({"Content-Type": "application/json"})
        if nat_mode in ["dnat_and_snat", "snat", "no_nat"]:
            payload = {"nat_mode": nat_mode}
        else:
            raise ValueError(f"Invalid NAT mode '{nat_mode}'")
        return requests.patch(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    # -----------------------------------------------------------------------
    # Cloud Servers: Public IPs

    def get_ips_by_server_id(self, server_id: int):
        """List public IPs of Cloud Server."""
        url = f"{self.api_url}/servers/{server_id}/ips"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def add_ip_addr(
        self, server_id: int, version: str = None, ptr: str = None
    ):
        """Add new public IP to Cloud Server."""
        url = f"{self.api_url}/servers/{server_id}/ips"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"type": version, "ptr": ptr}
        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def delete_ip_addr(self, server_id: int, ip_addr: str):
        """Delete IP address from Cloud Server."""
        url = f"{self.api_url}/servers/{server_id}/ips"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"ip": ip_addr}
        return requests.delete(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def update_ip_addr(
        self, server_id: int, ip_addr: str = None, ptr: str = None
    ):
        """Update IP address properties."""
        url = f"{self.api_url}/servers/{server_id}/ips"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"ip": ip_addr, "ptr": ptr}
        return requests.patch(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    # -----------------------------------------------------------------------
    # Cloud Servers: Disks

    def get_disks_by_server_id(self, server_id: int):
        """List Cloud Server disks."""
        url = f"{self.api_url}/servers/{server_id}/disks"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_disk(self, server_id: int, disk_id: int):
        """Get disk."""
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def update_disk(self, server_id: int, disk_id: int, size: int = None):
        """Resize disk."""
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"size": size}
        return requests.patch(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def add_disk(self, server_id: int, size: int = None):
        """Add new disk to Cloud Server."""
        url = f"{self.api_url}/servers/{server_id}/disks"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"size": size}
        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def delete_disk(self, server_id: int, disk_id: int):
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}"
        return requests.delete(url, headers=self.headers, timeout=self.timeout)

    def get_disk_autobackup_settings(self, server_id: int, disk_id: int):
        """Return disk auto-backup settings."""
        url = (
            f"{self.api_url}/servers/{server_id}/disks/{disk_id}/auto-backups"
        )
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def update_disk_autobackup_settings(
        self,
        server_id: int,
        disk_id: int,
        is_enabled: bool = None,
        copy_count: int = None,
        creation_start_at: int = None,
        interval: str = None,
        day_of_week: int = None,
    ):
        """Update disk auto-backup settings."""
        url = (
            f"{self.api_url}/servers/{server_id}/disks/{disk_id}/auto-backups"
        )
        self.headers.update({"Content-Type": "application/json"})
        payload = {"is_enabled": is_enabled}
        if copy_count:
            payload.update({"copy_count": copy_count})
        if creation_start_at:
            payload.update({"creation_start_at": creation_start_at})
        if interval:
            payload.update({"interval": interval})
        if day_of_week:
            payload.update({"day_of_week": day_of_week})
        return requests.patch(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    # -----------------------------------------------------------------------
    # Cloud Servers: Backups

    def get_disk_backups(self, server_id: int, disk_id: int):
        """Get backups list of server disk."""
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}/backups"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_disk_backup(self, server_id: int, disk_id: int, backup_id: int):
        """Get disk backup."""
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}/backups/{backup_id}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def create_disk_backup(
        self, server_id: int, disk_id: int, comment: str = None
    ):
        """Create new backup."""
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}/backups"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"comment": comment}
        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def update_disk_backup(
        self, server_id: int, disk_id: int, backup_id: int, comment: str = None
    ):
        """Update backup properties."""
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}/backups/{backup_id}"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"comment": comment}
        return requests.patch(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def delete_disk_backup(self, server_id: int, disk_id: int, backup_id: int):
        """Delete backup."""
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}/backups/{backup_id}"
        return requests.delete(url, headers=self.headers, timeout=self.timeout)

    def do_action_with_disk_backup(
        self, server_id: int, disk_id: int, backup_id: int, action: str = None
    ):
        """Perform action with backup."""
        url = f"{self.api_url}/servers/{server_id}/disks/{disk_id}/backups/{backup_id}/action"
        self.headers.update({"Content-Type": "application/json"})
        if action in ["restore", "mount", "unmount"]:
            payload = {"action": action}
        else:
            raise ValueError(f"Invalid action '{action}'")
        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    # -----------------------------------------------------------------------
    # SSH-keys

    def get_ssh_keys(self):
        """Get list of SSH-keys."""
        url = f"{self.api_url}/ssh-keys"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def get_ssh_key(self, ssh_key_id: int):
        """Get SSH-key by ID."""
        url = f"{self.api_url}/ssh-keys/{ssh_key_id}"
        return requests.get(url, headers=self.headers, timeout=self.timeout)

    def add_new_ssh_key(
        self, name: str = None, body: str = None, is_default: bool = False
    ):
        """Add new SSH-key."""
        url = f"{self.api_url}/ssh-keys"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"name": name, "body": body, "is_default": is_default}
        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def update_ssh_key(self, ssh_key_id: int, data: dict = None):
        """Update an existing SSH-key."""
        url = f"{self.api_url}/ssh-keys/{ssh_key_id}"
        self.headers.update({"Content-Type": "application/json"})
        payload = {}
        if data:
            for key in list(data.keys()):
                if key in ["name", "body", "is_default"]:
                    payload.update({key: data[key]})
                else:
                    raise ValueError(f"Invalid key '{key}'")
        return requests.patch(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def delete_ssh_key(self, ssh_key_id: int):
        """Delete SSH-key by ID."""
        url = f"{self.api_url}/ssh-keys/{ssh_key_id}"
        return requests.delete(url, headers=self.headers, timeout=self.timeout)

    def add_ssh_key_to_server(self, server_id: int, ssh_key_ids: list = None):
        """Add SSH-keys to Cloud Server."""
        url = f"{self.api_url}/servers/{server_id}/ssh-keys"
        self.headers.update({"Content-Type": "application/json"})
        payload = {"ssh_key_ids": ssh_key_ids}
        return requests.post(
            url,
            headers=self.headers,
            timeout=self.timeout,
            data=json.dumps(payload),
        )

    def delete_ssh_key_from_server(self, server_id: int, ssh_key_id: int):
        """Delete SSH-key from Cloud Server."""
        url = f"{self.api_url}/servers/{server_id}/ssh-keys/{ssh_key_id}"
        return requests.delete(url, headers=self.headers, timeout=self.timeout)

"""Example for getting all bssid from all wifi interfaces."""

from networkmanager.networkmanager import NetworkManager


def main() -> None:
    """Main example entrypoint"""
    manager = NetworkManager()

    for interface in manager.wifi_interfaces():
        manager.request_scan(interface)
        for ssid in manager.get_all_ap_from_wifi_interface(interface):
            print(ssid)


if __name__ == "__main__":
    main()

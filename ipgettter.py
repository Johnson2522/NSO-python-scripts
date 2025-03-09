import sys
sys.path.append('/home/mszabo/nso-6.3/src/ncs/pyapi/')
import ncs
import ncs.maagic as maagic

def get_ipv4_address(device_name, interface_id):
    with ncs.maapi.Maapi() as m:
        with ncs.maapi.Session(m, 'admin', 'python'):
            with m.start_read_trans() as t:
                root = maagic.get_root(t)
                device = root.devices.device[device_name]

                # Access the GigabitEthernet configuration
                gigabitethernet = device.config.cisco_ios_xr__interface.GigabitEthernet[interface_id]

                # Access IPv4 address configuration
                ipv4_address = gigabitethernet.ipv4.address
                if ipv4_address:
                    return ipv4_address.ip, ipv4_address.mask
                else:
                    return None, None

def main():
    routers = ['P1', 'P2']
    interface_id = '0/0/0/0'

    for router in routers:
        ip, mask = get_ipv4_address(router, interface_id)
        if ip and mask:
            print(f"Router: {router}")
            print(f"Interface: {interface_id}")
            print(f"IPv4 Address: {ip}")
            print(f"Subnet Mask: {mask}\n")
        else:
            print(f"No IPv4 address configured on {router} interface {interface_id}.\n")

if __name__ == "__main__":
    main()

import sys
sys.path.append('/home/mszabo/nso-6.3/src/ncs/pyapi/')
import ncs
import ncs.maagic as maagic

def get_isis_info(device_name):
    with ncs.maapi.Maapi() as m:
        with ncs.maapi.Session(m, 'admin', 'python'):
            with m.start_read_trans() as t:
                root = maagic.get_root(t)
                device = root.devices.device[device_name]

                isis_info = {}

                # Access ISIS configuration under the CORE tag
                isis_tag = device.config.cisco_ios_xr__router.isis.tag['CORE']
                
                isis_info['apply_group'] = isis_tag.apply_group
                isis_info['is_type'] = isis_tag.is_type
                isis_info['net'] = isis_tag.net

                # Distribute link-state
                isis_info['distribute_link_state'] = isis_tag.distribute.link_state

                # Address Family IPv4 Unicast
                ipv4_unicast = isis_tag.address_family.ipv4.unicast
                isis_info['ipv4_unicast'] = {
                    'metric_style': ipv4_unicast.metric_style,
                    'mpls_traffic_eng_level': ipv4_unicast.mpls.traffic_eng.level,
                    'mpls_traffic_eng_router_id': ipv4_unicast.mpls.traffic_eng.router_id,
                    'router_id': ipv4_unicast.router_id,
                    'redistribute_static': ipv4_unicast.redistribute.static,
                    'segment_routing_mpls': ipv4_unicast.segment_routing.mpls,
                    'sr_prefer': ipv4_unicast.segment_routing.mpls.sr_prefer,
                }

                # Address Family IPv4 Multicast
                isis_info['ipv4_multicast'] = isis_tag.address_family.ipv4.multicast

                # Interfaces under ISIS CORE tag
                isis_info['interfaces'] = {}
                for interface in isis_tag.interface:
                    isis_info['interfaces'][interface.name] = {
                        'ipv4_unicast': interface.address_family.ipv4.unicast,
                        'ipv4_multicast': interface.address_family.ipv4.multicast if 'multicast' in interface.address_family.ipv4 else None,
                        'prefix_sid_absolute': interface.address_family.ipv4.unicast.prefix_sid.absolute if 'prefix_sid' in interface.address_family.ipv4.unicast else None,
                    }

                return isis_info

def main():
    router = 'P1'  # Specify the router to fetch ISIS information

    isis_info = get_isis_info(router)
    print(f"ISIS Information for Router: {router}")
    print(f"Apply Group: {isis_info['apply_group']}")
    print(f"ISIS Type: {isis_info['is_type']}")
    print(f"NET ID: {isis_info['net']}")
    print(f"Distribute Link State: {isis_info['distribute_link_state']}")
    print("IPv4 Unicast:")
    for key, value in isis_info['ipv4_unicast'].items():
        print(f"  {key}: {value}")
    print(f"IPv4 Multicast: {isis_info['ipv4_multicast']}")
    print("Interfaces:")
    for interface, details in isis_info['interfaces'].items():
        print(f"  Interface: {interface}")
        print(f"    IPv4 Unicast: {details['ipv4_unicast']}")
        if details['ipv4_multicast']:
            print(f"    IPv4 Multicast: {details['ipv4_multicast']}")
        if details['prefix_sid_absolute']:
            print(f"    Prefix SID Absolute: {details['prefix_sid_absolute']}")

if __name__ == "__main__":
    main()

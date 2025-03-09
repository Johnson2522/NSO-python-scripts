import sys
sys.path.append('/home/mszabo/nso-6.3/src/ncs/pyapi/')
import ncs
import ncs.maagic as maagic

def get_pce_info(device_name):
    try:
        # Create a connection to NSO
        with ncs.maapi.Maapi() as m:
            # Start a session
            with ncs.maapi.Session(m, 'admin', 'python') as s:
                # Start a read transaction
                with m.start_read_trans() as t:
                    # Get the root object
                    root = maagic.get_root(t)
                    
                    # Access the device
                    device = root.devices.device[device_name]
                    
                    # Access the PCE configuration
                    pce_config = device.config.cisco_ios_xr__pce
                    
                    # Initialize the dictionary to hold PCE information
                    pce_info = {}

                    # Retrieve the PCE address
                    pce_info['address_ipv4'] = pce_config.address.ipv4

                    # Retrieve segment routing traffic engineering configuration
                    sr_traffic_eng = pce_config.segment_routing.traffic_eng

                    # Retrieve segment lists
                    pce_info['segment_lists'] = {}
                    for segment_list in sr_traffic_eng.segment_list:
                        segments = []
                        for index in segment_list.index:
                            segments.append({
                                'id': index.id,
                                'mpls_label': index.mpls.label,
                            })
                        pce_info['segment_lists'][segment_list.name] = segments

                    # Print the collected PCE information
                    print(f"PCE Information for device {device_name}:")
                    print(f"Address IPv4: {pce_info['address_ipv4']}")
                    print("Segment Lists:")
                    for list_name, segments in pce_info['segment_lists'].items():
                        print(f"  Segment List {list_name}:")
                        for segment in segments:
                            print(f"    Index ID: {segment['id']}, MPLS Label: {segment['mpls_label']}")

    except ncs.MaapiError as e:
        print(f"An error occurred: {e}")

# Fetch and print PCE information for device 'P1'
get_pce_info('P2')
get_pce_info('P1')


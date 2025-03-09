import sys
sys.path.append('/home/mszabo/nso-6.3/src/ncs/pyapi/')
import ncs
import ncs.maagic as maagic

def modify_segment_list_mpls(devices, segment_list_name, index_id, new_mpls_label):
    try:
        # Loop through each device in the list
        for device_name in devices:
            # Create a connection to NSO
            with ncs.maapi.Maapi() as m:
                # Start a session
                with ncs.maapi.Session(m, 'admin', 'python') as s:
                    # Start a write transaction
                    with m.start_write_trans() as t:
                        # Get the root object
                        root = maagic.get_root(t)
                        
                        # Access the device
                        device = root.devices.device[device_name]
                        
                        # Access the PCE configuration
                        pce_config = device.config.cisco_ios_xr__pce
                        
                        # Access the segment routing traffic engineering configuration
                        sr_traffic_eng = pce_config.segment_routing.traffic_eng
                        
                        # Access the specific segment list
                        segment_list = sr_traffic_eng.segment_list[segment_list_name]
                        
                        # Check if the given index exists or create a new one
                        if index_id in segment_list.index:
                            segment = segment_list.index[index_id]
                        else:
                            segment = segment_list.index.create(index_id)

                        # Set the new MPLS label
                        segment.mpls.label = new_mpls_label

                        # Apply the changes
                        t.apply()

                        print(f"Modified MPLS label for Segment List '{segment_list_name}' at Index {index_id} on device '{device_name}' to {new_mpls_label}.")

    except ncs.MaapiError as e:
        print(f"An error occurred: {e}")

# Example usage to modify MPLS label on both P1 and P2 routers
devices = ['P1', 'P2']
modify_segment_list_mpls(devices, 'SL3', 1, 16002)
modify_segment_list_mpls(devices, 'SL3', 2, 16013)


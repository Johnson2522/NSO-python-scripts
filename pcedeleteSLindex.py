import sys
sys.path.append('/home/mszabo/nso-6.3/src/ncs/pyapi/')
import ncs
import ncs.maagic as maagic

def delete_segment_list_index(devices, segment_list_name, index_id):
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
                        
                        # Check if the given index exists
                        if index_id in segment_list.index:
                            # Delete the index
                            del segment_list.index[index_id]

                            # Apply the changes
                            t.apply()

                            print(f"Deleted Index {index_id} from Segment List '{segment_list_name}' on device '{device_name}'.")
                        else:
                            print(f"Index {index_id} not found in Segment List '{segment_list_name}' on device '{device_name}'.")

    except ncs.MaapiError as e:
        print(f"An error occurred: {e}")

# Example usage to delete an index from the Segment List on both P1 and P2 routers
devices = ['P1', 'P2']
delete_segment_list_index(devices, 'SL4', 1)
delete_segment_list_index(devices, 'SL4', 2)
delete_segment_list_index(devices, 'SL4', 3)

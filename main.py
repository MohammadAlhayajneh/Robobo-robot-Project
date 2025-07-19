#
# Example of using threads to develop reactive (subsumption) architecture
#

from robobopy.Robobo import Robobo

from behaviour_mod.search_object import SearchObject
from behaviour_mod.approach_object import ApproachObject
from behaviour_mod.search_and_approach_bin import SearchAndApproachBin

import time

def main():
    # Create a Robobo object and connect to the robot
    robobo = Robobo("localhost")
    robobo.connect()

    # Dictionary to share parameters between behaviors
    # The "stop" flag will indicate when the task is complete
    params = {"stop": False}

    # Create behavior instances
    search_object_behaviour = SearchObject(robobo, [], params)
    approach_object_behaviour = ApproachObject(robobo, [search_object_behaviour], params)
    search_and_approach_bin_behaviour = SearchAndApproachBin(robobo, [approach_object_behaviour, search_object_behaviour], params)
    # Additional behaviors (like finding a color) can be defined similarly
    # find_color_behaviour = FindColor(robobo, [follow_wall_behaviour, go_to_wall_behaviour], params, BlobColor.RED)

    # Create a list of all the behaviors in priority order (low to high)
    threads = [search_object_behaviour, approach_object_behaviour, search_and_approach_bin_behaviour]

    # Start all behaviors (threads)
    search_object_behaviour.start()
    approach_object_behaviour.start()
    search_and_approach_bin_behaviour.start()

    # Keep the main thread running
    # This loop checks if the "stop" condition has been triggered
    # When a behavior sets "stop" to True, the loop will end
    while not params["stop"]:
        time.sleep(0.1)  # Small delay to reduce CPU usage

    # Wait for all threads to finish
    # This ensures that all behaviors complete their cleanup before exiting
    for thread in threads:
        thread.join()

    # Disconnect the robot once the mission is complete
    robobo.disconnect()
    print("Robot disconnected")

if __name__ == "__main__":
    main()

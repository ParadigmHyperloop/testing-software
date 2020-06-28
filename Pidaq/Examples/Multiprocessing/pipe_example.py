""" pipe_example.py

Proof of Concept - Controlling a process from another process using a pipe
This example demonstrates the control of one process from another using a Pipe.
The process would be very similar if using a Pool/Queue/Duplex pipe.

In this example the active_test thread controls the telem thread by sending
it messages through a unidirectional pipe. After the telem thread prints an 
arbitrary message for 5 seconds, The active_test thread launches and tells 
the telem thread to print a new message, then 5 seconds later tells it to close.

Simply run using python3 pipe_example.py

"""


from multiprocessing import Pipe, Process
from time import sleep


def telem(timeout: float, message: str, conn):
    """ Print messages received through a pipe until True is received """
    stopLoop = False
    while(not stopLoop):
        # Read pipe and update number
        # Poll for timeout seconds, returns true if data is available 
        if conn.poll(timeout=timeout):
            message = conn.recv()
            if isinstance(message, bool):
                stopLoop = message
        print(message)
    

def active_test(newMsg: str, conn):
    """ Tell telem thread to print a new message or to close """
    # Send the new message to print through the pipe
    conn.send(newMsg)
    sleep(5)
    
    # "Swap back to the old database"
    conn.send("Test complete - using standby database")
    sleep(5)
    
    # Send command to "close" the telem thread
    conn.send(True)
    
    # Close the conn when finished sending data - probably a good idea
    conn.close() 


if __name__ == "__main__":
    # Launch the telemetry thread and commander threads

    # Configure initial message and updated message
    initialMsg = "Using default database"
    newMsg = "Test started - using production database"
    timeout = 1
    
    # Create pipe endpoint connection objects (unidirectional)
    parent_conn, child_conn = Pipe(duplex=False)
    
    # Create "telemetry" process
    p_telem = Process(target=telem, args=(timeout, initialMsg, parent_conn))
    
    # Create "active_test" process
    p_active_test = Process(target=active_test, args=(newMsg, child_conn))
    
    # Run telem thread for 10 seconds before launching active test
    p_telem.start()
    sleep(5)
    p_active_test.start()
    
    # Wait for both processes to complete
    p_active_test.join()
    p_telem.join()
    
    print("Child Processes Complete")
    
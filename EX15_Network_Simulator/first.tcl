# Create a new simulator instance
set ns [new Simulator]

# Open the trace file for general tracing
set tracefile [open "tracefile.tr" w]
$ns trace-all $tracefile

# Open the NAM trace file for visualizing the simulation
set namfile [open "namfile.nam" w]
$ns namtrace-all $namfile

# Create nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]

# Create duplex links between the nodes with specific bandwidth, delay, and queue type
$ns duplex-link $n1 $n2 10Mb 20ms DropTail
$ns duplex-link $n1 $n3 5Mb 10ms DropTail
$ns duplex-link $n2 $n3 100Mb 20ms DropTail
$ns duplex-link $n2 $n4 1Mb 30ms DropTail

# Create and attach the first TCP agent to node 1
set tcp1 [new Agent/TCP]
$tcp1 set class_ 2  ;# Set TCP class to 2 for congestion control
$ns attach-agent $n1 $tcp1

# Create and attach the second TCP agent to node 4
set tcp2 [new Agent/TCP]
$tcp2 set class_ 2  ;# Set TCP class to 2 for congestion control
$ns attach-agent $n4 $tcp2

# Create and attach the first TCP sink agent to node 2
set sink1 [new Agent/TCPSink]
$ns attach-agent $n2 $sink1

# Create and attach the second TCP sink agent to node 2
set sink2 [new Agent/TCPSink]
$ns attach-agent $n2 $sink2

# Connect the TCP agents to the corresponding sink agents
$ns connect $tcp1 $sink1
$ns connect $tcp2 $sink2

# Create an FTP application and attach it to the first TCP agent
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ns at 0.1 "$ftp start"  ;# Start the FTP application at time 0.1s

# Create another FTP application and attach it to the second TCP agent
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ns at 0.1 "$ftp2 start"  ;# Start the second FTP application at time 0.1s

# Set TCP parameters for the first TCP agent
$tcp1 set window_ 20  ;# Set the TCP window size to 20 packets
$tcp1 set maxcwnd_ 40  ;# Set the maximum congestion window to 40 packets

# Set TCP parameters for the second TCP agent
$tcp2 set window_ 20  ;# Set the TCP window size to 20 packets
$tcp2 set maxcwnd_ 40  ;# Set the maximum congestion window to 40 packets


# Define colors for the links in NAM visualization
$ns color 1 Blue  ;# Set color of link 1 to blue
$ns color 2 Red   ;# Set color of link 2 to red

# Define a finish procedure to clean up after the simulation ends
proc finish {} {
    global ns tracefile namfile
    $ns flush-trace  ;# Flush trace data to the file
    close $tracefile  ;# Close the trace file
    close $namfile    ;# Close the NAM trace file
    puts "Simulation finished!"  ;# Print a message indicating the simulation has ended
    exit 0  ;# Exit the simulation
}

# Schedule the finish procedure to be called at 10 seconds
$ns at 10.0 "finish"

# Run the simulation
$ns run

#!/bin/bash

# Written by Michel Thomasius
# Simple BASH project script to make NMAP scans a little bit more user friendly, without having to remember all the switches

# Function to prompt user for input and store it in a variable
# -p is the prompt. "$1" shows the user the prompt, and then $2 stores the user's input for use by the script
get_input() {
  read -p "$1: " $2
}

# Prompt user for scan range (IP or IP range)
get_input "Enter the scan range (IP or IP range)" scan_range

# Prompt user for TCP ports to scan
get_input "Enter TCP ports to scan (comma-separated or range)" tcp_ports

# Prompt user for UDP ports to scan
get_input "Enter UDP ports to scan (comma-separated or range)" udp_ports

# Prompt user for default port range
get_input "Enter default port range" default_port_range

# Prompt user for scan intensity
get_input "Enter scan intensity (Options: 'T0' - Slowest to 'T5' - Most Aggressive)" scan_intensity

# Prompt user for retries
get_input "Enter the number of retries" retries

# If retries is greater than 1, prompt user for max retry time
if [ "$retries" -gt 1 ]; then
  get_input "Enter max retry time in ms" max_retry_time
fi

# Prompt user for output format options
get_input "Enter output format options" output_options

# Assemble the nmap command based on the user inputs
nmap_command="nmap"

if [ -n "$tcp_ports" ]; then
  nmap_command+=" -p $tcp_ports"
fi

if [ -n "$udp_ports" ]; then
  nmap_command+=" -pU:$udp_ports"
fi

if [ -n "$default_port_range" ]; then
  nmap_command+=" --defeat-rst-ratelimit --source-port $default_port_range"
fi

if [ -n "$scan_intensity" ]; then
  nmap_command+=" -$scan_intensity"
fi

if [ -n "$retries" ]; then
  nmap_command+=" --max-retries $retries"
fi

if [ -n "$max_retry_time" ]; then
  nmap_command+=" --max-retries-rtt-timeout $max_retry_time"
fi

if [ -n "$output_options" ]; then
  nmap_command+=" $output_options"
fi

nmap_command+=" $scan_range"

# Prompt user for confirmation
read -p "The following nmap command will be executed: \"$nmap_command\". Do you want to proceed? (y/n): " confirmation

# Check if the user's input is "y" (yes) or "Y" (YES)
if [[ "$confirmation" =~ ^[Yy]$ ]]; then
  # Run the nmap scan with the constructed command
  echo "Running nmap scan with the following command:"
  echo "$nmap_command"
  eval $nmap_command
else
  echo "Nmap scan was not executed. Exiting..."
fi

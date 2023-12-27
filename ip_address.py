import ipaddress

# Function to calculate the number of usable IPs in a network
def calculate_usable_ips(network_cidr):
    network = ipaddress.ip_network(network_cidr, strict=False)
    # For a subnet, typically the first address is reserved for the network address and the last for the broadcast address.
    return network.num_addresses - 2 if network.num_addresses > 2 else 0

# Function to print the details of a vNet and its subnets
def print_network_details(vnet_cidr, subnets_cidr):
    vnet = ipaddress.ip_network(vnet_cidr, strict=False)
    print(f"vNet '{vnet_cidr}' with mask bit {vnet.prefixlen} has {calculate_usable_ips(vnet_cidr)} usable IPs.")

    for subnet_cidr in subnets_cidr:
        subnet = ipaddress.ip_network(subnet_cidr, strict=False)
        print(f"Subnet '{subnet_cidr}' with mask bit {subnet.prefixlen} has {calculate_usable_ips(subnet_cidr)} usable IPs.")

# Function to check if the given IPs or CIDR blocks are within the vNet address spaces
def check_ip_in_vnets(vnets_cidr, ips_to_check):
    # Convert the list of vNet CIDR blocks into a list of network objects
    vnets = [ipaddress.ip_network(vnet, strict=False) for vnet in vnets_cidr]

    # Check each IP or CIDR block against the list of vNet networks
    for ip in ips_to_check:
        ip_obj = ipaddress.ip_network(ip, strict=False)
        within_vnet = any(ip_obj.subnet_of(vnet) for vnet in vnets)
        print(f"IP/CIDR {ip} is within the vNet address spaces: {within_vnet}")

# Example usage:
vnets_cidr = ['10.0.0.0/16', '10.1.0.0/16']  # Replace with your subscription's vNet CIDRs
ips_to_check = ['10.0.0.47', '10.0.1.0/24', '10.2.0.0/24']  # Replace with the IPs/CIDR blocks you want to check

check_ip_in_vnets(vnets_cidr, ips_to_check)


# Example usage:
vnet_cidr = '10.0.0.0/16'  # Replace with your vNet CIDR
subnets_cidr = ['10.0.0.0/24', '10.0.1.0/24']  # Replace with your subnet CIDRs

print_network_details(vnet_cidr, subnets_cidr)

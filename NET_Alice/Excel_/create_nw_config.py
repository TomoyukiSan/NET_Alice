

def create_cisco_config(port_number: str = None,
                        vlan: int = None,
                        ip_address: str = None,
                        subnet_mask: str = None,
                        description: str = None):

    config: str = ""
    if port_number is not None:
        config += f"interface {port_number}\n"

    if vlan is not None:
        config += f"switchport mode access\n"
        config += f"switchport access vlan {vlan}\n"

    if ip_address is not None and subnet_mask is not None:
        config += f"ip address {ip_address} {subnet_mask}\n"

    if description is not None:
        config += f"description {description}\n"

    return config

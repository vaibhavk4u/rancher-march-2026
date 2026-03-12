#!/usr/bin/env python3
import subprocess
import time
import re
import json

# Define VMs and hostnames
vm_list = [
    {"name": "rancher-vm", "hostname": "rancher.tektutor.org"},
    {"name": "cluster1-master", "hostname": "cluster1-master.tektutor.org"},
    {"name": "cluster1-worker", "hostname": "cluster1-worker.tektutor.org"},
    {"name": "cluster2-master", "hostname": "cluster2-master.tektutor.org"},
    {"name": "lb-vm", "hostname": "lb.tektutor.org"},
]

def get_ip(vm_name, retries=5, delay=2):
    """Get the IP address of a VM using 'virsh domifaddr'"""
    for i in range(retries):
        try:
            result = subprocess.run(
                ["virsh", "domifaddr", vm_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout
            match = re.search(r"ipv4\s+([\d\.]+)/\d+", output)
            if match:
                return match.group(1)
        except Exception:
            pass
        time.sleep(delay)
    return "0.0.0.0"

def main():
    # Initialize inventory structure
    inventory = {
        "_meta": {"hostvars": {}},
        "all": {
            "children": ["rancher_upstream", "cluster1", "cluster2", "ungrouped"],
            "vars": {
                "ansible_user": "root",
                "ansible_ssh_common_args": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
            }
        },
        "rancher_upstream": {"hosts": ["rancher-vm"]},
        "cluster1": {
            "children": ["cluster1_master", "cluster1_worker"]
        },
        "cluster1_master": {"hosts": ["cluster1-master"]},
        "cluster1_worker": {"hosts": ["cluster1-worker"]},
        "cluster2": {"hosts": ["cluster2-master"]},
        "lb": {"hosts": ["lb-vm"]}
    }

    for vm in vm_list:
        name = vm["name"]
        ip = get_ip(name)
        
        # Build hostvars for each VM
        inventory["_meta"]["hostvars"][name] = {
            "ansible_host": ip,
            "hostname": vm["hostname"]
        }

    print(json.dumps(inventory, indent=2))

if __name__ == "__main__":
    main()

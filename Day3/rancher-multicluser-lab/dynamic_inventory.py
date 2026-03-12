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

def get_ip(vm_name, retries=12, delay=5):
    """Get the IP address of a VM using 'virsh domifaddr' output parsing"""
    for i in range(retries):
        try:
            result = subprocess.run(
                ["virsh", "domifaddr", vm_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output = result.stdout
            # Example line: vnet0     ipv4  192.168.122.211/24  ...
            match = re.search(r"ipv4\s+([\d\.]+)/\d+", output)
            if match:
                return match.group(1)
        except Exception:
            pass
        time.sleep(delay)
    return "0.0.0.0"  # fallback if IP not found

# Build inventory
inventory = {
    "_meta": {"hostvars": {}},
    "rancher_upstream": {"hosts": []},
    "cluster1": {"hosts": []},
    "cluster2": {"hosts": []},
}

for vm in vm_list:
    ip = get_ip(vm["name"])
    inventory["_meta"]["hostvars"][vm["name"]] = {
        "ansible_host": ip,
        "ansible_user": "root",
        "ansible_password": "root",
        "ansible_ssh_extra_args": "-o StrictHostKeyChecking=no",
        "hostname": vm["hostname"]
    }
    # Assign groups
    if vm["name"] in ["rancher-vm", "cluster1-master", "cluster1-worker"]:
        inventory["rancher_upstream"]["hosts"].append(vm["name"])
    if vm["name"] in ["cluster1-master", "cluster1-worker"]:
        inventory["cluster1"]["hosts"].append(vm["name"])
    if vm["name"] == "cluster2-master":
        inventory["cluster2"]["hosts"].append(vm["name"])

print(json.dumps(inventory, indent=2))

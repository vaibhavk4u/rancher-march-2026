#!/bin/bash

for vm in rancher-vm cluster1-master cluster1-worker cluster2-master lb-vm; do   sudo virsh destroy $vm 2>/dev/null;   sudo virsh undefine $vm --remove-all-storage 2>/dev/null; done


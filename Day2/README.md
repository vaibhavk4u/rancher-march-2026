# Day 2

## Lab - Let's automate RKE2 cluster setup using Rancher

This is our plan
<pre>
- Let's create a golden image to create thin-clone with KVM, this will reduce the actual disk usage.
- We will have to install RHEL v9.7 manually on the golden image, later we will clone this image to setup other VMs
- We will setup a single node RKE2 to setup Rancher
- Using Terraform, let's provision VMs using KVM
- Let's automate the RKE2 cluster setup using Rancher
</pre>

Create a golden RHEL image with qcow2
```
qemu-img create -f qcow2 rhel9-golden.qcow2 40G
```

Install RHEL v9.7 using the RHEL DVD iso
```
sudo virt-install \
--name rhel9-golden \
--ram 4096 \
--vcpus 2 \
--disk path=/var/lib/libvirt/images/rhel9-golden.qcow2,size=40 \
--os-variant rhel9.7 \
--location /var/lib/libvirt/images/rhel-9.7-x86_64-dvd.iso \
--network network=default \
--graphics vnc
```



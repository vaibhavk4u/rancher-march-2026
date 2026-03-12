# Day 5

## Info - Setup a rancher cluster with Cilium and Traefic Ingress Controller

Note
<pre>
- By default, RKE2 ships with Canal (Calico + Flannel) and Traefik
- In our cluster setup, we will be using Cilium in the place of Canal
</pre>

Create a lightweight VM using podman
```
podman machine init rancher --cpus 4 --memory 8192 --disk-size 50
podman machine start rancher
podman machine ssh rancher
sudo hostnamectl set-hostname rancher.tektutor.org
hostname
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/38d19e7a-57c4-400a-a9f0-cbcf80e6a4bb" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/06f15de2-6090-4eb3-a4d1-6a50021ea6c0" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/49b98704-0cc1-4690-b0d9-6f82fbde6e4d" />


Create configuration directories
```
sudo mkdir -p /etc/rancher/rke2/
sudo mkdir -p /var/lib/rancher/rke2/server/manifests/
```

Define Cluster Configurations
```
cat <<EOF | sudo tee /etc/rancher/rke2/config.yaml
cni: cilium
write-kubeconfig-mode: "0644"
EOF
```

Enable Hubble
```
cat <<EOF | sudo tee /var/lib/rancher/rke2/server/manifests/rke2-cilium-config.yaml
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-cilium
  namespace: kube-system
spec:
  valuesContent: |-
    hubble:
      enabled: true
      ui:
        enabled: true
      relay:
        enabled: true
EOF
```

Download RKE2 binaries
```
curl -sfL https://get.rke2.io | sudo INSTALL_RKE2_METHOD="tar" sh -
```

Start the RKE2 Cluster
```
sudo systemctl daemon-reload
sudo systemctl enable rke2-server.service
sudo systemctl start rke2-server.service
sudo systemctl status rke2-server.service
sudo rke2 server status
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/b2a77898-8bb6-4d64-8285-c99ba446d5a7" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/4e18cd88-ae73-4fdd-99de-a8e17ad16c11" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/daac684a-afaf-4b49-a2b3-496de60559cc" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/7d3d1764-ff40-49a3-8480-451195f19fc9" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/7d6e138b-eb9b-49be-8f39-3aa5cd4f242f" />

Test the cluster
```
mkdir ~/.kube
sudo cp /etc/rancher/rke2/rke2.yaml $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
chmod 600 $HOME/.kube/config
sudo ln -s /var/lib/rancher/rke2/bin/kubectl /usr/local/bin/kubectl
kubectl get pods -A
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/f7ec8048-5c19-440f-be37-5707dca37d2f" />

# Day 4

## Lab - Rancher with two clusters

List the clusters from the rancher vm
```
kubectl get clusters.management.cattle.io -o custom-columns="ID:.metadata.name,NAME:.spec.displayName"
```
<img width="480" height="300" alt="image" src="https://github.com/user-attachments/assets/8559ad39-22e3-46ba-8c45-1993a48392e3" />

My Rancher Management GUI looks as below
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/ff4fc67f-c2c7-4ba2-bbe4-bb8d5770b075" />

Let's create a Cluster Group. On your Ranger Webconsole, click on Continuous Delivery
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/c272b3fd-c112-4cd6-abf8-3b021d9d9277" />
Now, let's create a Cluster Group named "tektutor-cluster-group"
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/f92e1a66-201f-41b4-8b34-231b309ef80c" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/e7034ce7-5564-4138-baca-276497768a2c" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/acd82804-6a28-4856-9b95-4c6f05c0fdcf" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/38fb95de-38fb-4474-885e-3c7e71028b08" />

Let's make the cluster1 as dev and cluster2 as prod environment
```
kubectl label clusters.management.cattle.io c-6fvtr env=dev project=tektutor --overwrite
kubectl label clusters.management.cattle.io c-j2759 env=prod project=tektutor --overwrite

# List both cluster along with the labels 
kubectl get clusters.management.cattle.io -L env,project
```
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/deb8067a-f720-40ab-a325-ae0dc977d57f" />

Let's add the GitOps to Fleet
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/49cfb179-6437-4910-9a7d-6582e31b9b45" />
Create Git Repo and Click Next
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/07effce3-562a-4d88-87e8-8da0956607ff" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/ff514994-4855-4253-afa7-7ef561d64b0b" />
Click Next
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/24410595-0ddb-46cd-984c-fff252fbda61" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/7b42b5b0-a3e1-4e6b-b8cb-7a9b7eb3f2c1" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/56e0d61d-9364-4c25-8015-c214dd173cbb" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/559da9a0-912c-4490-bb9f-32a851fe5cf7" />

I pushed the nginx deployment manifest(yaml) file to my github repo
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/2a6ec200-4932-41c9-a92b-e66d0e8b3170" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/29b21953-1b46-4328-995d-096b5d4381a3" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/f69fd424-8bfa-4863-87a7-c0e4bf7e4076" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/bf8f59f4-c6c6-4036-9d9b-697a80706831" />

Making sure our cluster1 and cluster2 rancher agent is running
```
kubectl logs -f -n cattle-system -l app=cattle-cluster-agent
```
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/7e990f6f-73b0-4275-ba7c-2a323abac13c" />
<img width="1911" height="1111" alt="image" src="https://github.com/user-attachments/assets/46ccf8f1-d96f-4b8e-a408-9820cfeec297" />


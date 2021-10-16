# Flask contacts for Kubernetes

This is a basic tutorial to run a flask application on kubernetes. My goal is to give you a practial ideia about deploying kubernetes app, please feel free to contribute and to suggest enhancements.

Main components:
1. app/flask-contact-deploy.yaml --> the kubernetes deployment for the web application built with Python, Flask and apache (wsgi module)
2. app/flask-contact-job.yaml  --> the kubernetes job to randonly insert initial pieces of data for our contacts 
3. app/mysql-deploy.yaml --> the kubernetes deployment for our MySql Database.


# Bulding and pushing the app images to DockerHub

The fisrt requirement is Docker, that is used to build the images for the app and also to pull/push updates in our registry.

Installing Docker in Linux https://docs.docker.com/engine/install/: <br/>
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Now, create an account in DockerHub (https://hub.docker.com/)
Then login into your accout:
```
docker login
```
To build the images:
1. Go to conf-init-db-job folder:  <br/>
```
docker build -t $(DOCKERHUBUSER)/flask-contacts:conf-init-db-job .
docker push $(DOCKERHUBUSER)/flask-contacts:conf-init-db-job
```
2. Go to flask-contacts-deploy:  <br/>
```
docker build -t $(DOCKERHUBUSER)/flask-contacts:flask-contacts-deploy .
docker push $(DOCKERHUBUSER)/flask-contacts:flask-contacts-deploy
```
**Replace $(DOCKERHUBUSER) with your user**

# Deploying on Kubernetes

You need a Kubernetes cluster with at least 1 Master + 1 Worker nodes. I personally recomend to build your cluster using Ubuntu VM's + kubeadm (1.  https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/     2. https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

For the next steps, you must have kubecetl installed and liked to your cluster

1. First of all, create the namespace for the app and set the service account permissions:  <br/>
```
kubectl apply -f https://raw.githubusercontent.com/mauromatsudo/flask-app-for-k8s/master/k8s/access.yaml
```
2. For security reasons, there is a NetworkPolicy who prevents access to your database pod:  <br/>
```
kubectl apply -f https://raw.githubusercontent.com/mauromatsudo/flask-app-for-k8s/master/k8s/netpolicy.yaml
```
3. Now is the annoying part. As we need a persistent volume to maintain the contacts data, I decided to create a NFS volume beacause it could be shared among all the worker nodes, although it is not suitable for prodution environment and also takes some effort.
So lets install the NFS Server on the master node: <br/>
```
sudo apt update && apt install -y nfs-server
sudo mkdir /opt/flask_contact
sudo chmod 777 /opt/flask_contact
sudo echo "/opt/flask_contact 192.168.111.0/24(rw,sync,no_root_squash,no_subtree_check)" >> /etc/exports # the ip 192.168.111.0 is cluster my network, change it with your network address
sudo export -a
```
Then, let's mount the shared on worker nodes (do this in each worker node): <br/>
nos worker nodes
```
sudo apt update && apt install -y nfs-client
sudo mkdir /db
sudo echo "192.168.111.135:/opt/flask_contact /db nfs" >> /etc/fstab
sudo mount -a
```
Finally, we can create your persistent volume based on the NFS: <br/>
```
kubectl appy -f https://github.com/mauromatsudo/flask-app-for-k8s/blob/master/k8s/app/storage.yaml
```

4. During this step, the dockerhub registry is set as the source of images.
```
kubectl create secret docker-registry regcred --docker-server=hub.docker.com --docker-username=$dockerUser--docker-password=$dockerPassword --docker-email=$dockerEmail -n flask-contacts 
```

5. The MySQL root password should be securily stored using a secret.
```
kubectl create secret generic flask-contacts-sec -n flask-contacts --from-literal=db_root_password=${CHOOSEAPASSWORD}
```
6. After creating the secret, it's possible to run the MySQL Deployment
```
kubectl apply -f https://github.com/mauromatsudo/flask-app-for-k8s/blob/master/k8s/app/mysql-deploy.yaml
```
7. Non-sensitive informations are stored in ConfigMaps:
```
kubectl apply -f https://raw.githubusercontent.com/mauromatsudo/flask-app-for-k8s/master/k8s/app/flask-contact-confmap.yaml
```
8. conf-init-db ins a job which inserts some random data into MySQL ṕod:
```
kubectl apply -f https://raw.githubusercontent.com/mauromatsudo/flask-app-for-k8s/master/k8s/app/conf-init-db.yaml
```
9. Finally, we can deploy the app:
```
kubectl apply -f https://raw.githubusercontent.com/mauromatsudo/flask-app-for-k8s/master/k8s/app/flask-contact-deploy.yaml
```
10. To access/test the app:
```
sudo echo "{IP_ADDR_FROM_ANY_NODE} flask-contacts.com >> /etc/hosts"
```
Use curl, wget or even your browser: http://flask-contacts.com:32000

[DEMO](https://flaskcontacts.herokuapp.com/)

![alls](https://github.com/tanrax/flask-contacts/raw/master/screenshots/alls.jpg)

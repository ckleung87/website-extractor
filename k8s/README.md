# kubernetes Deployment
An example to deploy the Website Extractor with K8s.

# Deploy with EKS

## 1. Create EKS cluster in AWS
- Create cluster
- Add Node group

## 2. Set AWS Crediental
- install aws-cli
- set crediental
- https://docs.aws.amazon.com/cli/latest/reference/configure/

## 3. Set EKS Config
- aws eks update-kubeconfig --name <eks-cluster-name> --region <aws-region>

## 4. Verify EKS Cluster
- aws sts get-caller-identity
- kubectl get nodes

# Deploy with Docker Decktop

## 1. Install Docker
- Mac: https://docs.docker.com/docker-for-mac/install/

## 2. Enable K8s
- https://docs.docker.com/docker-for-mac/#kubernetes

## 3. Verify Cluster
- aws sts get-caller-identity
- kubectl get nodes

# Deploy with EKS

## 1. Set EKS Config
- kubectl config use-context docker-for-desktop

## 2. Verify EKS Cluster
- aws sts get-caller-identity
- kubectl get nodes

# Deploy Service

## 1. Install helm
* https://github.com/helm/helm

## 2. Install k8s dashboard
* https://artifacthub.io/packages/helm/k8s-dashboard/kubernetes-dashboard

## 3. Install aws-efs-csi-driver (EKS Deployment)
Install this plugin to mount EFS drive to K8s as a Persistent Volume
```
helm repo add aws-efs-csi-driver https://kubernetes-sigs.github.io/aws-efs-csi-driver/
helm upgrade --install aws-efs-csi-driver --namespace kube-system aws-efs-csi-driver/aws-efs-csi-driver
```

## 4. Install Website Extractor Service
```
helm install -f ./extractor/values.dev.yaml extractor ./extractor
```

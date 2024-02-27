aws sts get-caller-identity
aws eks update-kubeconfig --name <eks-cluster-name> --region <aws-region>
kubectl get nodes

helm version
helm ls

# Inti
#helm install -f ./extractor/values.dev.yaml extractor ./extractor

#upgrade
helm upgrade -f ./extractor/values.dev.yaml extractor ./extractor
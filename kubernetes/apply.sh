kubectl apply -f namespaces.yml

kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"

sleep 60

kubectl apply -f deployments/rabbitmq.yml

sleep 120

RABBITMQ_PASSWORD=$(kubectl get secret rabbitmq-default-user -o jsonpath="{.data.password}" -n rabbitmq-namespace | base64 --decode)
RABBITMQ_USER=$(kubectl get secret rabbitmq-default-user -o jsonpath="{.data.username}" -n rabbitmq-namespace | base64 --decode)

# Crear un nuevo ConfigMap con las credenciales de RabbitMQ
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: rabbit-config
  namespace: applications-namespace
data:
  RABBITMQ_USER: $RABBITMQ_USER
  RABBITMQ_PASSWORD: $RABBITMQ_PASSWORD
  RABBITMQ_HOST: rabbitmq.rabbitmq-namespace.svc.cluster.local
EOF

# Crear un nuevo ConfigMap con las credenciales de GCP
kubectl create configmap -n applications-namespace credentials-config --from-file=../credentials.json

kubectl apply -f config.yml

kubectl apply -f volumes/redis-data.yml

kubectl apply -f deployments/redis-master.yml
kubectl apply -f deployments/redis-replica.yml
kubectl apply -f services/redis-master.yml
kubectl apply -f services/redis-replica.yml

kubectl apply -f deployments/entry-server.yml
kubectl apply -f deployments/split-service.yml
kubectl apply -f deployments/join-service.yml
kubectl apply -f services/entry-server.yml
kubectl apply -f services/split-service.yml
kubectl apply -f services/join-service.yml

1. Clonar o docker-compose
```sh
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'
```
2. alterar o docker-compose.yml para que fique como abaixo:
```yml
  # Trocar para LocalExecutor
  AIRFLOW__CORE__EXECUTOR: LocalExecutor

  # deletar as duas linhas
  AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
  AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0

  # deletar toda a seção airflow-worker
  airflow-worker:
    # ...

  # deletar essas linhas de dependencias
  redis:
      condition: service_healthy

  # deletar toda a seção sobre redis
  redis:
    # ...

  # deletar toda a seção flower
    flower:
      # ...
```


x. criar um `airflow_runner.sh` com o conteúdo abaixo
```sh
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

y. conceder permissão de execução ao `airflow_runner.sh`
```sh
chmod +x airflow_runner.sh 
```

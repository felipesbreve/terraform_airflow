from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

BASE_DIR = 'cd /home/felipe/terraform/terraform_aws/primeira_instancia/; '

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    # 'retries': 1,
}

# Crie o DAG
dag = DAG(
    'send_to_bq_with_terraform',
    default_args=default_args,
    description='Envia arquivos para o BigQuery com Terraform',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['Terraform', 'BigQuery'],
)

# Inicializa o Terraform
init_task = BashOperator(
    task_id='terraform_init',
    bash_command=f'{BASE_DIR} terraform init',
    dag=dag,
)

# Planeja a execução do Terraform
plan_task = BashOperator(
    task_id='terraform_plan',
    bash_command=f'{BASE_DIR} terraform plan',
    dag=dag,
    on_failure_callback=lambda context: print("Erro no planejamento do Terraform."),
)

# Aplica o Terraform
apply_task = BashOperator(
    task_id='terraform_apply',
    bash_command=f'{BASE_DIR} terraform apply -auto-approve',
    dag=dag,
)

# Destroi o Terraform
destroy_task = BashOperator(
    task_id='terraform_destroy',
    bash_command=f'{BASE_DIR} terraform destroy -auto-approve',
    dag=dag,
    trigger_rule=TriggerRule.ALL_DONE
)

# Defina as dependências entre as tasks
init_task >> plan_task >> apply_task >> destroy_task

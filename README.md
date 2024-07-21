Neste projeto, configurei uma DAG no Airflow para provisionar uma instância EC2, com Terraform, e realizar a ingestão de dados em um dataset no BigQuery.
![image](https://github.com/user-attachments/assets/5f00c35c-c4f2-40fd-9c89-c74086ba0a42)

As taks desta DAG consistem, basicamente, nas etapas de execução do Terraform
![image](https://github.com/user-attachments/assets/c9cd4199-3a61-4bfa-992f-266b82d2ac35)

Um ponto importante de configuração é que na task de _detroy_ seja configurado para rodar mesmo que a etapa de _apply_ falhe, pois é muito provável que a máquina seja criada.
Esta configuração é feita alterando o parâmetro `trigger_rule=TriggerRule.ALL_DONE`
![image](https://github.com/user-attachments/assets/5bfce3d0-c599-4f28-9eb6-d16b4150e94f)

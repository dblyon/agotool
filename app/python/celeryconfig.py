# broker_url = 'pyamqp://'
broker_url = 'amqp://agotool:lightspeed@localhost:5672/agotool'
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True
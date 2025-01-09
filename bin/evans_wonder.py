import oracle_connect2 as oracle_connect
import pandas as pd
from keepass_connect import get_keepass_entry
import os
from msTeam import msteam
from logMessage import logMessage as lm
from keepass_connect import get_keepass_entry
# Step 2 connect to an oracle database
query = f'''
SELECT job, schema_user, last_date, this_date, failures, broken, what
FROM dba_jobs
where JOB = 83
'''
SITE = get_keepass_entry('Webhook For Teams Monitoring', 'password')
# SITE = "https://envirotechservices0.webhook.office.com/webhookb2/1413ff64-a59e-409f-9eff-01d6338b2825@0503c475-d695-4a93-b708-cd271f1b183c/IncomingWebhook/e66ca7b77457418399194ecc74dca030/0a11c728-296e-46db-9549-ffe889c558e4"
file_path = r"C:\Users\esisvc\Projects\Workflow_monitoring\log\wonderware.txt"
#print(query)
# # Parse Data
lib_dir = r"C:\Users\esisvc\Oracle\instantclient_21_7"
os.chdir(lib_dir)
orc = oracle_connect.Oracle()
orc.connect_node()

try:
    orc.execute_node(sql=query, commit=False)
    data = orc.cursor.fetchall()
    col_names = []
    for i in range(0, len(orc.cursor.description)):
        col_names.append(orc.cursor.description[i][0])
    dataset = pd.DataFrame(data)
    #print(dataset.head())
    dataset = pd.DataFrame(data, columns=col_names)
finally:
    orc.disconnect_node()


failures_count = dataset['FAILURES'].iloc[0] 
broken = dataset['BROKEN'].iloc[0]
#dataset.columns = col_names
# Assuming 'dataset' is a pandas DataFrame containing a 'failures' column
if failures_count > 0 and broken == 'Y':
    msteam(SITE, f"There are {failures_count} failures associated with the Evans Wonderware software and the JOB is broken, please check ORCL server and investigate the problem further", ['Trent Radford', 'Chris Delaney'])
elif failures_count > 0 and broken == 'N':
    msteam(SITE, f"There are {failures_count} failures associated with the Evans Wonderware software but the JOB is not broken yet, please check ORCL server and investigate the problem further", ['Trent Radford', 'Chris Delaney'])
else:
    lm(file_path, "No errors, not broken")
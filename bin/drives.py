import shutil
from msTeam import msteam
from logMessage import logMessage as lm
from keepass_connect import get_keepass_entry
# Step 2 connect to an oracle database

SITE = get_keepass_entry('Webhook For Teams Monitoring', 'password')
# SITE = "https://envirotechservices0.webhook.office.com/webhookb2/1413ff64-a59e-409f-9eff-01d6338b2825@0503c475-d695-4a93-b708-cd271f1b183c/IncomingWebhook/e66ca7b77457418399194ecc74dca030/0a11c728-296e-46db-9549-ffe889c558e4"
file_path = r"C:\Users\esisvc\Projects\Workflow_monitoring\log\drives.txt"
#print(query)
# # Parse Data

try:
    # Get the disk usage statistics for the C: drive
    total, used, free = shutil.disk_usage("C:\\")

    # Convert the values to GB for better readability
    total_gb = total / (1024 ** 3)
    used_gb = used / (1024 ** 3)
    free_gb = free / (1024 ** 3)

    ratio = (used_gb / total_gb) * 100 

    lm(file_path, f"ESIPYDEV Total Capacity: {total_gb:.2f} GB")
    lm(file_path, f"ESIPYDEV Used Space: {used_gb:.2f} GB")
    lm(file_path, f"ESIPYDEV Free Space: {free_gb:.2f} GB")
    lm(file_path, f"ESIPYDEV Ratio: {ratio:.2f} %")
except FileNotFoundError:
    lm(file_path, "Could not access ESIPYDEV. Ensure the server and share are accessible.")
network_path = r"\\ESISQL\c$"  # Example: \\192.168.1.100\C$

try:
    total_sql, used_sql, free_sql = shutil.disk_usage(network_path)

    total_sql__gb = total_sql / (1024 ** 3)
    used_sql_gb = used_sql / (1024 ** 3)
    free_sql_gb = free_sql / (1024 ** 3)
    ratio_sql = (used_sql_gb / total_sql__gb) * 100 
    lm(file_path, f"ESISQL Total Capacity: {total_sql__gb:.2f} GB")
    lm(file_path, f"ESISQL Used Space: {used_sql_gb:.2f} GB")
    lm(file_path, f"ESISQL Free Space: {free_sql_gb:.2f} GB")
    lm(file_path, f"ESISQL Ratio: {ratio_sql:.2f} %")
except FileNotFoundError:
    lm(file_path, "Could not access ESISQL. Ensure the server and share are accessible.")
    
network_path1 = r"\\envirodb01\c$"  # Example: \\192.168.1.100\C$

try:
    total_env, used_env, free_env = shutil.disk_usage(network_path1)

    total_env__gb = total_env / (1024 ** 3)
    used_env_gb = used_env / (1024 ** 3)
    free_env_gb = free_env / (1024 ** 3)
    ratio_env = (used_env_gb / total_env__gb) * 100 
    lm(file_path, f"envirodb01 Total Capacity: {total_env__gb:.2f} GB")
    lm(file_path, f"envirodb01 Used Space: {used_env_gb:.2f} GB")
    lm(file_path, f"envirodb01 Free Space: {free_env_gb:.2f} GB")
    lm(file_path, f"envirodb01 Ratio: {ratio_env:.2f} %")
except FileNotFoundError:
    lm(file_path, "Could not access Envirodb01. Ensure the server and share are accessible.")    
    

# Define a flag to track if any drive is almost full
alert_triggered = False

if ratio >= 93:
    msteam(SITE, f"ESIPYDEV c-drive is almost full, it is at {ratio:.2f}% please make space", ['Trent Radford', 'Chris Delaney'])
    alert_triggered = True  # Set flag to true when an alert is triggered

if ratio_sql >= 93:
    msteam(SITE, f"ESISQL c-drive is almost full, it is at {ratio_sql:.2f}% please make space", ['Trent Radford', 'Chris Delaney'])
    alert_triggered = True

if ratio_env >= 93:
    msteam(SITE, f"Envirodb01 c-drive is almost full, it is at {ratio_env:.2f}% please make space", ['Trent Radford', 'Chris Delaney'])
    alert_triggered = True

# If no alerts were triggered, log a message indicating sufficient space
if not alert_triggered:
    lm(file_path, "All drives have room")

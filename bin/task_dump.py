import win32com.client

from logMessage import logMessage as lm
import socket
from msTeam import msteam
from datetime import date


today = date.today().strftime('%Y-%m-%d')
host = socket.gethostname()
LOG = r'C:\Users\esisvc\Projects\Monitoring\log\Monitoring_log.txt'
print(today)
site = "https://envirotechservices0.webhook.office.com/webhookb2/1413ff64-a59e-409f-9eff-01d6338b2825@0503c475-d695-4a93-b708-cd271f1b183c/IncomingWebhook/e66ca7b77457418399194ecc74dca030/0a11c728-296e-46db-9549-ffe889c558e4"
# site = "https://envirotechservices0.webhook.office.com/webhookb2/1413ff64-a59e-409f-9eff-01d6338b2825@0503c475-d695-4a93-b708-cd271f1b183c/IncomingWebhook/ac1230c14741498a9e3b445f88267866/0a11c728-296e-46db-9549-ffe889c558e4"
# msteam(site, "Starting Scheduled Task Monitoring", "Trent Radford")
try:
    msteam(site, "Starting Scheduled Task Monitoring", ['Trent Radford', 'Chris Delaney'])
    TASK_ENUM_HIDDEN = 1
    TASK_STATE = {
        0: 'Unknown',
        1: 'Disabled',
        2: 'Queued',
        3: 'Ready',
        4: 'Running'
    }

    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    n = 0
    folders = [scheduler.GetFolder('\\Python Tasks')]
    while folders:
        folder = folders.pop(0) if folders else None
        if folder is not None:
            sub_folders = list(folder.GetFolders(0))
            folders += sub_folders if sub_folders else []
            tasks = list(folder.GetTasks(TASK_ENUM_HIDDEN))
            n += len(tasks)
            for task in tasks:
                last_run_time_str = str(task.LastRunTime) if task.LastRunTime else "Unknown"
                split = last_run_time_str.split(" ") if last_run_time_str else ["Unknown"]
                if len(split) > 0:
                    task_state = TASK_STATE.get(task.State, "Unknown")
                    if task_state == "Ready":
                        if task.LastTaskResult == 0:
                            lm(LOG, f"{task.Name} ran successfully at {split[0]}")
                        else:
                            if split[0] == today:
                                msteam(site, f"Task {task.Name}, ran Today, but failed with error code {task.LastTaskResult}", ["Trent Radford", "Chris Delaney"])
                            else:
                                msteam(site, f"Task {task.Name}, did not run today and is in a failed state", ["Trent Radford", "Chris Delaney"])
                    else:
                        lm(LOG, f"{task.Name} is not ready, its state is {task_state}")
    lm(LOG, f'Listed {n} tasks.')

except Exception as e:
    msteam(site, f"WARNING! The Task Monitoring python script is NOT WORKING and is throwing the following Error: {e}! PLEASE log into \\\\{host}\\c$\\Users\\esisvc\\Projects\\Monitoring\\bin to investigate the issue. \n", ["Trent Radford", "Chris Delaney"])


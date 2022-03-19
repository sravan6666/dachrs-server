FLASK_ENV=development
FLASK_APP=App.py
APP_DEBUG_MODE=True
MONGO_TASKS_COLLECTION=tasks
MONGO_PROJECT_COLLECTION=projects
MONGO_EPIC_COLLECTION=epic
MONGO_STORY_COLLECTION=story
MONGO_PROGRAM_COLLECTION=program
MONGO_USERS_COLLECTION=user
MONGO_ROLES_COLLECTION=role
MONGO_TASKBOARD_COLLECTION=task_board
MONGO_TASKBOARDSTATUS_COLLECTION=task_board_status
MONGO_COMPANY_COLLECTION=company
MONGO_TEAM_COLLECTION=team
DEFAULT_TASKBOARD_COLUMNS=Backlog,To-Do,In Progress,Completed

FILE_LOCAL_PATH=./data

# Secure data
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=kanbanuat;AccountKey=/KD1v2GNhzQJdPQMYPEMWNPEI1MaOJ7CkhZHkUkd/eVI2W6xZ+I7TOygUDeUBO/91FA/jkHafiFLpU8R7DLACg==;EndpointSuffix=core.windows.net"
MONGO_CONNECTION_STR=mongodb://kanbandachrs:UfYcBuLcWSapeQi7PvakgneeWyOe6G1Hn4O8e4qiwLvI6czynHyOXCy75xlFNofAevNbbQ9MdheRKlPaMGXQow==@kanbandachrs.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@kanbandachrs@
#MONGO_CONNECTION_STR=MONGO-CONNECTION-URL
; MONGO_CONNECTION_STR = mongodb://localhost:27017/
MONGO_DB=kanban-dev
SENDGRID_API_KEY=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

KEY_VAULT_NAME=kanban-dev-kw
#	id of an Azure Active Directory application
AZURE_CLIENT_ID=0bb470e9-49c9-43e1-a2c6-07a1e7c55757
#	id of the application's Azure Active Directory tenant 
AZURE_TENANT_ID=19067814-6baf-41b4-94bc-1b498c041ba2
#	one of the application's client secrets
AZURE_CLIENT_SECRET=
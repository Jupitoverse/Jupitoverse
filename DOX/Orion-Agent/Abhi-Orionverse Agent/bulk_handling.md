Input Box:-

Tab: "Bulk Handling":-



B1: Bulk Retry  			:Single big text Box and Submit Button: Text Box would take these three values in comma separateded and then line wise line:activity_ids, plan_ids , error_id
B2: Bulk Force Complete     :Single big text Box and Submit Button: Text Box would take these three values in comma separateded and then line wise line:activity_ids, plan_ids , error_id
B3: Bulk Rework        :Single big text Box and Submit Button: Text Box would take these three values in comma separateded and then line wise line:activity_ids, plan_ids 
B4: Bulk Resolve Error      :Single big text Box and Submit Button: Text Box would take these three values in comma separateded and then line wise line:activity_ids, plan_ids , error_id
B5: Complete Stuck Activity :Single big text Box and Submit Button: Text Box would take these three values in comma separateded and then line wise line:activity_ids, plan_ids 
B6: Bulk Flag Release:      :One small box for attribute_name, One small box for "flag" value and then One Big text Box for multi line projectid and then  Submit Button: projectid, single value for :flag,attribute_name

all big text box should show number of lines too 
Also after commiting it should throw the no of opeartion performed on UI like "n" activity retried like this.
On Clicking Submit ,it should ask with pop up for confirmation(Yes or No)with the number of line count placed in big input box.


Get Authorization Code:-

We have to pass this auth code as a bearer token in below python script running behind each sub tab.


B1: Bulk Retry              # Retry failed orders/activities in bulk 
B2: Bulk Force Complete     # Force complete stuck orders
B3: Bulk Re-execute         # Re-execute workflows from specific steps  #nahi hai
B4: Bulk Resolve Error      # Resolve errors in bulk   #nahi hai
B5: Complete Stuck Activity # Complete stuck activities

#Common Bulk Handling Script:-
#==============================


import requests
 
# Inputs from UI:- List of plan_ids and activity_ids ,project_ids , error_id 


plan_ids = []  # Replace with your actual plan IDs like '0F30089DABAC4A79A50EF9C8C87F45611737061897','F9FC0070A02C4387AAABF618FA1506311737065038'
activity_ids = []  # Replace with your actual activity IDs like '99A1C7B722584BC5A1617007D03015E2','A70327A634EC48238035F813E574EC21'
project_ids=[] # replace project IDs like 'Project1449179','Project323863'
error_id =[] # replace error IDs



#Base URL

B1_Retry = ""
B2_FC = ""
B3_Rework = "https://oso.orion.comcast.com/frontend-services-ws-war/servicepoint/reworkActivity"
B4_Resolve = ""
B5_Complete = "https://oso.orion.comcast.com/frontend-services-ws-war/servicepoint/updateActivityStatus"


# Bearer token for authentication


bearer_token = 'PFVFTT5LPTxrZXk+LnN5c3RlbS5lbnYuZW5jcnlwdGlvbi4wO0M9MTczNzA5MzA0ODAzMTtNPVh9Mm5JeXsweTZ0RldlZjVxVWZMe2Z5UGFQZ1poOEtqVGZLOG90TWVXVmxHQjFUWVl1MjlheHpONHBvQVlNYUUwOzwvVUVNPg=='  
# Replace with your actual bearer toke

# Headers including the Authorization header
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Content-Type': 'application/json'
}
 
# Function to execute the API call


#3_Rework
 
# Loop through each combination of plan ID and activity ID
# print(len(activity_ids))
 



def F3_Rework (plan_id, activity_id):
    url = f"{B3_Rework}/{plan_id}/{activity_id}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Successfully executed API for Plan ID: {plan_id}, Activity ID: {activity_id},{project_id}")
        elif response.status_code == 403:
            print(f"Forbidden: You don't have permission to access this resource for Plan ID: {plan_id}, Activity ID: {activity_id}. Status Code: {response.status_code}")
        else:
            print(f"Failed to execute API for Plan ID: {plan_id}, Activity ID: {activity_id}. Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
		
# Function call for each set of activity id and plan id		
for i in range(0,len(activity_ids)):
        F3_Rework(plan_ids[i], activity_ids[i])



#5_Complete
 
# Loop through each combination of plan ID and activity ID
# print(len(activity_ids))
 
for i in range(0,len(activity_ids)):
        F5_Complete(plan_ids[i], activity_ids[i],project_ids[i])

		
def F5_Complete(plan_id, activity_id,project_id):
    a1="Completed"
    url = f"{B5_Complete}/{project_id}/{plan_id}/{activity_id}/{a1}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Successfully executed API for Plan ID: {plan_id}, Activity ID: {activity_id},{project_id}")
        elif response.status_code == 403:
            print(f"Forbidden: You don't have permission to access this resource for Plan ID: {plan_id}, Activity ID: {activity_id}. Status Code: {response.status_code}")
        else:
            print(f"Failed to execute API for Plan ID: {plan_id}, Activity ID: {activity_id}. Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
		

	
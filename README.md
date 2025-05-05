# SCALE API Helper (LLM)

This project was created to teach myself the SCALE API.
I hope this serves useful to someone else in the near future.
- Recent: On 05/05/2025 I Added the MCP Funcations, use both 03_mcp*.py files, have fun in OWI or Claude Desktop!!!!!

I've included scripts 01-02, the full API schema as `scale_api_full_schema.json`, and api_schema.db to show how I set this up and how it works.

Keep in mind that this is basic RAG so it is definitely no where near perfect. I'll work on this more in the future!

## How To use this project (as-is)
1. Git Clone this project.
2. Install the requirements via `requirements.txt`
3. Make sure you have ollama installed & running, then make sure you have `mistral:7b` downloaded as well. 

  Other models probably will work fine for this, but I have found this model to be the most consistent.

3. open two separate terminal windows, or a split terminal, even `screen` works for this.
4. in one window run: `python 03_flaskapi.py`
5. in the other window run: `python 03_llmRAG.py`
6. Have fun!


## Example output
Question Example 0, Straight Path: 
``` 
Ask a question about the API: /User
```
Answer:
```
mistral:7b's Response:
  Based on the API schema you provided, I can identify the following actions related to the "User" resource:

1. `POST /User` -- Creates a new user by sending a request with required details (such as username, email, password, etc.) inside the request body.
2. `GET /User` -- Retrieves a list of all users available in the system.
3. `GET /User/{uuid}` -- Retrieves information about a specific user, identified by a unique UUID (Universally Unique Identifier).
4. Both `POST /User/{uuid}` and `PATCH /User/{uuid}` are intended to edit/update user information. However, they differ in the manner they modify the data:
   - `POST /User/{uuid}` -- Creates a new user with an updated UUID, replacing any existing user with the same UUID.
   - `PATCH /User/{uuid}` -- Updates the existing record for that specific user identified by the provided UUID without replacing it.
5. `DELETE /User/{uuid}` -- Deletes a specific user identified by the provided UUID from the system.
```

Question Example 1, Straight Path 2:
```
Ask a question about the API: /virDomain
```
Answer:
```
mistral:7b's Response:
 1. To get a list of VMs, you can use GET method at either `/VirDomain` or `/VirDomain/{virDomainUUID}` endpoint if you have a specific UUID.
2. Create a new VM requires POST request to `/VirDomain`
3. Editing a VM can be done in three ways:
   - Using PUT method at `/VirDomain/{virDomainUUID}` (you might need to update the whole VM information)
   - Using PATCH method at `/VirDomain/{virDomainUUID}` (you can update specific fields)
4. To delete a VM, use DELETE method at `/VirDomain/{virDomainUUID}` endpoint.
5. Creating a new _VirDomainBlockDevice_ requires POST request to `/VirDomainBlockDevice` or `/VirDomainBlockDevice/{uuid}` if you have a specific UUID for editing the existing one.
6. Editing an existing _VirDomainBlockDevice_ can be done in three ways:
   - Using PUT method at `/VirDomainBlockDevice/{uuid}` (you might need to update the whole _VirDomainBlockDevice_ information)
   - Using PATCH method at `/VirDomainBlockDevice/{uuid}` (you can update specific fields)
7. Deleting an existing _VirDomainBlockDevice_ requires DELETE request to `/VirDomainBlockDevice/{uuid}` endpoint.
8. Creating and attaching a new virtual network device for the VM needs POST method at `/VirDomainNetDevice/{virDomainUUID}`. Make sure that the VM is shutoff before adding a network device.
9. Retrieve all virtual network devices with GET request to `/VirDomainNetDevice`. Get or edit specific virtual network device by using get(`GET /VirDomainNetDevice/{uuid}`) and editing operations (POST, PATCH, DELETE) by having the UUID. Make sure that the VM is shutoff before modifying a network device or deleting it using `/VirDomainNetDevice/{uuid}` endpoint.
10. Creating and initiating a VM Replication to a remote system can be done using POST method at `/VirDomainReplication`. You can edit an existing replication by having the UUID, and available editing operations are POST, PATCH, and DELETE as before. Check the documentation for specific parameters or formats related to this API for more details.
11. Capturing a persistent copy of a VM state requires using POST method at `/VirDomainSnapshot`. To get a list of VM snapshots use GET request to `/VirDomainSnapshot` or check a specific snapshot by having the UUID and using GET at `/VirDomainSnapshot/{uuid}`. Delete a snapshot with DELETE method at `/VirDomainSnapshot/{uuid}` endpoint.
12. Create an automated VM Snapshot Schedule and edit/manage it by using POST, PATCH, DELETE methods on respective endpoints:
   - `POST /VirDomainSnapshotSchedule` to create a schedule
   - `GET /VirDomainSnapshotSchedule/{uuid}` to get the list of schedules
   - `PATCH /VirDomainSnapshotSchedule/{uuid}` and `DELETE /VirDomainSnapshotSchedule/{uuid}` to edit or remove a snapshot schedule.
13. Retrieve stats for a VM by using GET request at either `/VirDomainStats` (retrieves all info) or `/VirDomainStats/{virDomainUUID}` (retrieves specific VM's stats).
14. You can export, import and clone VMs by using POST operations:
   - Export a VM: POST `/VirDomain/{virDomainUUID}/export`
   - Import a VM: POST `/VirDomain/import`
   - Clone a VM from snapshot: POST `/VirDomain/{virDomainUUID}/clone`
```

import requests
import json
import time
import os
import re

from datetime import datetime

import quantum_lab.resources as res

class quantum_lab():

    def __init__(self,
            resourceId: str,
            volumeName: str
        ):
        self.userID = os.environ["QCC_USER_ID"]
        # self.uploadType = uploadType
        # self.shot = shot
        self.resourceId = resourceId
        # self.filePath = filePath
        self.namespace = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", os.environ["QCC_USER_ID"].split('@')[0])
        print("[NAMESPACE] ", self.namespace)
        self.volumeName = volumeName
        self.volumePath = self.getDirpath(volumeName)
        self.resourceName = res.getResourceName(resourceId)
        self.url = "http://quantum-job-management.qcc.svc.cluster.local:8080"

        if not isinstance(self.volumePath, str):
            raise ValueError(f"[ERROR] Volume {volumeName} not found in home. -> (/home/jovyan)")
        if "ERROR" in self.resourceName:
            raise ValueError(f"[ERROR] resourceID {resourceId} not found. Please check resources's information.")


    def getDirpath(self, dirPath):
        dirList = os.listdir(f"/home/jovyan/")
        for dirName in dirList:
            if dirPath == dirName:
                return f"/home/jovyan/{dirName}"
        return 0


    def error_handler(self, response):
        if response.status_code == 204:
            print(f"Status: {response.status_code}")
            print(f"ErrorMessage: Job not found.")
            return response.text
        print(f"Status: {response.status_code}")
        print(f"ErrorMessage: {response.json()['error']}")
        return {response.json()['error']}


    def createProcess(self,
            uploadType: str, 
            shot: int, 
            fileName: str, 
            timeout = 10
        ):
        ## check file.
        filePath = ""
        fileList = os.listdir(self.volumePath)
        for files in fileList:
            if files == fileName:
                filePath = f"/mnt/{self.namespace}/{self.volumeName}/{fileName}"

        if filePath == "":
            raise ValueError(f"[ERROR] File {fileName} not found.")

        print("[FilePath] ", filePath)
        url_path = f"{self.url}/v1/jobs"

        headers = {
            "Content-Type": "application/json",
            "emailId": self.userID,
        }

        body = json.dumps({
            "resource": {
                "id": self.resourceId,
                "name": self.resourceName
            },
            "type": uploadType.upper(),
            "filePath": filePath,
            "shot": shot,
        })

        response = requests.post(f"{url_path}", headers=headers, data=body) 
        if response.status_code >= 400:
            return self.error_handler(response)
        
        data = response.json()
        
        print("{:<40} {:<10}".format("ID", "Created Status"))
        print("{:<40} {:<10}".format(data["id"], data["status"]))

        jobID = data["id"]

        time_num = 0
        while True:
            time.sleep(1)
            response = requests.get(f"{self.url}/v1/jobs/{jobID}", headers=headers) 
            data = response.json()
            p_status = data["status"]
            print(f"Time: {time_num} / Job Status: {p_status}        ", end='\r')
            if p_status == "Success" or p_status == "Failed":
                break
            time_num += 1

            if time_num > timeout:
                print("TimeOut...")
                break

        
        return jobID

    def create(self, 
            uploadType: str, 
            shot: int, 
            fileName: str, 
        ):
        ## check file.
        filePath = ""
        fileList = os.listdir(self.volumePath)
        for files in fileList:
            if files == fileName:
                filePath = f"/mnt/{self.namespace}/{self.volumeName}/{fileName}"

        if filePath == "":
            raise ValueError(f"[ERROR] File {fileName} not found.")

        print("[FilePath] ", filePath)
        url_path = f"{self.url}/v1/jobs"

        headers = {
            "Content-Type": "application/json",
            "emailId": self.userID,
        }

        body = json.dumps({
            "resource": {
                "id": self.resourceId,
                "name": self.resourceName
            },
            "type": uploadType.upper(),
            "filePath": filePath,
            "shot": shot,
        })

        response = requests.post(f"{url_path}", headers=headers, data=body) 
        if response.status_code >= 400:
            return self.error_handler(response)
        
        data = response.json()
        
        print("{:<40} {:<10}".format("ID", "Created Status"))
        print("{:<40} {:<10}".format(data["id"], data["status"]))
        
        return data["id"]

    def getList(self, limit = 0):
        url_path = f"{self.url}/v1/jobs"

        headers = {
            "Content-Type": "application/json",
            "emailId": self.userID,
        }
        response = requests.get(f"{url_path}",headers=headers)
        
        if response.status_code != 200:
            return self.error_handler(response)
        
        data = response.json()
            # {:<40} {:<15} {:<10} {:<10} {:<10}
        print("{:<40} {:<15} {:<10} {:<5} {:<10} {:<20} {:<30}".format(
            "ID", 
            # "JobID", 
            # "ResourceID", 
            "ResourceName", 
            "Status", 
            "Shot",
            "Type",
            "FilePath", 
            "CreatedAt"
            )
        )
        index = 0
        for ele in data["content"]:
            print("{:<40} {:<15} {:<10} {:<5} {:<10} {:<20} {:<30}".format(
                ele["id"], 
                # ele["jobId"], 
                # ele["resourceId"], 
                ele["resource"]["name"], 
                ele["status"],
                ele["shot"],
                ele["type"],
                ele["filePath"].split('/')[-1],
                str(datetime.fromtimestamp(int(ele["createdAt"]/1000)))
                )
            )
            index += 1 
            if limit != 0 and index > limit:
                break

        return 1

    def getJob(self, id: str):
        url_path = f"{self.url}/v1/jobs/{id}"

        headers = {
            "Content-Type": "application/json",
            "emailId": self.userID,
        }
        response = requests.get(f"{url_path}", headers=headers)
        
        if response.status_code >= 400:
            return self.error_handler(response)

        data = response.json()
        print("{:<40} {:<15} {:<10} {:<5} {:<10} {:<20} {:<30}".format(
            "ID", 
            # "JobID", 
            # "ResourceID", 
            "ResourceName", 
            "Status", 
            "Shot",
            "Type",
            "FilePath", 
            "CreatedAt"
            )
        )
        print("{:<40} {:<15} {:<10} {:<5} {:<10} {:<20} {:<30}".format(
            data["id"], 
            # ele["jobId"], 
            # ele["resourceId"], 
            data["resource"]["name"], 
            data["status"],
            data["shot"],
            data["type"],
            data["filePath"].split('/')[-1],
            str(datetime.fromtimestamp(int(data["createdAt"]/1000)))
            )
        )
        
        return data

    def delete(self, id: str):
        url_path = f"{self.url}/v1/jobs/{id}"

        headers = {
            "Content-Type": "application/json",
            "emailId": self.userID,
        }
        response = requests.delete(f"{url_path}", headers=headers)

        if response.status_code >= 400:
            return self.error_handler(response)

        print(f"Deleted job : {id}")

        return response.text

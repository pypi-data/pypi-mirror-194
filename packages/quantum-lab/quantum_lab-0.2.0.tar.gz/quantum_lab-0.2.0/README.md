quantum_lab

## Requirements
### Python Package
- setuptools: Python 라이브러리 및 확장을 배포하는데 일반적으로 사용되는 익스텐션 라이브러리입니다.
- wheel: wheel은 파이썬의 build package로 일반적인 source distribution보다 더 빠른 설치가 가능하여서 공식적으로 권장되는 포맷이다. 
- twine: pypi에 업로드하기 위한 패키지입니다.

## How To Use
1. File and config info : https://sdt.atlassian.net/wiki/spaces/SVC/pages/2322661469/python+QCC+python+Package
2. Upload package
- 패키지 빌드
```
$ cd notebook-job-py-package
$ python3 setup.py sdist bdist_wheel
```
- 패키지 업로드 - 업로드 시 pypi 계정 정보를 입력해야 합니다.
```
$ python3 -m twine upload dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: sujunelee                                                  
Enter your password: ************
```
3. Run
- Download package.
```
$ pip3 install quantum_lab
```
- Run code
```
from quantum_lab import resources
from quantum_lab import jobs
import json

## Resource 조회
result = resources.getResource()

## Job 객체 생성
q_job = jobs.quantum_lab("minkyu.kim@sdt.inc", 1, "june-w", "hardware qcc")

## Job 생성
q_job.create("pythoncode", 2, "/home/jovyan/june/june-w/test.py")

## Job 전체 조회
result = q_job.getList()

## Job 조회
result = q_job.getJob(279)

## Job 삭제
result = q_job.delete(278)
```
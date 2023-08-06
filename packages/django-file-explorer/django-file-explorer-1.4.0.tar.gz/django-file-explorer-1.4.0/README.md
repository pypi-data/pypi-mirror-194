# Django File Explorer

A django app to explore the host machine directory. 

It will provide following features:

1. Allow user login
2. Allow to set roles for user to delete and download directories.
3. Allow user to upload single file.

## Installation

Following command will help to install the package.

```bash
pip install django-file-explorer
```

## Setup

1. Add the app to **setting.py** file in **INSTALLED_APPS** section.

```python
INSTALLED_APPS = [
    ...
    'explorer.apps.ExplorerConfig',
]
```

2. If logging is required then add the following information to **settings.py** file:

```python
EXPLORER = {
    'log_dir': MEDIA_ROOT / 'logs',
    'log_file': MEDIA_ROOT / 'logs' / 'access.log'
}
```

**log_dir:** This is the path where multiple user log files will be created. Each file contain information about the single user.

**log_file:** Path to a file containing log information.

Following is the example of single log line.

```tex
[25/Feb/2023 12:44:43:PM] GET | 200 | <<username>> | <<action>> | <<volume>> | <<pageNumber>> | <<location>> | <<checkboxIdx>> |
```

2. Migrate the changes

```bash
python manage.py migrate
```

I you are managing DB separate then make following tables in database:

### explorer_action

| Name          | Position | Data type                | Length | Relation | Not NULL? | Type |
| ------------- | -------- | ------------------------ | ------ | -------- | --------- | ---- |
| id            | 1        | bigint                   |        | PK       | true      | None |
| name          | 2        | character varying        | 120    |          | true      | None |
| creation_date | 3        | timestamp with time zone |        |          | true      | None |

Add following **actions** to table:

1. download
2. delete
3. upload

**Note: All PK are auto incremental.**

### explorer_volume

| Name          | Position | Data type                | Length | Relation | Not NULL? | Type |
| ------------- | -------- | ------------------------ | ------ | -------- | --------- | ---- |
| id            | 1        | bigint                   |        | PK       | true      | None |
| name          | 2        | character varying        | 120    |          | true      | None |
| path          | 3        | character varying        | 2048   |          | true      | None |
| active        | 4        | boolean                  |        |          | true      | None |
| creation_date | 5        | timestamp with time zone |        |          | true      | None |

### explorer_userrole

| Name          | Position | Data type                | Length | Relation | Not NULL? | Type |
| ------------- | -------- | ------------------------ | ------ | -------- | --------- | ---- |
| id            | 1        | bigint                   |        | PK       | true      | None |
| creation_date | 2        | timestamp with time zone |        |          | true      | None |
| user_id       | 3        | integer                  |        | FK       | true      | None |
| volume_id     | 4        | bigint                   |        | FK       | true      | None |

Foreign Key Constraints

| Name      | Columns             | Referenced Table |
| --------- | ------------------- | ---------------- |
| user_id   | (user_id) -> (id)   | auth_user        |
| volume_id | (volume_id) -> (id) | explorer_volume  |

### explorer_userrole_actions

| Name        | Position | Data type | Length | Relation | Not NULL? | Type |
| ----------- | -------- | --------- | ------ | -------- | --------- | ---- |
| id          | 1        | bigint    |        | PK       | true      | None |
| userrole_id | 2        | bigint    |        | FK       | true      | None |
| action_id   | 3        | bigint    |        | FK       | true      | None |

Foreign Key Constraints

| Name        | Columns               | Referenced Table  |
| ----------- | --------------------- | ----------------- |
| userrole_id | (userrole_id) -> (id) | explorer_userrole |
| action_id   | (action_id) -> (id)   | explorer_action   |

3. Add URL to **urls.py** file.

```python
from django.urls import include

urlpatterns = [
    ...
    path('explorer/', include('explorer.urls'), name='explorer')
]
```

Add **volumes** to database by specifying its name and path. After that define the user roles for specific volume in **user roles** table.

## Run

Go to explorer url **SERVER:PORT/explorer** and explore the volumes.

## Author

**Tahir Rafique**

# people-analytics-itsm-sdk
[![PyPI Latest Release](https://img.shields.io/pypi/v/people-analytics-itsm-sdk.svg)](https://pypi.org/project/people-analytics-itsm-sdk/)
[![Downloads](https://pepy.tech/badge/people-analytics-itsm-sdk/month)](https://pepy.tech/project/people-analytics-itsm-sdk)

Interact with various ServiceNow functionality within your python application, includes the ability to perform create, read, update, and delete (CRUD) operations on existing tables, insert data into, retrieve information from and submit tickets.
## Installation
```sh
# or PyPI
pip install people-analytics-itsm-sdk
```

# Environment variables
To use people-analytics-itsm-sdk library, you need set four environment variables:
```dotenv
# ---DOTENV EXAMPLE---
ITSM_SERVICENOW_URL=https://service-now.com # base url of you servicenow server
ITSM_SERVICENOW_API_TOKEN= # servicenow auth token
ITSM_SERVICENOW_API_USER= # servicenow user
ITSM_SERVICENOW_API_PASSWORD= # servicenow user password

# you can choose beetwen user and password or api token to authentication
```
We recommended you to create a `.env` file in your project root to set environment variables.
## Coding in Windows OS
On coding in Windows OS, you need set the environment variables before import people-analytics-itsm-sdk library
```python
import os
# set environment variables before import people-analytics-itsm-sdk library
os.environ["ITSM_SERVICENOW_URL"] = "https://your-service-now-base-path.com"
os.environ["ITSM_SERVICENOW_API_TOKEN"] = "Your api token"
os.environ["ITSM_SERVICENOW_API_USER"] = "your.user.email@domain.com"
os.environ["ITSM_SERVICENOW_API_PASSWORD"] = "your password"

from people_analytics_itsm_sdk.sdk import Records
```
# Example Usage

## Get data from servicenow table
To get data from servicenow table, we use ``Records`` class.
```python
from people_analytics_itsm_sdk.sdk import Records


# This code get all records in one servicenow table
table_name = "sys_user" # replace this with table name are you need
records = Records(table=table_name)

table_data = records.all() # all() method return all records

```
## Querying
You can apply filters and select columns in the table using ``Records().query`` method. For example:
```python
from datetime import datetime, timedelta
from people_analytics_itsm_sdk.sdk import Records


table_name = "incident"
records = Records(table=table_name)

# define date interval to filter
start = datetime(1970, 1, 1)
end = datetime.now() - timedelta(days=20)

# query registers of incident with number started with 'INC0123', created between 1970-01-01 and 20 days old.
records.query.field('number').starts_with('INC0123')\
    .AND().field('sys_created_on').between(start, end)\
    .AND().field('sys_updated_on').order_descending()

data = records.all() # return all records of query
```

## Update tables
to create, delete and update records in a servicenow table, you can use ``Manager`` class.
```python
from people_analytics_itsm_sdk.sdk import Manager


table_name = "name of table you need update"
manager = Manager(table=table_name)

# create new register in table example
register_to_create = {
    "field1": "value1",
    "field2": "value2",
}

manager.create(data=register_to_create)

# update register in table example
register_update_sys_id = "id of register you need update"
register_data_to_update = {
    "field1": "value4"
}
manager.update(sys_id=register_update_sys_id, data=register_data_to_update)

# delete register in table example
register_delete_sys_id = "id of register you need delete"
manager.delete(sys_id=register_delete_sys_id)

```

## Submit tickets
To submit tickets, you can use ``ProducerServiceCatalog`` class.
```python
from people_analytics_itsm_sdk.sdk import ProducerServiceCatalog


survey_catalog_id = "id of your ticket survey in servicenow catalog"
variables = {
    "question1": "value1",
    "question2": "value2"
}

producer_catalog = ProducerServiceCatalog()

result = producer_catalog.store(catalog_id=survey_catalog_id, variables=variables)

```
# Query params

### field(field)
Define the field to operate

**parameters**: field – field (str) to operate

### order_descending()
Define a order descending of field

### order_ascending()
Define a order ascending of field

### starts_with(starts_with)
adds new STARTSWITH condition

**parameters**: starts_with – field of correspondence starts with a value provided

### ends_with(ends_with)
adds new ENDSWITH condition

**parameters**: ends_with – field of correspondence ends with a value provided

### contains(contains)
adds new LIKE condition

**parameters**: contains – field of correspondence contains the value provided

### not_contains(not_contains)
adds new NOTLIKE condition

**parameters**: not_contains – field of correspondence not contains the value provided

### is_empty()
adds new ISEMPTY condition

### is_not_empty()
adds new ISNOTEMPTY condition

### equals(data)
adds new IN or EQUALS condition depending on whether a list or string had provided

**parameters**:
data – *string* or *list* of values

**raise**:
QueryTypeError: if the data provided are of an unexpected kind

### not_equals(data)
adds a new NOT IN ou EQUALS condition depending on whether a *list* or *string* had provided

**parameters**:
data – *string* or *list* of values

**raise**:
QueryTypeError: if the data provided are of an unexpected kind

### greater_than(greater_than)
adds a new GREATER THAN condition

**parameters**:
greater_than – object compatible with *string* or *datetime* (naive UTC datetime or tz-aware datetime)

**raise**:
QueryTypeError: if greater_than provided are of an unexpected kind

### less_than(less_than)
adds new LESS THAN condition

**parameters**:
less_than – object compatible with *string* or *datetime* (naive UTC datetime or tz-aware datetime)

**raise**:
QueryTypeError: if less_than provided are of an unexpected kind

### between(start, end)
adds a new BETWEEN condition

**parameters**:
start – object compatible with *integer* or *datetime* (in the user's time zone SNOW)
end – object compatible with *integer* or *datetime* (in the user's time zoneSNOW)

**raise**:
QueryTypeError: if the initial or final arguments are of an invalid type

### AND()
adds a new AND operator

### OR()
adds a new OR operator

### NQ()
adds a new NQ operator (new query)

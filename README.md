# great_expectations_api

## What is it for ?

In order to be able to use the services provided by great_expectations in an environment other than Python, great_expextations_api is a solution that provides a rest API to communicate from any environment with great_expectations.

## How to setup
### 1) Initialize the service

    python3 great_expectations_api.py init

This command will :

 - Install the sub-required packages
 - Install the great_expectations package
 - Launch the initialization of great_expectations
 - Configure the environment

During this initialization, you will have to setup great_expectation.
Follow these steps (this example is for an Postgresql connection) :

 1. Great Expectations will create a new directory -> y
 2. Would you like to configure a Datasource -> y
 3. What data would you like Great Expectations to connect to -> 2
 4. Which database backend are you using -> 2
 5. Give your new Datasource a short name -> 'type the name'
 6. Fill the database informations
 7. Would you like to proceed -> y
 8. Would you like to profile new Expectations for a single data asset within your new Datasource -> y
 9. Which table would you like to use -> choose one randomly, it doesn't matter
 10. Name the new Expectation Suite -> config
 11. Would you like to proceed -> y
 12. Would you like to build Data Docs -> n

### 2) Start the REST API

    python3 great_expectations_api start

You will be asked to fill in:

 - IP : It's the server @IP on the network
 - PORT : It's the server running port

### 3) Delete the service

    python3 great_expectations_api delete

This command will :

 - Delete the great_expectations folder
 - Uninstall the great_expectations package and sub-packages

## How to use it

The url is composed like this:

    http://@IP:PORT/<data_source>/<schema>/<table>/<great_request>

 - **data_source** : It represent the connection to be used in the request. This connection must have been previously created.
 - **schema** : It represent the database schema of the requested table
 - **table** : It represent the requested table
 - **great_request** : It must be composed of two parts :
	 - The great_expectations request, for example `expect_column_to_exist`
	 - The parameter(s), for example `?column=name`

<!--stackedit_data:
eyJoaXN0b3J5IjpbNDYwMjQwODksMTk2NjQwMjg5OSwtMjAxNz
U5NDc1NywzMDM1MTY0MDcsMTQ5ODgyMTU0Ml19
-->
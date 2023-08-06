WAIT_TIME = 1

READY_SESSION_STATUS = "READY"
PROVISIONING_SESSION_STATUS = "PROVISIONING"
NOT_FOUND_SESSION_STATUS = "NOT_FOUND"
FAILED_SESSION_STATUS = "FAILED"
UNHEALTHY_SESSION_STATUS = [NOT_FOUND_SESSION_STATUS, FAILED_SESSION_STATUS]

ERROR_STATEMENT_STATUS = "ERROR"
CANCELLED_STATEMENT_STATUS = "CANCELLED"
AVAILABLE_STATEMENT_STATUS = "AVAILABLE"
FINAL_STATEMENT_STATUS = [ERROR_STATEMENT_STATUS, CANCELLED_STATEMENT_STATUS, AVAILABLE_STATEMENT_STATUS]
SQL_CELL_MAGIC = "%%sql"

CELL_MAGICS = {"%%configure", "%%sql"}

HELP_TEXT = f'''
Available Magic Commands
%help | Return a list of descriptions and input types for all magic commands. 

Configuration Magics
%%configure | Dictionary | A json-formatted dictionary consisting of all configuration parameters for a session. Each parameter can be specified here or through individual magics.
%profile | String | Specify a profile in your aws configuration to use as the credentials provider.
%iam_role | String | Specify an IAM role to execute your session with. | Default from ~/.aws/configure
%region | String | Specify the AWS region in which to initialize a session | Default from ~/.aws/configure
%max_capacity | Float | The number of AWS Glue data processing units (DPUs) that can be allocated.
%number_of_workers | int | The number of workers of a defined worker_type that are allocated when a job runs. worker_type must be set too.
%worker_type | String | Standard, G.1X, or G.2X. number_of_workers must be set too. 
%idle_timeout | Int | The number of minutes of inactivity after which a session will timeout. The default idle timeout value is 2880 minutes.
%endpoint | String | Define a custom glue endpoint url.
%security_config | String | Define a Security Configuration to be used with this session. 
%session_id  | String | Returns the session ID for the running session. If a String is provided, this will be set as the session ID for the next running session.
%session_id_prefix | String | Define a String that will precede all session IDs in the format [session_id_prefix]-[session_id]. If a session ID is not provided, a random UUID will be generated.
%enable_glue_datacatalog | Boolean | Enables you to use the AWS Glue Data Catalog as an Apache Spark Hive metastore. This feature is enabled by default. Pass either true or false to enable or disable datacatalog.
%connections | List | Specify a comma separated list of connections to use in the session.
%additional_python_modules | List | Comma separated list of additional Python modules to include in your cluster (can be from Pypi or S3).
%extra_py_files | List | Comma separated list of additional Python files From S3.
%extra_jars | List | Comma separated list of additional Jars to include in the cluster.
%temp_dir | String | Specifies an Amazon S3 path to a bucket that can be used as a temporary directory for the job.
%job_type | String | Define the job type you are running. By default, this value is "glueetl"
%status | Returns the status of the current Glue session including its duration, configuration and executing user / role.

Session Magics
%new_session | Delete the current session and start a new session.
%disconnect | Disconnect from the current session, if the kernel is currently connected to one.
%reconnect | String| Define an existing session ID to connect to.
%delete_session | Deletes the current session and kills the cluster. User stops being charged.
%list_sessions | Lists all currently running sessions by name and ID.
%reauthenticate | String | Reauthenticate with a new IAM role.
%%sql | String | Run SQL code. All lines after the initial %%sql magic will be passed as part of the SQL code. 
'''

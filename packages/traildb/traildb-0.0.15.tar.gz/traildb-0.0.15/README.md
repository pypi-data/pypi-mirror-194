# Trail

Trail brings more transparency in your ml experimentation.
Start by using mlflow to track experiments and follow the steps below.

# Installation

Install Trail from Pypi via '''pip install traildb'''

# Get started
'''
from traildb import trail_init
'''

# Initialize a trail object

add this line of code in the beginning of the trainingscript.

'''
trail = trail_init(username, password, database_name)
'''

The input paramter "username", "password" and "database_name" will be provided from the team.


# log experiment

Call the log_experiment() method after the mlflow run (not within the run) <br />

<br />
'''
with mlflow.start_run() as run: <br />
  ...your training code... <br />
trail.log_experiment(mlflow.get_run(run_id=run.info.run_id), parent_id:"String", data_meta:{dict})
'''

The input paramters parent_id [String] and data_meta [dict] must be provided in the according type.
If they are non existing please provide empty String ("") or dict ({})
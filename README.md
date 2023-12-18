# UPPAAL-TO-ROS-SIMULATION

**Setting up Azure ML Studio for pump model inference**
1. Go to https://ml.azure.com/home and create an account
2. Create a workspace and enter it
3. Under the *Assets* tab:
   - choose *Model* and upload model.pt
   - choose *Environments* and create an environment based on the conda yaml file
   - Lastly, choose *Endpoints* and create an endpoint using the uploaded model and environement,       choose the appropriate scoring file
5. Enter the endpoint, under the *consume* tab note the API keys and URL to call the endpoint
6. Enter the API and URL into the run.py file
8. Run either the *run_pumpmodel()* or *run_pumpdetection()* for pump model series detection or binary pump detection, respectively (*Note*: pictures needs to be supplied to *run.py*)

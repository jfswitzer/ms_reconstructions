# Metashape Reconstructions on Kubernetes
## Set up storage (only do this once)
Create the persistent storage volume

`kubectl apply -f make_storage.yaml`

Connect to it with an interactive pod

`kubectl create -f interactive.yaml`
`kubectl exec -it int-pod-gpu2 bash`

Then download the metashape source (make sure to get the professional edition) from https://www.agisoft.com/downloads/installer/, and use `kubectl cp <location on your disk> <pod name>:/extvol` to copy it into the persistent storage volume. Also download the python package (under the 'Python 3 Module' header, will be a .whl file) and copy into `/extvol` on the storage volume.

Do the same to copy the images you would like to use for your reconstruction into `/extvol/images` on the persistent volume (you might have to create this folder). 

## Copying files to/from the persistent volume
To copy files between the persistent volume and your machine, the storage volume needs to be mounted to a pod. You can do this via the interactive command above, but for large file transfers (like images) it's easier to use a long-running job.

Use `sleep.yaml` to maintain connection to storage:

`kubectl apply -f sleep.yaml`

Get the name of the pod

`kubectl get pods`

Then you can run the copy

`kubectl cp <location on your disk> <pod name>:/extvol`

Once you're done copying, delete your job.

`kubectl delete jobs/<job name>`

## Image reconstruction

Once the storage volume is set up, there are 2 ways to perform image reconstruction:

1. Via an interactive pod (this lets you debug any issues, but might not work for really long running tasks)
Create & connect to the pod

`kubectl create -f interactive.yaml`
`kubectl exec -it int-pod-gpu2 bash`

Set up environment stuff / activate the metashape license (this is my trial key, you might need another one). Your .whl file also might be called something different.

`cd /extvol`
`python3 -m pip install Metashape-1.7.0-cp35.cp36.cp37.cp38-abi3-linux_x86_64.whl`
`sudo dpkg --add-architecture i386`
`sudo apt-get update`
`sudo apt-get install libglu1-mesa`
`cd metashape-pro`

Activate the license

`./metashape.sh --activate TXC3V-LUVCT-E1BLK-U83UR-GP25H`
`export agisoft_LICENSE=/extvol/metashape-pro/metashape_trial.lic //(or whatever license file is)`
`cd ..`

Remove stale git repo & re-clone, run the reconstructions script

`rm -rf ms_reconstructions`
`git clone https://github.com/jfswitzer/ms_reconstructions.git`
`cd ms_reconstructions`
`python3 make_reconstruction.py`

2. Via a job

Create the job, which will automatically run all of the commands from above

`kubectl create -f job.yaml`

To check state of job:

`kubectl describe jobs/msr`
`kubectl logs jobs/msr`

Make sure to delete the job once it has completed

`kubectl delete jobs/msr`

## Results retrieval
Connect with an interactive pod

`kubectl create -f interactive.yaml`
`kubectl exec -it int-pod-gpu2 bash`

Copy results to local machine

`kubectl cp int-pod-gpu2:/extvol/ms_reconstruction/result.psz <local destination folder>`

# rpwr-assignments
Assignments for the course Robot Programming with ROS

Clone the repository, 

```
git clone --recurse-submodules https://github.com/artnie/rpwr-assignments.git
```

## Run as Docker locally

Install the Docker Compose Plugin. Linux can install Compose individually. Windows and Mac get it together with Docker Desktop
* Linux (Docker **Compose Plugin**): https://docs.docker.com/compose/install/linux/#install-using-the-repository
* Windows (Docker Desktop): https://docs.docker.com/desktop/install/windows-install/
* Mac (Docker Desktop): https://docs.docker.com/desktop/install/mac-install/

`cd` into the repository. Then start the JupyterNotebook with

```
docker compose -f binder/docker-compose.yml up
```
For troubleshooting with Windows, refer to https://github.com/IntEL4CoRo/cram_teaching/blob/main/docs/install_wsl.md

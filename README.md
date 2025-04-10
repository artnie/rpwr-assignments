# rpwr-assignments
Assignments for the course Robot Programming with ROS

## Build locally

Install the Docker Compose Plugin. Linux can install Compose individually. Windows and Mac get it together with Docker Desktop
* Linux (Docker **Compose Plugin**): https://docs.docker.com/compose/install/linux/#install-using-the-repository
* Windows (Docker Desktop): https://docs.docker.com/desktop/install/windows-install/
* Mac (Docker Desktop): https://docs.docker.com/desktop/install/mac-install/

Clone the repository, cd into it. Then start the image with 
```
docker compose -f binder/docker-compose.yml up
```
For troubleshooting with Windows, refer to https://github.com/IntEL4CoRo/cram_teaching/blob/main/docs/install_wsl.md

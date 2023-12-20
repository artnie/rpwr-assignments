FROM intel4coro/artnie-2dpycram-324103:ae09d0364ac1d9ea3abda5f1985056701172a8ca

ENV PATH=$PATH:/home/user/.local/bin
ENV PYCRAM_WS=/home/${NB_USER}/workspace/ros
ENV TURTLEBOT3_MODEL=waffle_pi


USER root
RUN apt-get update && \
    apt-get install -y \
    ros-noetic-turtlebot3-msgs \
    ros-noetic-turtlebot3-description \
    ros-noetic-turtlebot3-teleop \
    ros-noetic-turtlebot3-navigation \
    ros-noetic-dwa-local-planner \
    byobu \
    iputils-ping && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
USER ${NB_USER}

WORKDIR ${PYCRAM_WS}/src/
RUN git clone https://github.com/artnie/turtlebot3_simulations -b rpwr \
 && git clone https://github.com/code-iai/iai_office_sim

# Build pycram workspace
WORKDIR  ${PYCRAM_WS}

RUN catkin build

WORKDIR ${PYCRAM_WS}/src/pycram
COPY --chown=${NB_USER}:users . rpwr-assignments/



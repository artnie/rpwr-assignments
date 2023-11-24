FROM intel4coro/artnie-2dpycram-324103:17b77c002b7ebeedda5846477f52d67ef14012a5
WORKDIR ${HOME}
COPY --chown=${NB_USER}:users . rpwr-assignments/

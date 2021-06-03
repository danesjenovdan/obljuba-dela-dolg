#!/bin/bash

sudo docker login rg.fr-par.scw.cloud/djnd -u nologin -p $SCW_SECRET_TOKEN

# BUILD AND PUBLISH OBLJUBA DELA DOLG
sudo docker build -f obljubadeladolg/Dockerfile -t obljubadeladolg:latest .
sudo docker tag obljubadeladolg:latest rg.fr-par.scw.cloud/djnd/obljubadeladolg:latest
sudo docker push rg.fr-par.scw.cloud/djnd/obljubadeladolg:latest

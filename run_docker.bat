@echo off
SET mypath=%~dp0
docker run -p 5001:5001 -it --rm -v %mypath%:/scratch clip_img_search:latest bash -c "(cd /scratch/ && python api.py)"
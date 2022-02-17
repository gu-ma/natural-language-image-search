docker run --network host -it --rm -v `pwd`:/scratch --user $(id -u):$(id -g) clip_img_search:latest bash -c \
    "(cd /scratch/ && python api.py)"
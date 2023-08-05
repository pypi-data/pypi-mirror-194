# if v1-5-pruned.ckpt does not exist, download it
if [ ! -f v1-5-pruned.ckpt ]; then
    curl -L https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt --output $(pwd)/v1-5-pruned.ckpt
fi

# if nvidia-smi exists then run docker with gpus

if docker ps -a | grep rb-control; then
    docker stop rb-control
    docker rm rb-control
fi

if command -v nvidia-smi &> /dev/null
then
    docker run --name rb-control --gpus all -it -d -v $(pwd)/v1-5-pruned.ckpt:/home/engineering/ControlNet/models/v1-5-pruned.ckpt -v $1:/home/engineering/ControlNet/training/fill50k -d rubbrband/control:latest 
else
    docker run --name rb-control -it -d -v $(pwd)/v1-5-pruned.ckpt:/home/engineering/ControlNet/models/v1-5-pruned.ckpt -v $1:/home/engineering/ControlNet/training/fill50k -d rubbrband/control:latest 
fi

docker exec -it rb-control /bin/bash -c " \
    conda run -n control python tool_add_control.py ./models/v1-5-pruned.ckpt ./models/control_sd15_ini.ckpt && \
    conda run -n control python tutorial_train.py"
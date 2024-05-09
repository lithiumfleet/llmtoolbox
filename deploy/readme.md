usage:

1. use launch script in vllm_infer_scripts which receives some args:
    + -m: path to model
    + -l: path to lora, if --uselora is not set, -l will be ignored.
    + -uselora: enable use lora
    + -gpu: a comma list to devices. e.g -gpu 1,2,3,4
    + -p: port. set this to 9870-9879

2. use node launch forwarding server: node forwarding_server/app.js

3. use cpolar to expose 9880 (i have had a server on 9880 :-)

4. fresh the server: get http://localhost:9880/v1/models to fresh the forwarding rules

WARNING: only /v1/models and /v1/chat/completion can be correctly redirect now...

e.g (plz cd to correct dir)
1. ./launch -m /data/lixubin/models/Qwen/Qwen1.5-72B-Chat-GPTQ-Int4 -p 9874 -gpu  1,3
2. node app.js

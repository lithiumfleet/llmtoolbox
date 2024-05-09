这里是一个使用express搭建的转发服务器.

```mermaid
flowchart LR
    subgraph vllm_server
        model1
        model2
        model3
    end
    subgraph forwarding_server
        listen
    end
    vllm_server-->forwarding_server
```

9880上的forwarding server会监听从9870-9879的所有openai服务器.
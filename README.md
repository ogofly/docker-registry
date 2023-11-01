# docker registry

使用官方 [registry](https://distribution.github.io/distribution/)，增加了几个常见配置

- nginx 认证：内部使用、公开使用
- image 清除(clean.py) ，结合以下脚本清除已删除的 image blob 文件

```bash
docker exec -ti reg bin/registry garbage-collect /etc/docker/registry/config.yml -m
```

#构建部分
# docker build -t test_v3:v1 -f tcs.build/Dockerfile.lb_yunapi_v3_proj.amd64 ~/lb_code/lb_yunapi_v3_proj

# 基础镜像
FROM csighub.tencentyun.com/zhhdzhang/tencentos4-nginx-py3.12-base:latest

# ssh弱口令修复（临时方案）
RUN PASSWORD=$(dd bs=1 count=12 if=/dev/urandom | md5sum | cut -d' ' -f1) && echo "root:$PASSWORD" | chpasswd -c SHA512

# 拷贝lb_chore_proj代码到运行目录，安装依赖
ARG code_path=/usr/local/services/lb_chore-1.0
COPY ./ ${code_path}
WORKDIR ${code_path}
RUN make install

# 拷贝nginx.conf
COPY ./etc/nginx.conf /etc/nginx/nginx.conf

#控制脚本
COPY ./tcs.build/build/entrypoint.sh /usr/bin
COPY ./tcs.build/build/healthchk.sh /usr/bin/
RUN chmod u+x /usr/bin/entrypoint.sh
RUN chmod u+x /usr/bin/healthchk.sh
ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]

EXPOSE 80


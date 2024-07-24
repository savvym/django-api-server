# 基础镜像
FROM csighub.tencentyun.com/zhhdzhang/tencentos4-nginx-py3.12-base:latest

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


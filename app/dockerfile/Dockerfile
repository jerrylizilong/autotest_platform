FROM jerry-sample-flask
LABEL author="jerry"
RUN echo "start"
USER root
RUN echo "using user root"
WORKDIR /opt/app-root/src
RUN echo "enter worksdir"
RUN pwd
COPY runall.sh /opt/app-root/src/runall.sh
RUN chmod +x /opt/app-root/src/runall.sh
RUN echo "chmod" && ls
ENTRYPOINT ["/opt/app-root/src/runall.sh"]

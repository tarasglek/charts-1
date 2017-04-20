# docker build -t queue:latest .
# docker run -e QUEUE_CONFIG=postgres://postgres:taras@fs66-b-app/postgres -it --rm queue
# docker tag queue:latest tarasglek/queue && docker push tarasglek/queue
FROM node:alpine
USER  node
WORKDIR /home/node
COPY package.json /home/node
RUN yarn install
COPY master.js rest.js /home/node/
EXPOSE 8080
CMD [ "yarn", "start" ]
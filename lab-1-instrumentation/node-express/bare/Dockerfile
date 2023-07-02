# Build app
FROM node:14
COPY ./index.js .
COPY ./package.json .
RUN npm install

# Run app
ENTRYPOINT [ "node", "index.js" ]
EXPOSE 4321

# build stage
FROM node:13.10.1-stretch as build_stage

WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:1.19.6-alpine as production_stage

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY --from=build_stage /app/dist /usr/share/nginx/html/

CMD ["nginx-debug", "-g", "daemon off;"]

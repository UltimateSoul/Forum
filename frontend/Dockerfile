# build stage
FROM node:13.10.1-stretch as build_stage

WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx as production_stage
EXPOSE 3000
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build_stage /app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]

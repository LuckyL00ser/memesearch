FROM node:20 AS frontend-builder

WORKDIR /frontend-app

COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM nginx:1.27.0
COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=frontend-builder /frontend-app/build /usr/share/nginx/html

EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
# Stage 1: Build Vite app
FROM node:20-alpine as build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . ./
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:stable-alpine as production

# Copy build output (Vite outputs to dist by default)
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

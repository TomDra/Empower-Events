FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install package*.json
CMD ["npm", "start"]
EXPOSE 3000
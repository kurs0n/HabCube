FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npx", "expo", "start", "--web", "--non-interactive", "--port", "3000"]

FROM node:18-alpine
WORKDIR /app

# Paketleri kopyala ve yükle
COPY package*.json ./
RUN npm install

# Uygulamayı kopyala
COPY . .

# Dev sunucusunu host üzerinden erişilebilir kıl
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

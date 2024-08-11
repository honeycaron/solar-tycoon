FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

#$ docker build -t ${도커 이미지명}:${도커 이미지 버전} .
#$ docker run -p ${실행할 포트 번호}:3000 ${도커 이미지명}:${도커 이미지 버전}
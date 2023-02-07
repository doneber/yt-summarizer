FROM node:16.3.0-alpine AS ui-build
WORKDIR /usr/src/app
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build

FROM node:16.3.0-alpine AS server-build
WORKDIR /root/
COPY --from=ui-build /usr/src/app/frontend/dist ./frontend/dist
COPY backend/package*.json ./backend/
RUN cd backend && npm install
COPY backend/app.js ./backend/

EXPOSE 80

CMD ["node", "./backend/app.js"]
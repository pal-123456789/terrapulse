FROM node:18-alpine

WORKDIR /app

# Copy package files first
COPY package.json .
COPY package-lock.json .

# Install dependencies and fix rollup issue
RUN npm ci && \
    npm rebuild @rollup/rollup-linux-x64-musl

# Copy application code
COPY . .

# Build the application
RUN npm run build

EXPOSE 5173
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:5173/ || exit 1
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]
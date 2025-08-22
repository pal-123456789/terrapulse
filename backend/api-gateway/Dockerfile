FROM golang:1.25-alpine

WORKDIR /app

# Install dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN go build -o api-gateway .

# Expose port
EXPOSE 8080

# Run the application
CMD ["./api-gateway"]
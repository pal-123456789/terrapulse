FROM golang:1.25-alpine

WORKDIR /app

# Copy dependency tracking files
COPY go.mod go.sum ./

# Install dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN go build -o notification-service .

# Expose port
EXPOSE 8082

# Run the application
CMD ["./notification-service"]
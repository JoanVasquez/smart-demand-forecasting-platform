FROM maven:3.9.9-eclipse-temurin-21 AS builder

# Set work directory
WORKDIR /app

# Copy pom.xml first to cache dependencies
COPY ./services/sale-service/pom.xml .

COPY ./shared /shared

# Download dependencies (better cache for faster builds)
RUN mvn dependency:go-offline -B

# Copy the source code
COPY ./services/sale-service/src ./src

# Build the application (skip tests for faster container build)
RUN mvn clean package -DskipTests


FROM eclipse-temurin:21-jre-jammy AS runtime

# Set work directory
WORKDIR /app

# Copy only the jar from the build stage
COPY --from=builder /app/target/*.jar app.jar

# Use non-root user for security
RUN useradd -m appuser
USER appuser

# Expose the application port
EXPOSE 8080

# Add JVM optimization for containers
ENTRYPOINT ["java", \
    "-XX:+UseContainerSupport", \
    "-XX:MaxRAMPercentage=75.0", \
    "-XX:InitialRAMPercentage=50.0", \
    "-XX:+ExitOnOutOfMemoryError", \
    "-jar", "app.jar"]

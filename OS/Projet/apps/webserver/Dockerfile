FROM maven:latest as builder
ADD ./pom.xml pom.xml
ADD ./src src/
RUN mvn clean package

FROM openjdk:17-oracle
COPY --from=builder target/ManageLdap-0.0.1-SNAPSHOT.jar ManageLdap.jar

CMD ["java", "-jar", "ManageLdap.jar"]

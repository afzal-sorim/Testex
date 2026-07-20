# Repository: E-commerce-project-springBoot

## Overview
This is a Spring Boot application for an E-commerce project. It includes a frontend (possibly React/Node or embedded) and backend.

## File Structure
```
E-commerce-project-springBoot/
    .gitignore
    basedata.sql
    jenkins file
    mvnw
    mvnw.cmd
    package.json
    playwright.config.ts
    pom.xml
    README.md
    roadmap.md
    .idea/
        E-commerce-project-springBoot1.iml
    src/
        main/
            java/
                com/
                    jtspringproject/
                        JtSpringProject/
                            HibernateConfiguration.java
                            JtSpringProjectApplication.java
                            configuration/
                                PasswordEncoderConfig.java
                                SecurityConfiguration.java
                            controller/
                                AdminController.java
                                ErrorController.java
                                UserController.java
                            dao/
                                cartDao.java
                                cartProductDao.java
                                categoryDao.java
                                productDao.java
                                userDao.java
                            models/
                                Cart.java
                                CartProduct.java
                                CartProductId.java
                                Category.java
                                Product.java
                                User.java
                            services/
                                cartService.java
                                categoryService.java
                                productService.java
                                userService.java
            resources/
                application.properties
                Product Images/
                    one.jpg
            webapp/
                views/
                    403.jsp
                    adminHome.jsp
                    adminlogin.jsp
                    cartproduct.jsp
                    categories.jsp
                    displayCustomers.jsp
                    index.jsp
                    products.jsp
                    productsAdd.jsp
                    productsUpdate.jsp
                    register.jsp
                    updateProfile.jsp
                    uproduct.jsp
                    userLogin.jsp
        test/
            java/
                com/
                    jtspringproject/
                        JtSpringProject/
                            JtSpringProjectApplicationTests.java
                            models/
                                CartProductIdTest.java
                                CartProductTest.java
    tests/
        e2e/
            01-navigation.spec.ts
            04-ui-components.spec.ts
```

## Dependencies (pom.xml)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.6.4</version>
		<relativePath /> <!-- lookup parent from repository -->
	</parent>
	<groupId>com.jtspringproject</groupId>
	<artifactId>JtSpringProject</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<name>JtSpringProject</name>
	<description>Spring project for Java Technology</description>
	<properties>
		<java.version>11</java.version>
	</properties>
	<dependencies>


		<dependency>
			<groupId>org.junit.jupiter</groupId>
			<artifactId>junit-jupiter</artifactId>
			<version>5.10.0</version>
			<scope>test</scope>
		</dependency>


		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>


		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<scope>test</scope>
		</dependency>

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-devtools</artifactId>
		</dependency>

		<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>jstl</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-data-jpa</artifactId>
		</dependency>

		<dependency>
			<groupId>org.apache.tomcat.embed</groupId>
			<artifactId>tomcat-embed-jasper</artifactId>
		</dependency>


		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<version>8.0.33</version>
		</dependency>
		
		<dependency>
    		<groupId>org.springframework.boot</groupId>
   			<artifactId>spring-boot-starter-security</artifactId>
		</dependency>

	    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>
</dependencies>

	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
			</plugin>
		</plugins>
	</build>

</project>
...
```


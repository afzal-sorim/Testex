import re

with open("python_backend/app/services/analysis_service.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update _calculate_risk_level
new_risk_logic = """    def _calculate_risk_level(self, current_version: int, deprecated_apis: list, project_info: dict) -> tuple:
        score = 0
        reasons = []
        if current_version <= 8:
            score += 3
            reasons.append(f"Legacy Java {current_version} environment requires modernization")
        elif current_version <= 11:
            score += 2
            reasons.append(f"Outdated Java {current_version} environment")
        elif current_version <= 16:
            score += 1
            reasons.append(f"Non-LTS Java {current_version} environment")
            
        if deprecated_apis:
            score += min(len(deprecated_apis), 3)
            reasons.append(f"Presence of {len(deprecated_apis)} deprecated API usages requiring remediation")
            
        if project_info.get("is_multi_module"):
            score += 1
            reasons.append("Multi-module architectural complexity")
            
        if project_info.get("database") not in ("None", "H2 (Embedded)", None):
            score += 1
            reasons.append(f"External database dependency ({project_info.get('database')})")
            
        if project_info.get("packaging_type") == "war":
            score += 1
            reasons.append("Legacy WAR packaging relying on external application servers")

        reason_str = "; ".join(reasons) if reasons else "Modern technology stack with no major risks identified."
        
        percentage = min(100, int((score / 10.0) * 100))
        if score == 0:
            percentage = 5

        if score >= 6:
            return f"High ({percentage}%)", reason_str
        elif score >= 3:
            return f"Medium ({percentage}%)", reason_str
        return f"Low ({percentage}%)", reason_str"""

content = re.sub(r'    def _calculate_risk_level\(self.*?return "Low", reason_str', new_risk_logic, content, flags=re.DOTALL)

# 2. Update professional reasons in set_detail calls
replacements = [
    ('"Maven", "Found pom.xml"', '"Maven", "Standard Maven build configuration identified"'),
    ('"Gradle", "Found build.gradle"', '"Gradle", "Standard Gradle build configuration identified"'),
    ('"Gradle Kotlin DSL", "Found build.gradle.kts"', '"Gradle Kotlin DSL", "Kotlin-based Gradle build configuration identified"'),
    ('"Spring Boot / Thymeleaf", "Detected spring-boot and thymeleaf dependencies"', '"Spring Boot / Thymeleaf", "Spring Boot framework with Thymeleaf templating engine detected"'),
    ('"Spring Boot / JSP", "Detected spring-boot and JSP/Jasper dependencies"', '"Spring Boot / JSP", "Spring Boot framework with legacy JSP templating detected"'),
    ('"Spring Boot / Web MVC", "Detected spring-boot-starter-web dependency"', '"Spring Boot / Web MVC", "Spring Boot Web MVC architecture detected via starter dependencies"'),
    ('"Spring Boot / WebFlux (Reactive)", "Detected spring-boot-starter-webflux dependency"', '"Spring Boot / WebFlux (Reactive)", "Reactive Spring WebFlux architecture detected"'),
    ('"Spring Boot / Data Only", "Detected spring-boot-starter-data dependency"', '"Spring Boot / Data Only", "Data-centric Spring Boot application detected without web starters"'),
    ('"Spring Boot", "Detected spring-boot dependency"', '"Spring Boot", "Core Spring Boot framework dependencies detected"'),
    ('"Spring MVC (Non-Boot)", "Detected spring-webmvc without Spring Boot"', '"Spring MVC (Non-Boot)", "Traditional Spring MVC framework detected without Spring Boot auto-configuration"'),
    ('"JSP/Servlet", "Detected servlet-api dependency"', '"JSP/Servlet", "Legacy Java Servlet/JSP web architecture detected"'),
    ('"JavaFX", "Detected javafx dependency"', '"JavaFX", "Desktop JavaFX application framework detected"'),
    ('"MySQL", "Detected mysql-connector dependency"', '"MySQL", "MySQL database driver connector identified in dependencies"'),
    ('"PostgreSQL", "Detected postgresql dependency"', '"PostgreSQL", "PostgreSQL database driver identified in dependencies"'),
    ('"SQL Server", "Detected mssql dependency"', '"SQL Server", "Microsoft SQL Server driver identified in dependencies"'),
    ('"Oracle", "Detected oracle jdbc dependency"', '"Oracle", "Oracle JDBC driver identified in dependencies"'),
    ('"MongoDB", "Detected mongodb dependency"', '"MongoDB", "MongoDB NoSQL driver identified in dependencies"'),
    ('"H2 (Embedded)", "Detected h2database dependency"', '"H2 (Embedded)", "H2 embedded in-memory database identified"'),
    ('"war", "Explicit war packaging specified in build file"', '"war", "Legacy Web Application Archive (WAR) packaging explicitly configured"'),
    ('"jar", "Default jar packaging (no war specified)"', '"jar", "Standard Java Archive (JAR) deployment packaging identified"'),
    ('True, "Detected module subprojects structure"', 'True, "Multi-module project architecture with explicit sub-projects defined"'),
    ('False, "No submodules detected"', 'False, "Standard monolithic project structure without sub-modules"'),
]

for old, new in replacements:
    content = content.replace(old, new)

# 3. Fix java reason
content = content.replace('java_reason = f"Explicitly defined in build configuration (v{current_java_version})"', 'java_reason = f"Java version {current_java_version} explicitly declared in compiler configuration"')
content = content.replace('java_reason = f"Inferred from project structure/defaults (v{current_java_version})"', 'java_reason = f"Default Java version {current_java_version} inferred from project characteristics"')

with open("python_backend/app/services/analysis_service.py", "w", encoding="utf-8") as f:
    f.write(content)
print("analysis_service patched!")

/**
 * Mock API responses matching the backend models.
 * Used by apiMocks.ts to intercept network requests in tests.
 */

export const MOCK_ANALYSIS_SUCCESS = {
  repoUrl: 'https://github.com/spring-projects/spring-petclinic',
  projectType: 'Java',
  isJava: true,
  detectedJavaVersion: '8',
  buildTool: 'Maven',
  frameworkType: 'Spring Boot 2.7.18',
  frameworkVersions: { 'Spring Boot': '2.7.18' },
  database: 'MySQL',
  packagingType: 'jar',
  isMultiModule: false,
  hasFrontend: true,
  frontendFramework: 'Thymeleaf',
  endpointCount: 12,
  riskLevel: 'Medium',
  dependencies: [
    'spring-boot-starter-web',
    'spring-boot-starter-data-jpa',
    'spring-boot-starter-thymeleaf',
    'mysql-connector-java',
    'spring-boot-starter-test',
  ],
  deprecatedApis: [
    'javax.persistence → jakarta.persistence',
    'javax.servlet → jakarta.servlet',
  ],
  migrationRecommendation: 'Upgrade from Java 8 to Java 21 LTS for virtual threads and improved performance.',
  reasoning: 'This project uses Spring Boot 2.7.18 with Java 8. Upgrading to Java 21 will provide access to virtual threads, pattern matching, sealed classes, and records. The migration path involves updating the Java version, upgrading Spring Boot to 3.x, and migrating javax to jakarta namespace.',
  usedProvider: 'gemini',
};

export const MOCK_ANALYSIS_NON_JAVA = {
  repoUrl: 'https://github.com/pallets/flask',
  projectType: 'Unknown',
  isJava: false,
  detectedJavaVersion: null,
  buildTool: 'Not Detected',
  frameworkType: null,
  frameworkVersions: {},
  database: 'None',
  packagingType: null,
  isMultiModule: false,
  hasFrontend: false,
  frontendFramework: null,
  endpointCount: 0,
  riskLevel: 'Low',
  dependencies: [],
  deprecatedApis: [],
  migrationRecommendation: 'This repository does not appear to be a Java project. Migration is not applicable.',
  reasoning: 'The repository does not contain any Java source files, pom.xml, or build.gradle.',
};

export const MOCK_MIGRATION_TASK_RESPONSE = {
  task_id: 'mock-task-12345',
};

export const MOCK_MIGRATION_STATUS_PENDING = {
  status: 'PENDING',
  result: null,
  error: null,
};

export const MOCK_MIGRATION_STATUS_SUCCESS = {
  status: 'SUCCESS',
  result: {
    success: true,
    targetVersion: '21',
    buildStatus: 'Build Success',
    modifiedFiles: [
      'pom.xml',
      'src/main/java/org/springframework/samples/petclinic/PetClinicApplication.java',
      'src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java',
      'src/main/java/org/springframework/samples/petclinic/vet/VetController.java',
    ],
    migrationSummary: '✅ Migration Summary:\n- Java version upgraded: 8 → 21\n- Spring Boot upgraded: 2.7.18 → 3.2.0\n- javax.* → jakarta.* namespace migration\n- Updated 4 files\n- Build: SUCCESS\n- Tests: ALL PASSED',
    gitDiff: 'diff --git a/pom.xml b/pom.xml\n--- a/pom.xml\n+++ b/pom.xml\n@@ -5,7 +5,7 @@\n   <properties>\n-    <java.version>8</java.version>\n+    <java.version>21</java.version>\n   </properties>',
    buildErrors: null,
    suggestedFixes: null,
    fixHistory: null,
  },
  error: null,
};

export const MOCK_MIGRATION_STATUS_BUILD_FAILURE = {
  status: 'SUCCESS',
  result: {
    success: false,
    targetVersion: '21',
    buildStatus: 'Build Failure',
    modifiedFiles: ['pom.xml'],
    migrationSummary: '❌ Migration completed but build failed.',
    gitDiff: null,
    buildErrors: 'ERROR: Compilation failure\n[ERROR] /src/main/java/Example.java:[15,10] cannot find symbol\n  symbol:   class javax.servlet.http.HttpServletRequest',
    suggestedFixes: 'Replace javax.servlet imports with jakarta.servlet equivalents.',
    fixHistory: null,
  },
  error: null,
};

export const MOCK_MIGRATION_STATUS_FAILURE = {
  status: 'FAILURE',
  result: null,
  error: 'Migration task failed: Unable to clone repository.',
};

export const MOCK_RUN_START_RESPONSE = {
  status: 'STARTING',
  port: 8080,
  projectType: 'spring-boot',
};

export const MOCK_RUN_STATUS_STOPPED = {
  status: 'STOPPED',
  port: 8080,
  projectType: 'spring-boot',
  previewUrl: null,
  endpoints: [],
  errorReason: null,
  noUiMessage: null,
  swaggerUrl: null,
};

export const MOCK_RUN_STATUS_RUNNING = {
  status: 'RUNNING',
  port: 8080,
  projectType: 'spring-boot',
  previewUrl: 'http://localhost:8080',
  endpoints: [
    { method: 'GET', path: '/owners', file: 'OwnerController.java' },
    { method: 'GET', path: '/vets', file: 'VetController.java' },
    { method: 'POST', path: '/owners/new', file: 'OwnerController.java' },
  ],
  errorReason: null,
  noUiMessage: null,
  swaggerUrl: null,
};

export const MOCK_ERROR_RESPONSES = {
  privateRepo: {
    errorMessage: 'Authentication required. This repository is private. Please provide valid credentials.',
  },
  notFound: {
    errorMessage: 'Repository not found. Please verify the URL and ensure the repository exists.',
  },
  serverError: {
    message: 'Internal server error. The analysis service is currently unavailable.',
  },
};

export const MOCK_LAST_MIGRATION_LOCALSTORAGE = {
  success: true,
  targetVersion: '21',
  buildStatus: 'Build Success',
  modifiedFiles: ['pom.xml', 'src/main/java/App.java'],
  migrationSummary: 'Migration completed successfully. 2 files modified.',
  buildErrors: null,
  suggestedFixes: null,
};

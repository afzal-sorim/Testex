/**
 * Shared test fixture data used across all Playwright functional tests.
 */

export const VALID_REPO_URLS = {
  springPetclinic: 'https://github.com/spring-projects/spring-petclinic',
  springBoot: 'https://github.com/spring-projects/spring-boot',
  guava: 'https://github.com/google/guava',
} as const;

export const INVALID_URLS = {
  plainText: 'not-a-url',
  missingProtocol: 'github.com/user/repo',
  emptyString: '',
} as const;

export const SIDEBAR_TABS = {
  dashboard: 'Dashboard',
  analysis: 'Repository Analysis',
  migration: 'Migration Center',
  explorer: 'Repository Explorer',
  conversion: 'Code Conversion',
  migrationReport: 'Migration Report',
  conversionReport: 'Conversion Report',
  apiKeys: 'API Keys',
} as const;

export const JAVA_VERSIONS = ['11', '17', '21', '25'] as const;

export const DEFAULT_TARGET_VERSION = '21';

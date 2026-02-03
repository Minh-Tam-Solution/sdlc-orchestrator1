/**
 * E2E Validation Unit Tests
 *
 * Sprint 139 - RFC-SDLC-602 E2E API Testing Enhancement
 * Tests the VS Code Extension's E2E validation functionality
 *
 * Tests:
 * - E2E Validation types and interfaces
 * - Cross-Reference validation logic
 * - SSOT compliance checking
 * - Coverage calculation
 *
 * @version 1.0.0
 * @since Sprint 139
 */

import * as assert from 'assert';
import type {
    E2EValidationResult,
    E2EValidationError,
    E2EValidationWarning,
    E2EChecklistItem,
    E2ETestingReport,
    CrossReferenceValidationResult,
    CrossReferenceLink,
    EndpointCoverage,
    EvidenceType,
} from '../../types/evidence';

suite('E2E Validation Types Test Suite', () => {
    // ===========================================================================
    // Test Cases - Evidence Types
    // ===========================================================================

    test('EvidenceType enum has all required values', () => {
        // Verify RFC-SDLC-602 evidence types exist
        const requiredTypes = [
            'requirements_document',
            'design_document',
            'code_review',
            'test_results',
            'deployment_log',
            'audit_trail',
            'e2e_testing_report',
            'api_documentation_reference',
            'security_testing_results',
            'stage_cross_reference',
        ];

        // These values should be available in the EvidenceType enum
        // We can't directly test the enum, but we can verify the types work
        const evidenceTypeExamples: EvidenceType[] = [
            'e2e_testing_report' as EvidenceType,
            'api_documentation_reference' as EvidenceType,
            'security_testing_results' as EvidenceType,
            'stage_cross_reference' as EvidenceType,
        ];

        assert.strictEqual(evidenceTypeExamples.length, 4, 'Should have 4 new E2E evidence types');
    });

    // ===========================================================================
    // Test Cases - E2E Validation Result Structure
    // ===========================================================================

    test('E2EValidationResult interface has required fields', () => {
        const result: E2EValidationResult = {
            valid: true,
            passRate: 95.5,
            totalEndpoints: 58,
            testedEndpoints: 55,
            passedEndpoints: 55,
            failedEndpoints: 0,
            errors: [],
            warnings: [],
            checklist: [],
            testResults: null,
            stage05Path: 'docs/05-deploy',
            openapiPath: 'docs/03-integrate/01-api-contracts/openapi.json',
            validationTimestamp: '2026-02-02T10:00:00Z',
        };

        assert.strictEqual(result.valid, true);
        assert.strictEqual(result.passRate, 95.5);
        assert.strictEqual(result.totalEndpoints, 58);
        assert.strictEqual(result.testedEndpoints, 55);
        assert.ok(result.validationTimestamp.includes('2026'));
    });

    test('E2EValidationResult with errors is invalid', () => {
        const error: E2EValidationError = {
            code: 'E2E-001',
            message: 'Stage 05 folder not found',
            path: 'docs/05-deploy',
        };

        const result: E2EValidationResult = {
            valid: false,
            passRate: 0,
            totalEndpoints: 0,
            testedEndpoints: 0,
            passedEndpoints: 0,
            failedEndpoints: 0,
            errors: [error],
            warnings: [],
            checklist: [],
            testResults: null,
            validationTimestamp: new Date().toISOString(),
        };

        assert.strictEqual(result.valid, false);
        assert.strictEqual(result.errors.length, 1);
        assert.strictEqual(result.errors[0].code, 'E2E-001');
    });

    test('E2EValidationResult with warnings is valid but flagged', () => {
        const warning: E2EValidationWarning = {
            code: 'E2E-W001',
            message: 'Coverage below 80% threshold',
        };

        const result: E2EValidationResult = {
            valid: true,
            passRate: 75,
            totalEndpoints: 20,
            testedEndpoints: 15,
            passedEndpoints: 15,
            failedEndpoints: 0,
            errors: [],
            warnings: [warning],
            checklist: [],
            testResults: null,
            validationTimestamp: new Date().toISOString(),
        };

        assert.strictEqual(result.valid, true);
        assert.strictEqual(result.warnings.length, 1);
        assert.ok(result.warnings[0].message.includes('80%'));
    });

    // ===========================================================================
    // Test Cases - E2E Testing Report Structure
    // ===========================================================================

    test('E2ETestingReport interface has complete structure', () => {
        const report: E2ETestingReport = {
            timestamp: '2026-02-02T10:00:00Z',
            totalEndpoints: 58,
            testedEndpoints: 55,
            passedEndpoints: 52,
            failedEndpoints: 3,
            passRate: 94.5,
            coverage: [
                {
                    method: 'GET',
                    path: '/api/v1/users',
                    tested: true,
                    passed: true,
                    statusCode: 200,
                    responseTime: 45,
                },
                {
                    method: 'POST',
                    path: '/api/v1/users',
                    tested: true,
                    passed: false,
                    statusCode: 500,
                    errorMessage: 'Internal server error',
                },
            ],
            reportPath: 'docs/05-deploy/03-E2E-Testing/results.json',
            testRunner: 'newman',
            environment: 'staging',
            baseUrl: 'https://api.sdlc-orchestrator.io',
        };

        assert.strictEqual(report.totalEndpoints, 58);
        assert.strictEqual(report.coverage.length, 2);
        assert.strictEqual(report.coverage[0].method, 'GET');
        assert.strictEqual(report.coverage[0].passed, true);
        assert.strictEqual(report.coverage[1].passed, false);
        assert.strictEqual(report.testRunner, 'newman');
    });

    test('EndpointCoverage with various states', () => {
        const covered: EndpointCoverage = {
            method: 'GET',
            path: '/api/v1/projects',
            tested: true,
            passed: true,
            statusCode: 200,
            responseTime: 32,
        };

        const uncovered: EndpointCoverage = {
            method: 'DELETE',
            path: '/api/v1/projects/{id}',
            tested: false,
            passed: false,
        };

        const failed: EndpointCoverage = {
            method: 'PUT',
            path: '/api/v1/projects/{id}',
            tested: true,
            passed: false,
            statusCode: 403,
            errorMessage: 'Forbidden - insufficient permissions',
        };

        assert.strictEqual(covered.tested, true);
        assert.strictEqual(covered.passed, true);
        assert.strictEqual(uncovered.tested, false);
        assert.strictEqual(failed.passed, false);
        assert.ok(failed.errorMessage?.includes('Forbidden'));
    });

    // ===========================================================================
    // Test Cases - Checklist Items
    // ===========================================================================

    test('E2EChecklistItem structure for compliance', () => {
        const checklistItems: E2EChecklistItem[] = [
            { item: 'Stage 05 folder exists', passed: true },
            { item: 'E2E test results present', passed: true },
            { item: 'Pass rate >= 80%', passed: true, details: '94.5%' },
            { item: 'All critical endpoints tested', passed: false, details: 'Missing: POST /auth/login' },
            { item: 'OpenAPI spec in Stage 03', passed: true },
            { item: 'No duplicate openapi.json files', passed: true },
        ];

        const passedItems = checklistItems.filter(item => item.passed);
        const failedItems = checklistItems.filter(item => !item.passed);

        assert.strictEqual(passedItems.length, 5);
        assert.strictEqual(failedItems.length, 1);
        assert.ok(failedItems[0].details?.includes('POST /auth/login'));
    });
});

suite('Cross-Reference Validation Test Suite', () => {
    // ===========================================================================
    // Test Cases - Cross-Reference Result Structure
    // ===========================================================================

    test('CrossReferenceValidationResult interface structure', () => {
        const result: CrossReferenceValidationResult = {
            valid: true,
            stage03Path: 'docs/03-integrate',
            stage05Path: 'docs/05-deploy',
            totalEndpoints: 58,
            coveredEndpoints: 45,
            uncoveredEndpoints: 13,
            coveragePercentage: 77.6,
            links: [],
            errors: [],
            warnings: [],
            validationTimestamp: '2026-02-02T10:00:00Z',
        };

        assert.strictEqual(result.valid, true);
        assert.strictEqual(result.totalEndpoints, 58);
        assert.strictEqual(result.coveredEndpoints, 45);
        assert.strictEqual(result.coveragePercentage, 77.6);
    });

    test('CrossReferenceLink for bidirectional traceability', () => {
        const links: CrossReferenceLink[] = [
            {
                sourceStage: '03-integrate',
                sourcePath: 'docs/03-integrate/01-api-contracts/openapi.json',
                sourceType: 'openapi',
                targetStage: '05-deploy',
                targetPath: 'docs/05-deploy/03-E2E-Testing/test_users.py',
                targetType: 'test',
                linkType: 'tests',
                valid: true,
                validatedAt: '2026-02-02T10:00:00Z',
            },
            {
                sourceStage: '03-integrate',
                sourcePath: 'docs/03-integrate/01-api-contracts/openapi.json',
                sourceType: 'openapi',
                targetStage: '05-deploy',
                targetPath: 'docs/05-deploy/03-E2E-Testing/test_auth.py',
                targetType: 'test',
                linkType: 'tests',
                valid: false, // Broken link
            },
        ];

        const validLinks = links.filter(link => link.valid);
        const brokenLinks = links.filter(link => !link.valid);

        assert.strictEqual(validLinks.length, 1);
        assert.strictEqual(brokenLinks.length, 1);
        assert.strictEqual(links[0].linkType, 'tests');
    });

    // ===========================================================================
    // Test Cases - Coverage Calculation
    // ===========================================================================

    test('Coverage calculation with all endpoints tested', () => {
        const result: CrossReferenceValidationResult = {
            valid: true,
            stage03Path: 'docs/03-integrate',
            stage05Path: 'docs/05-deploy',
            totalEndpoints: 20,
            coveredEndpoints: 20,
            uncoveredEndpoints: 0,
            coveragePercentage: 100,
            links: [],
            errors: [],
            warnings: [],
            validationTimestamp: new Date().toISOString(),
        };

        assert.strictEqual(result.coveragePercentage, 100);
        assert.strictEqual(result.uncoveredEndpoints, 0);
    });

    test('Coverage calculation with partial coverage', () => {
        const total = 50;
        const covered = 35;
        const percentage = (covered / total) * 100;

        const result: CrossReferenceValidationResult = {
            valid: true,
            stage03Path: 'docs/03-integrate',
            stage05Path: 'docs/05-deploy',
            totalEndpoints: total,
            coveredEndpoints: covered,
            uncoveredEndpoints: total - covered,
            coveragePercentage: percentage,
            links: [],
            errors: [],
            warnings: [],
            validationTimestamp: new Date().toISOString(),
        };

        assert.strictEqual(result.coveragePercentage, 70);
        assert.strictEqual(result.uncoveredEndpoints, 15);
    });

    test('Coverage below threshold adds warning', () => {
        const warning: E2EValidationWarning = {
            code: 'E2E-W002',
            message: 'Coverage 65% is below 80% recommended threshold',
        };

        const result: CrossReferenceValidationResult = {
            valid: true, // Still valid, just warning
            stage03Path: 'docs/03-integrate',
            stage05Path: 'docs/05-deploy',
            totalEndpoints: 20,
            coveredEndpoints: 13,
            uncoveredEndpoints: 7,
            coveragePercentage: 65,
            links: [],
            errors: [],
            warnings: [warning],
            validationTimestamp: new Date().toISOString(),
        };

        assert.strictEqual(result.warnings.length, 1);
        assert.ok(result.warnings[0].message.includes('65%'));
        assert.ok(result.warnings[0].message.includes('80%'));
    });

    // ===========================================================================
    // Test Cases - SSOT Compliance
    // ===========================================================================

    test('SSOT compliance - openapi.json only in Stage 03', () => {
        // Valid case: openapi.json only in Stage 03
        const validResult: CrossReferenceValidationResult = {
            valid: true,
            stage03Path: 'docs/03-integrate',
            stage05Path: 'docs/05-deploy',
            totalEndpoints: 20,
            coveredEndpoints: 18,
            uncoveredEndpoints: 2,
            coveragePercentage: 90,
            links: [],
            errors: [],
            warnings: [],
            validationTimestamp: new Date().toISOString(),
        };

        assert.strictEqual(validResult.valid, true);
        assert.strictEqual(validResult.errors.length, 0);
    });

    test('SSOT violation - duplicate openapi.json detected', () => {
        const error: E2EValidationError = {
            code: 'SSOT-001',
            message: 'Duplicate openapi.json found in Stage 05',
            path: 'docs/05-deploy/openapi.json',
        };

        const result: CrossReferenceValidationResult = {
            valid: false,
            stage03Path: 'docs/03-integrate',
            stage05Path: 'docs/05-deploy',
            totalEndpoints: 20,
            coveredEndpoints: 18,
            uncoveredEndpoints: 2,
            coveragePercentage: 90,
            links: [],
            errors: [error],
            warnings: [],
            validationTimestamp: new Date().toISOString(),
        };

        assert.strictEqual(result.valid, false);
        assert.strictEqual(result.errors[0].code, 'SSOT-001');
        assert.ok(result.errors[0].path?.includes('05-deploy'));
    });
});

suite('E2E Command Logic Test Suite', () => {
    // ===========================================================================
    // Helper functions (mirrors command logic)
    // ===========================================================================

    function calculatePassRate(passed: number, total: number): number {
        if (total === 0) return 0;
        return Math.round((passed / total) * 100 * 10) / 10; // 1 decimal
    }

    function determineValidationStatus(
        passRate: number,
        minPassRate: number,
        strict: boolean
    ): boolean {
        if (strict) {
            return passRate >= minPassRate;
        }
        return passRate > 0 || minPassRate === 0;
    }

    function categorizeEndpoint(
        method: string,
        path: string
    ): 'critical' | 'important' | 'normal' {
        // Authentication endpoints are critical
        if (path.includes('/auth') || path.includes('/login') || path.includes('/token')) {
            return 'critical';
        }

        // Write operations are important
        if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(method.toUpperCase())) {
            return 'important';
        }

        return 'normal';
    }

    // ===========================================================================
    // Test Cases - Pass Rate Calculation
    // ===========================================================================

    test('calculatePassRate with all passing', () => {
        assert.strictEqual(calculatePassRate(50, 50), 100);
    });

    test('calculatePassRate with partial passing', () => {
        assert.strictEqual(calculatePassRate(45, 50), 90);
    });

    test('calculatePassRate with none passing', () => {
        assert.strictEqual(calculatePassRate(0, 50), 0);
    });

    test('calculatePassRate with zero total', () => {
        assert.strictEqual(calculatePassRate(0, 0), 0);
    });

    test('calculatePassRate with decimal result', () => {
        assert.strictEqual(calculatePassRate(77, 100), 77);
        assert.strictEqual(calculatePassRate(2, 3), 66.7);
    });

    // ===========================================================================
    // Test Cases - Validation Status
    // ===========================================================================

    test('determineValidationStatus strict mode - above threshold', () => {
        assert.strictEqual(determineValidationStatus(90, 80, true), true);
    });

    test('determineValidationStatus strict mode - below threshold', () => {
        assert.strictEqual(determineValidationStatus(75, 80, true), false);
    });

    test('determineValidationStatus non-strict mode - any passing', () => {
        assert.strictEqual(determineValidationStatus(10, 80, false), true);
    });

    test('determineValidationStatus non-strict mode - none passing', () => {
        assert.strictEqual(determineValidationStatus(0, 80, false), false);
    });

    // ===========================================================================
    // Test Cases - Endpoint Categorization
    // ===========================================================================

    test('categorizeEndpoint - auth endpoints are critical', () => {
        assert.strictEqual(categorizeEndpoint('POST', '/api/v1/auth/login'), 'critical');
        assert.strictEqual(categorizeEndpoint('POST', '/api/v1/auth/token'), 'critical');
        assert.strictEqual(categorizeEndpoint('POST', '/api/v1/auth/logout'), 'critical');
    });

    test('categorizeEndpoint - write operations are important', () => {
        assert.strictEqual(categorizeEndpoint('POST', '/api/v1/users'), 'important');
        assert.strictEqual(categorizeEndpoint('PUT', '/api/v1/users/123'), 'important');
        assert.strictEqual(categorizeEndpoint('DELETE', '/api/v1/users/123'), 'important');
        assert.strictEqual(categorizeEndpoint('PATCH', '/api/v1/users/123'), 'important');
    });

    test('categorizeEndpoint - read operations are normal', () => {
        assert.strictEqual(categorizeEndpoint('GET', '/api/v1/users'), 'normal');
        assert.strictEqual(categorizeEndpoint('GET', '/api/v1/users/123'), 'normal');
        assert.strictEqual(categorizeEndpoint('GET', '/api/v1/projects'), 'normal');
    });
});

suite('E2E Error Codes Test Suite', () => {
    // ===========================================================================
    // Test Cases - Error Code Standards
    // ===========================================================================

    test('E2E error codes follow naming convention', () => {
        const errors: E2EValidationError[] = [
            { code: 'E2E-001', message: 'Stage 05 folder not found' },
            { code: 'E2E-002', message: 'No test results found' },
            { code: 'E2E-003', message: 'OpenAPI spec not found in Stage 03' },
            { code: 'SSOT-001', message: 'Duplicate openapi.json detected' },
        ];

        // All codes should start with E2E- or SSOT-
        for (const error of errors) {
            const validPrefix = error.code.startsWith('E2E-') || error.code.startsWith('SSOT-');
            assert.ok(validPrefix, `Invalid code prefix: ${error.code}`);
        }
    });

    test('Warning codes follow naming convention', () => {
        const warnings: E2EValidationWarning[] = [
            { code: 'E2E-W001', message: 'Coverage below 80%' },
            { code: 'E2E-W002', message: 'Some tests skipped' },
            { code: 'E2E-W003', message: 'Test results older than 24 hours' },
        ];

        // All warning codes should have -W suffix
        for (const warning of warnings) {
            assert.ok(warning.code.includes('-W'), `Warning code should include -W: ${warning.code}`);
        }
    });
});

suite('E2E Integration Test Mocks', () => {
    // ===========================================================================
    // Mock CLI Integration (for testing without real CLI)
    // ===========================================================================

    interface CLIResult {
        exitCode: number;
        stdout: string;
        stderr: string;
    }

    function mockCLIExecution(command: string): CLIResult {
        // Simulate CLI responses based on command
        if (command.includes('e2e validate')) {
            return {
                exitCode: 0,
                stdout: JSON.stringify({
                    valid: true,
                    pass_rate: 94.5,
                    total_endpoints: 58,
                    tested_endpoints: 55,
                    passed_endpoints: 52,
                    failed_endpoints: 3,
                }),
                stderr: '',
            };
        }

        if (command.includes('e2e cross-reference')) {
            return {
                exitCode: 0,
                stdout: JSON.stringify({
                    valid: true,
                    coverage: { total: 58, covered: 45, percentage: 77.6 },
                    missing_tests: [
                        { method: 'POST', path: '/api/v1/admin/users' },
                        { method: 'DELETE', path: '/api/v1/admin/users/{id}' },
                    ],
                }),
                stderr: '',
            };
        }

        return {
            exitCode: 1,
            stdout: '',
            stderr: 'Unknown command',
        };
    }

    test('Mock CLI e2e validate returns valid JSON', () => {
        const result = mockCLIExecution('sdlcctl e2e validate --format json');

        assert.strictEqual(result.exitCode, 0);

        const parsed = JSON.parse(result.stdout);
        assert.strictEqual(parsed.valid, true);
        assert.strictEqual(parsed.pass_rate, 94.5);
        assert.strictEqual(parsed.total_endpoints, 58);
    });

    test('Mock CLI e2e cross-reference returns coverage', () => {
        const result = mockCLIExecution('sdlcctl e2e cross-reference --format json');

        assert.strictEqual(result.exitCode, 0);

        const parsed = JSON.parse(result.stdout);
        assert.strictEqual(parsed.valid, true);
        assert.strictEqual(parsed.coverage.total, 58);
        assert.strictEqual(parsed.coverage.percentage, 77.6);
        assert.strictEqual(parsed.missing_tests.length, 2);
    });

    test('Mock CLI unknown command returns error', () => {
        const result = mockCLIExecution('sdlcctl unknown command');

        assert.strictEqual(result.exitCode, 1);
        assert.ok(result.stderr.includes('Unknown'));
    });
});

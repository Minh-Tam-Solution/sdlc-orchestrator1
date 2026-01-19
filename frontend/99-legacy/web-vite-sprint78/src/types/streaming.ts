/**
 * File: frontend/web/src/types/streaming.ts
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 51A
 * Date: 2025-12-25
 * Authority: Frontend Lead + CTO Approved
 * Foundation: Progressive Code Generation Flow Plan
 *
 * Description:
 * SSE (Server-Sent Events) type definitions for streaming code generation.
 * Used by CodeGenerationPage to handle real-time file generation events.
 */

/**
 * All possible SSE event types from the backend
 */
export type StreamEventType =
  | 'started'
  | 'file_generating'
  | 'file_generated'
  | 'quality_started'
  | 'quality_gate'
  | 'completed'
  | 'error'

/**
 * Base interface for all stream events
 */
export interface StreamEvent {
  type: StreamEventType
  timestamp: string
  session_id: string
}

/**
 * Event: Generation started
 * Sent when code generation begins
 */
export interface StartedEvent extends StreamEvent {
  type: 'started'
  model: string
  provider: string
}

/**
 * Event: File is being generated
 * Sent when a new file starts generating
 */
export interface FileGeneratingEvent extends StreamEvent {
  type: 'file_generating'
  path: string
}

/**
 * Event: File generation complete
 * Sent when a file is fully generated with content
 */
export interface FileGeneratedEvent extends StreamEvent {
  type: 'file_generated'
  path: string
  content: string
  lines: number
  language: string
  syntax_valid?: boolean
}

/**
 * Event: Quality pipeline started
 * Sent when quality gates begin running
 */
export interface QualityStartedEvent extends StreamEvent {
  type: 'quality_started'
}

/**
 * Event: Quality gate result
 * Sent for each gate completion
 */
export interface QualityGateEvent extends StreamEvent {
  type: 'quality_gate'
  gate_number: number
  gate_name: string
  status: 'passed' | 'failed' | 'skipped'
  issues: number
  duration_ms: number
}

/**
 * Event: Generation completed
 * Sent when all files are generated
 */
export interface CompletedEvent extends StreamEvent {
  type: 'completed'
  total_files: number
  total_lines: number
  duration_ms: number
  success: boolean
}

/**
 * Event: Error occurred
 * Sent when an error occurs during generation
 */
export interface ErrorEvent extends StreamEvent {
  type: 'error'
  message: string
  recovery_id?: string
}

/**
 * Union type for all stream events
 */
export type CodegenStreamEvent =
  | StartedEvent
  | FileGeneratingEvent
  | FileGeneratedEvent
  | QualityStartedEvent
  | QualityGateEvent
  | CompletedEvent
  | ErrorEvent

/**
 * Streaming file state for UI display
 */
export interface StreamingFile {
  path: string
  content: string
  lines: number
  language: string
  status: 'generating' | 'valid' | 'error'
}

/**
 * Parse SSE event data from server
 */
export function parseStreamEvent(data: string): CodegenStreamEvent | null {
  try {
    return JSON.parse(data) as CodegenStreamEvent
  } catch {
    console.error('Failed to parse stream event:', data)
    return null
  }
}

/**
 * Detect language from file extension
 */
export function detectLanguage(path: string): string {
  const ext = path.split('.').pop()?.toLowerCase() || ''
  const langMap: Record<string, string> = {
    'py': 'python',
    'ts': 'typescript',
    'tsx': 'typescript',
    'js': 'javascript',
    'jsx': 'javascript',
    'json': 'json',
    'yaml': 'yaml',
    'yml': 'yaml',
    'md': 'markdown',
    'sql': 'sql',
    'html': 'html',
    'css': 'css',
    'sh': 'bash',
    'txt': 'text',
    'toml': 'toml',
    'ini': 'ini',
    'cfg': 'ini',
  }
  return langMap[ext] || ext
}

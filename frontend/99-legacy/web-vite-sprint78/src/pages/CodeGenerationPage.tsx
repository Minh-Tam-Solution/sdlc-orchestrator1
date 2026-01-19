/**
 * File: frontend/web/src/pages/CodeGenerationPage.tsx
 * Version: 1.1.0
 * Status: ACTIVE - Sprint 51A
 * Date: December 25, 2025
 * Authority: Frontend Lead + CTO Approved
 * Foundation: EP-06 Code Generation Page (Code-Generation-Page-Specification.md)
 *
 * Description:
 * Code Generation Page - Phase 2 of EP-06 flow.
 * Receives AppBlueprint from onboarding and triggers code generation.
 * Displays generation progress and allows downloading generated code.
 *
 * Sprint 51A Changes:
 * - Added SSE streaming support via EventSource
 * - Real-time file generation display
 * - Fallback to POST endpoint if SSE fails
 * - Progressive quality gate display
 */

import { useState, useCallback, useRef, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { ArrowLeft, Play, Download, RefreshCw, CheckCircle2, XCircle, Clock, AlertTriangle } from 'lucide-react'

import DashboardLayout from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Separator } from '@/components/ui/separator'
import { BlueprintJsonViewer } from '@/components/codegen/BlueprintJsonViewer'
import { useToast } from '@/hooks/useToast'
import apiClient, { getErrorMessage } from '@/api/client'
import {
  parseStreamEvent,
  type CodegenStreamEvent,
  type StreamingFile,
} from '@/types/streaming'

// Generation status types
type GenerationStatus = 'idle' | 'validating' | 'generating' | 'quality_check' | 'completed' | 'failed'

interface GenerationProgress {
  status: GenerationStatus
  current_step: string
  total_steps: number
  completed_steps: number
  current_gate?: string
  errors: string[]
  warnings: string[]
}

// Quality Gate types (matches backend QualityPipelineResult)
interface QualityGateIssue {
  file: string
  line?: number
  column?: number
  severity: string
  code: string
  message: string
  suggestion?: string
}

interface QualityGateResult {
  gate_name: string
  gate_number: number
  status: 'pending' | 'running' | 'passed' | 'failed' | 'skipped'
  duration_ms: number
  error_count: number
  warning_count: number
  summary: string
  issues: QualityGateIssue[]
}

interface QualityPipelineResult {
  success: boolean
  total_duration_ms: number
  failed_gate?: number
  summary: string
  gates: QualityGateResult[]
}

// Backend response format for /generate/full endpoint
interface BackendGenerateFullResponse {
  success: boolean
  provider: string
  files: Record<string, string>
  file_count: number
  total_lines: number
  tokens_used: number
  generation_time_ms: number
  quality: QualityPipelineResult
  metadata: Record<string, unknown>
}

interface GeneratedCode {
  files: GeneratedFile[]
  total_files: number
  total_lines: number
  provider: string
  tokens_used: number
  generation_time_ms: number
  quality?: QualityPipelineResult
}

interface GeneratedFile {
  path: string
  language: string
  lines: number
  content: string
}

// Helper to detect language from file extension
function detectLanguage(path: string): string {
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
  }
  return langMap[ext] || ext
}

// Transform backend response to frontend format
function transformResponse(data: BackendGenerateFullResponse): GeneratedCode {
  const files: GeneratedFile[] = Object.entries(data.files).map(([path, content]) => ({
    path,
    content,
    language: detectLanguage(path),
    lines: content.split('\n').length,
  }))

  return {
    files,
    total_files: data.file_count,
    total_lines: data.total_lines,
    provider: data.provider,
    tokens_used: data.tokens_used,
    generation_time_ms: data.generation_time_ms,
    quality: data.quality,
  }
}

// Vietnamese status labels
const STATUS_LABELS: Record<GenerationStatus, string> = {
  idle: 'Sẵn sàng',
  validating: 'Đang kiểm tra Blueprint...',
  generating: 'Đang tạo code...',
  quality_check: 'Kiểm tra chất lượng...',
  completed: 'Hoàn tất',
  failed: 'Thất bại',
}

// Status badge variants
const STATUS_VARIANTS: Record<GenerationStatus, 'default' | 'secondary' | 'destructive' | 'outline'> = {
  idle: 'outline',
  validating: 'secondary',
  generating: 'secondary',
  quality_check: 'secondary',
  completed: 'default',
  failed: 'destructive',
}

// Status icons
function StatusIcon({ status }: { status: GenerationStatus }) {
  switch (status) {
    case 'completed':
      return <CheckCircle2 className="h-5 w-5 text-green-500" />
    case 'failed':
      return <XCircle className="h-5 w-5 text-destructive" />
    case 'validating':
    case 'generating':
    case 'quality_check':
      return <RefreshCw className="h-5 w-5 animate-spin text-primary" />
    default:
      return <Clock className="h-5 w-5 text-muted-foreground" />
  }
}

export default function CodeGenerationPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const { toast } = useToast()

  // Get blueprint from navigation state
  const blueprint = location.state?.blueprint as Record<string, unknown> | null
  const stats = location.state?.stats as Record<string, unknown> | null

  // Generation state
  const [progress, setProgress] = useState<GenerationProgress>({
    status: 'idle',
    current_step: '',
    total_steps: 4,
    completed_steps: 0,
    errors: [],
    warnings: [],
  })
  const [generatedCode, setGeneratedCode] = useState<GeneratedCode | null>(null)

  // Sprint 51A: Streaming state
  const [streamingFiles, setStreamingFiles] = useState<StreamingFile[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const eventSourceRef = useRef<EventSource | null>(null)

  // Cleanup EventSource on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close()
      }
    }
  }, [])

  // Note: We don't auto-redirect here - show UI message instead
  // This prevents blank page issues on production

  // Sprint 51A: Start streaming generation via SSE
  const startStreamingGeneration = useCallback(() => {
    if (!blueprint) return

    // Reset state
    setStreamingFiles([])
    setProgress({
      status: 'generating',
      current_step: 'Connecting to server...',
      total_steps: 4,
      completed_steps: 0,
      errors: [],
      warnings: [],
    })
    setGeneratedCode(null)
    setIsStreaming(true)

    // Build SSE URL with blueprint as query param
    const baseUrl = (import.meta.env['VITE_API_URL'] as string | undefined) || ''
    const token = localStorage.getItem('access_token') || ''

    // Note: EventSource doesn't support POST body, so we need to use a different approach
    // For Sprint 51A, we'll use fetch with streaming for POST requests
    const startStream = async () => {
      try {
        const response = await fetch(`${baseUrl}/api/v1/codegen/generate/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            'Accept': 'text/event-stream',
          },
          body: JSON.stringify({
            app_blueprint: blueprint,
            language: 'python',
            framework: 'fastapi',
          }),
        })

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }

        const reader = response.body?.getReader()
        if (!reader) {
          throw new Error('No response body')
        }

        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })

          // Parse SSE events from buffer
          const lines = buffer.split('\n')
          buffer = lines.pop() || '' // Keep incomplete line in buffer

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6)
              const event = parseStreamEvent(data)
              if (event) {
                handleStreamEvent(event)
              }
            }
          }
        }
      } catch (error) {
        console.error('Streaming failed, falling back to POST:', error)
        // Fallback to POST endpoint
        fallbackToPost()
      }
    }

    startStream()
  }, [blueprint])

  // Handle individual stream events
  const handleStreamEvent = useCallback((event: CodegenStreamEvent) => {
    switch (event.type) {
      case 'started':
        setProgress(prev => ({
          ...prev,
          status: 'generating',
          current_step: `Using ${event.model} (${event.provider})`,
        }))
        break

      case 'file_generating':
        setStreamingFiles(prev => [...prev, {
          path: event.path,
          content: '',
          lines: 0,
          language: detectLanguage(event.path),
          status: 'generating',
        }])
        setProgress(prev => ({
          ...prev,
          current_step: `Generating ${event.path}...`,
        }))
        break

      case 'file_generated':
        setStreamingFiles(prev => prev.map(f =>
          f.path === event.path
            ? {
                path: event.path,
                content: event.content,
                lines: event.lines,
                language: event.language,
                status: event.syntax_valid ? 'valid' : 'error',
              }
            : f
        ))
        break

      case 'quality_started':
        setProgress(prev => ({
          ...prev,
          status: 'quality_check',
          current_step: 'Running quality gates...',
        }))
        break

      case 'quality_gate':
        setProgress(prev => ({
          ...prev,
          current_gate: `${event.gate_name}: ${event.status}`,
          completed_steps: event.gate_number,
        }))
        break

      case 'completed':
        setIsStreaming(false)
        // Convert streaming files to GeneratedCode format
        setGeneratedCode({
          files: streamingFiles.map(f => ({
            path: f.path,
            content: f.content,
            lines: f.lines,
            language: f.language,
          })),
          total_files: event.total_files,
          total_lines: event.total_lines,
          provider: 'ollama',
          tokens_used: 0,
          generation_time_ms: event.duration_ms,
        })
        setProgress(prev => ({
          ...prev,
          status: event.success ? 'completed' : 'failed',
          current_step: event.success ? 'Code generation completed' : 'Generation completed with issues',
          completed_steps: 4,
        }))
        toast({
          title: event.success ? 'Tạo code thành công!' : 'Code đã tạo xong',
          description: `${event.total_files} files, ${event.total_lines.toLocaleString()} dòng code trong ${(event.duration_ms / 1000).toFixed(1)}s`,
          variant: event.success ? 'success' : 'warning',
        })
        break

      case 'error':
        setIsStreaming(false)
        setProgress(prev => ({
          ...prev,
          status: 'failed',
          current_step: 'Generation failed',
          errors: [...prev.errors, event.message],
        }))
        toast({
          title: 'Lỗi tạo code',
          description: event.message,
          variant: 'error',
        })
        break
    }
  }, [streamingFiles, toast])

  // Fallback to POST endpoint if SSE fails
  const fallbackToPost = useCallback(async () => {
    setProgress(prev => ({
      ...prev,
      current_step: 'Streaming unavailable, using standard generation...',
    }))

    try {
      const response = await apiClient.post('/codegen/generate/full', {
        app_blueprint: blueprint,
        language: 'python',
        framework: 'fastapi',
      }, {
        timeout: 120000,
      })

      const transformed = transformResponse(response.data as BackendGenerateFullResponse)
      setGeneratedCode(transformed)

      const qualityPassed = transformed.quality?.success ?? true
      setProgress(prev => ({
        ...prev,
        status: qualityPassed ? 'completed' : 'failed',
        current_step: qualityPassed ? 'Code generation completed' : 'Quality check failed',
        completed_steps: 4,
      }))

      toast({
        title: qualityPassed ? 'Tạo code thành công!' : 'Code đã tạo nhưng có lỗi chất lượng',
        description: `${transformed.total_files} files, ${transformed.total_lines.toLocaleString()} dòng code`,
        variant: qualityPassed ? 'success' : 'error',
      })
    } catch (error) {
      setProgress(prev => ({
        ...prev,
        status: 'failed',
        current_step: 'Generation failed',
        errors: [...prev.errors, getErrorMessage(error)],
      }))
      toast({
        title: 'Lỗi tạo code',
        description: getErrorMessage(error),
        variant: 'error',
      })
    } finally {
      setIsStreaming(false)
    }
  }, [blueprint, toast])

  // Code generation mutation - fallback for direct POST
  const generateMutation = useMutation({
    mutationFn: async () => {
      setProgress(prev => ({
        ...prev,
        status: 'generating',
        current_step: 'Đang tạo code từ Blueprint...',
        completed_steps: 0,
      }))

      const response = await apiClient.post('/codegen/generate/full', {
        app_blueprint: blueprint,
        language: 'python',
        framework: 'fastapi',
      }, {
        timeout: 120000,
      })

      return response.data
    },
    onSuccess: (data) => {
      const transformed = transformResponse(data as BackendGenerateFullResponse)
      setGeneratedCode(transformed)

      const qualityPassed = transformed.quality?.success ?? true
      const completedSteps = transformed.quality?.gates.filter(
        g => g.status === 'passed' || g.status === 'skipped'
      ).length ?? 4

      setProgress(prev => ({
        ...prev,
        status: qualityPassed ? 'completed' : 'failed',
        current_step: qualityPassed ? 'Code generation completed' : 'Quality check failed',
        completed_steps: completedSteps,
        current_gate: undefined,
        warnings: transformed.quality?.gates.flatMap(g =>
          g.issues.filter(i => i.severity === 'warning').map(i => `${i.file}: ${i.message}`)
        ) ?? [],
        errors: transformed.quality?.gates.flatMap(g =>
          g.issues.filter(i => i.severity === 'error').map(i => `${i.file}: ${i.message}`)
        ) ?? [],
      }))

      const qualitySummary = transformed.quality?.summary ?? ''
      toast({
        title: qualityPassed ? 'Tạo code thành công!' : 'Code đã tạo nhưng có lỗi chất lượng',
        description: `${transformed.total_files} files, ${transformed.total_lines.toLocaleString()} dòng code (${transformed.provider}). ${qualitySummary}`,
        variant: qualityPassed ? 'success' : 'error',
      })
    },
    onError: (error) => {
      setProgress(prev => ({
        ...prev,
        status: 'failed',
        current_step: 'Generation failed',
        errors: [...prev.errors, getErrorMessage(error)],
      }))

      toast({
        title: 'Lỗi tạo code',
        description: getErrorMessage(error),
        variant: 'error',
      })
    },
  })

  // Handle start generation - Sprint 51A: Try streaming first, fallback to POST
  const handleStartGeneration = useCallback(() => {
    setProgress({
      status: 'idle',
      current_step: '',
      total_steps: 4,
      completed_steps: 0,
      errors: [],
      warnings: [],
    })
    setGeneratedCode(null)
    setStreamingFiles([])

    // Sprint 51A: Use streaming generation
    startStreamingGeneration()
  }, [startStreamingGeneration])

  // Handle download - call /generate/zip endpoint for proper ZIP file
  const handleDownloadZip = useCallback(async () => {
    if (!blueprint) {
      toast({
        title: 'Chưa có Blueprint',
        description: 'Vui lòng tạo Blueprint trước.',
        variant: 'error',
      })
      return
    }

    try {
      toast({
        title: 'Đang tạo file ZIP...',
        description: 'Vui lòng chờ trong giây lát.',
      })

      // Call /generate/zip endpoint
      // Use 120s timeout (code generation takes 30-90s typically)
      const response = await apiClient.post('/codegen/generate/zip', {
        app_blueprint: blueprint,
        language: 'python',
        framework: 'fastapi',
      }, {
        responseType: 'blob',
        timeout: 120000, // 120 seconds
      })

      // Create download link
      const blob = new Blob([response.data], { type: 'application/zip' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url

      // Extract filename from Content-Disposition header or use default
      const contentDisposition = response.headers['content-disposition']
      const filenameMatch = contentDisposition?.match(/filename=([^;]+)/)
      const filename = filenameMatch ? filenameMatch[1] : `generated-code-${Date.now()}.zip`

      a.download = filename
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)

      toast({
        title: 'Download thành công!',
        description: `File ZIP đã được tải: ${filename}`,
        variant: 'success',
      })
    } catch (error) {
      toast({
        title: 'Lỗi tải file',
        description: getErrorMessage(error),
        variant: 'error',
      })
    }
  }, [blueprint, toast])

  // Calculate progress percentage
  const progressPercent = (progress.completed_steps / progress.total_steps) * 100

  // Show message if no blueprint (user navigated directly to this page)
  if (!blueprint) {
    return (
      <DashboardLayout>
        <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-6">
          <div className="text-center space-y-4">
            <div className="text-6xl">📋</div>
            <h1 className="text-2xl font-bold">Chưa có Blueprint</h1>
            <p className="text-muted-foreground max-w-md">
              Bạn cần tạo Blueprint trước khi có thể generate code.
              Hãy bắt đầu từ trang Onboarding để tạo Blueprint cho ứng dụng của bạn.
            </p>
          </div>
          <Button onClick={() => navigate('/app-builder')} size="lg">
            Đi đến App Builder
          </Button>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate('/app-builder')}
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Quay lại App Builder
              </Button>
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Code Generation</h1>
            <p className="text-muted-foreground mt-1">
              Tạo code từ AppBlueprint với 4-Gate Quality Pipeline
            </p>
          </div>
          <div className="flex items-center gap-2">
            <StatusIcon status={progress.status} />
            <Badge variant={STATUS_VARIANTS[progress.status]}>
              {STATUS_LABELS[progress.status]}
            </Badge>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column - Blueprint Viewer */}
          <div className="space-y-6">
            <BlueprintJsonViewer
              blueprint={blueprint as any}
            />

            {/* Stats from onboarding */}
            {stats && (
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Thống kê Blueprint</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <div className="font-bold text-lg">{(stats as any).modules_count || 0}</div>
                      <div className="text-muted-foreground">Modules</div>
                    </div>
                    <div>
                      <div className="font-bold text-lg">{(stats as any).entities_count || 0}</div>
                      <div className="text-muted-foreground">Entities</div>
                    </div>
                    <div>
                      <div className="font-bold text-lg">{(stats as any).endpoints_count || 0}</div>
                      <div className="text-muted-foreground">Endpoints</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Generation Controls & Progress */}
          <div className="space-y-6">
            {/* Generation Controls */}
            <Card>
              <CardHeader>
                <CardTitle>Tạo Code</CardTitle>
                <CardDescription>
                  Nhấn nút bên dưới để bắt đầu quá trình tạo code từ Blueprint
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-3">
                  <Button
                    onClick={handleStartGeneration}
                    disabled={generateMutation.isPending || isStreaming || progress.status === 'generating'}
                    className="flex-1"
                  >
                    {(generateMutation.isPending || isStreaming) ? (
                      <>
                        <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                        {isStreaming ? 'Đang stream...' : 'Đang xử lý...'}
                      </>
                    ) : (
                      <>
                        <Play className="h-4 w-4 mr-2" />
                        Bắt đầu Generate
                      </>
                    )}
                  </Button>
                  <Button
                    variant="outline"
                    onClick={handleDownloadZip}
                    disabled={progress.status !== 'completed'}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download ZIP
                  </Button>
                </div>

                {/* Progress Section */}
                {progress.status !== 'idle' && (
                  <>
                    <Separator />
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-sm">
                        <span>{progress.current_step}</span>
                        <span className="text-muted-foreground">
                          {progress.completed_steps}/{progress.total_steps}
                        </span>
                      </div>
                      <Progress value={progressPercent} className="h-2" />

                      {progress.current_gate && (
                        <div className="text-sm text-muted-foreground">
                          {progress.current_gate}
                        </div>
                      )}
                    </div>
                  </>
                )}

                {/* Errors */}
                {progress.errors.length > 0 && (
                  <Alert variant="destructive">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertTitle>Lỗi</AlertTitle>
                    <AlertDescription>
                      <ul className="list-disc list-inside">
                        {progress.errors.map((err, idx) => (
                          <li key={idx}>{err}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                )}

                {/* Warnings */}
                {progress.warnings.length > 0 && (
                  <Alert>
                    <AlertTriangle className="h-4 w-4" />
                    <AlertTitle>Cảnh báo</AlertTitle>
                    <AlertDescription>
                      <ul className="list-disc list-inside">
                        {progress.warnings.map((warn, idx) => (
                          <li key={idx}>{warn}</li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                )}
              </CardContent>
            </Card>

            {/* Generated Files List */}
            {generatedCode && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>Generated Files</span>
                    <Badge variant="secondary">
                      {generatedCode.total_files ?? 0} files • {(generatedCode.total_lines ?? 0).toLocaleString()} lines
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 max-h-[300px] overflow-auto">
                    {generatedCode.files?.map((file, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between p-2 rounded-lg bg-muted/50 text-sm"
                      >
                        <div className="flex items-center gap-2 truncate">
                          <Badge variant="outline" className="text-xs">
                            {file.language}
                          </Badge>
                          <span className="truncate font-mono text-xs">{file.path}</span>
                        </div>
                        <span className="text-muted-foreground text-xs">
                          {file.lines} lines
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* 4-Gate Quality Pipeline - Shows real results from backend */}
            <Card>
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm">4-Gate Quality Pipeline</CardTitle>
                  {generatedCode?.quality && (
                    <Badge variant={generatedCode.quality.success ? 'default' : 'destructive'}>
                      {generatedCode.quality.summary}
                    </Badge>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  {generatedCode?.quality?.gates ? (
                    // Show real gate results from backend
                    generatedCode.quality.gates.map((gate, idx) => (
                      <div
                        key={idx}
                        className={`flex items-center justify-between p-2 rounded-lg ${
                          gate.status === 'passed'
                            ? 'bg-green-500/10 text-green-700 dark:text-green-400'
                            : gate.status === 'failed'
                            ? 'bg-red-500/10 text-red-700 dark:text-red-400'
                            : gate.status === 'skipped'
                            ? 'bg-yellow-500/10 text-yellow-700 dark:text-yellow-400'
                            : 'bg-muted/50 text-muted-foreground'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          {gate.status === 'passed' ? (
                            <CheckCircle2 className="h-4 w-4" />
                          ) : gate.status === 'failed' ? (
                            <XCircle className="h-4 w-4" />
                          ) : gate.status === 'skipped' ? (
                            <AlertTriangle className="h-4 w-4" />
                          ) : (
                            <Clock className="h-4 w-4" />
                          )}
                          <span className="font-medium">{gate.gate_name}</span>
                        </div>
                        <div className="flex items-center gap-2 text-xs">
                          {gate.error_count > 0 && (
                            <span className="text-red-600">{gate.error_count} errors</span>
                          )}
                          {gate.warning_count > 0 && (
                            <span className="text-yellow-600">{gate.warning_count} warnings</span>
                          )}
                          <span>{gate.duration_ms}ms</span>
                        </div>
                      </div>
                    ))
                  ) : (
                    // Show static placeholder before generation
                    [
                      { name: 'Syntax Check', desc: 'AST parse, ruff' },
                      { name: 'Security (SAST)', desc: 'Semgrep scan' },
                      { name: 'Context Validation', desc: 'Import checks' },
                      { name: 'Test Coverage', desc: 'pytest sandbox' },
                    ].map((item, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between p-2 rounded-lg bg-muted/50 text-muted-foreground"
                      >
                        <div className="flex items-center gap-2">
                          <Clock className="h-4 w-4" />
                          <span className="font-medium">{item.name}</span>
                        </div>
                        <span className="text-xs">{item.desc}</span>
                      </div>
                    ))
                  )}
                </div>

                {/* Show quality issues if any */}
                {generatedCode?.quality?.gates.some(g => g.issues.length > 0) && (
                  <div className="mt-4 space-y-2">
                    <div className="text-xs font-medium text-muted-foreground">Issues Found:</div>
                    <div className="max-h-[150px] overflow-auto space-y-1">
                      {generatedCode.quality.gates.flatMap(g =>
                        g.issues.slice(0, 5).map((issue, i) => (
                          <div
                            key={`${g.gate_number}-${i}`}
                            className={`text-xs p-2 rounded ${
                              issue.severity === 'error'
                                ? 'bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-300'
                                : 'bg-yellow-50 dark:bg-yellow-950 text-yellow-700 dark:text-yellow-300'
                            }`}
                          >
                            <div className="font-mono">{issue.file}:{issue.line || '?'}</div>
                            <div>{issue.message}</div>
                            {issue.suggestion && (
                              <div className="text-muted-foreground mt-1">💡 {issue.suggestion}</div>
                            )}
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

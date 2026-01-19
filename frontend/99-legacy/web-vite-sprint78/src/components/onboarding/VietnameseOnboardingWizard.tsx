/**
 * File: frontend/web/src/components/onboarding/VietnameseOnboardingWizard.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 47
 * Date: December 23, 2025
 * Authority: Frontend Lead + CTO Approved
 * Foundation: Vietnamese Domain Templates + Onboarding IR (EP-06)
 *
 * Description:
 * Vietnamese SME onboarding wizard for F&B, Hospitality, and Retail domains.
 * 5-step guided flow: Domain → App Name → Features → Scale → Generate
 */

import { useState, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Badge } from '@/components/ui/badge'
import { useOnboardingWizard } from '@/hooks/useOnboarding'
import OnboardingProgress from './OnboardingProgress'
import type {
  OnboardingStep,
  DomainOption,
  FeatureOption,
  ScaleOption,
} from '@/types/onboarding'

// Vietnamese labels
const LABELS_VI: Record<OnboardingStep, string> = {
  welcome: 'Chào mừng',
  domain: 'Chọn ngành nghề',
  app_name: 'Tên ứng dụng',
  features: 'Chọn tính năng',
  scale: 'Quy mô doanh nghiệp',
  confirm: 'Xác nhận',
  complete: 'Hoàn tất',
}

// Domain icons
const ICONS: Record<string, string> = {
  restaurant: '🍜',
  hotel: '🏨',
  retail: '🛒',
}

// Scale tier badge colors
const TIER_COLORS: Record<string, string> = {
  LITE: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100',
  STANDARD: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100',
  PROFESSIONAL: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100',
  ENTERPRISE: 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-100',
}

interface VietnameseOnboardingWizardProps {
  onComplete?: (blueprint: unknown) => void
  onCancel?: () => void
}

/**
 * Vietnamese SME Onboarding Wizard
 *
 * Guides Vietnamese SME founders through a 5-step process to generate
 * an AppBlueprint IR for code generation.
 */
export default function VietnameseOnboardingWizard({
  onComplete,
  onCancel,
}: VietnameseOnboardingWizardProps) {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [appNameInput, setAppNameInput] = useState('')
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  const {
    session,
    domains,
    features,
    scales,
    start,
    setDomain,
    setAppName,
    setFeatures,
    setScale,
    generate,
    isLoading,
    blueprint,
    blueprintStats,
  } = useOnboardingWizard(sessionId)

  // Start new session
  const handleStart = useCallback(async () => {
    try {
      setError(null)
      const newSession = await start({ locale: 'vi' })
      setSessionId(newSession.session_id)
    } catch (err) {
      setError('Không thể bắt đầu. Vui lòng thử lại.')
      console.error('Failed to start onboarding:', err)
    }
  }, [start])

  // Select domain
  const handleDomainSelect = useCallback(async (domain: string) => {
    if (!sessionId) return
    try {
      setError(null)
      await setDomain({ domain })
    } catch (err) {
      setError('Không thể chọn ngành nghề. Vui lòng thử lại.')
      console.error('Failed to set domain:', err)
    }
  }, [sessionId, setDomain])

  // Submit app name
  const handleAppNameSubmit = useCallback(async () => {
    if (!sessionId || !appNameInput.trim()) return
    try {
      setError(null)
      await setAppName({ app_name: appNameInput.trim() })
    } catch (err) {
      setError('Tên ứng dụng không hợp lệ. Vui lòng thử lại.')
      console.error('Failed to set app name:', err)
    }
  }, [sessionId, appNameInput, setAppName])

  // Toggle feature selection
  const handleFeatureToggle = useCallback((featureKey: string) => {
    setSelectedFeatures(prev =>
      prev.includes(featureKey)
        ? prev.filter(f => f !== featureKey)
        : [...prev, featureKey]
    )
  }, [])

  // Submit features
  const handleFeaturesSubmit = useCallback(async () => {
    if (!sessionId || selectedFeatures.length === 0) return
    try {
      setError(null)
      await setFeatures({ features: selectedFeatures })
    } catch (err) {
      setError('Không thể lưu tính năng. Vui lòng thử lại.')
      console.error('Failed to set features:', err)
    }
  }, [sessionId, selectedFeatures, setFeatures])

  // Select scale
  const handleScaleSelect = useCallback(async (scaleKey: string) => {
    if (!sessionId) return
    try {
      setError(null)
      await setScale({ scale: scaleKey })
    } catch (err) {
      setError('Không thể chọn quy mô. Vui lòng thử lại.')
      console.error('Failed to set scale:', err)
    }
  }, [sessionId, setScale])

  // Generate blueprint
  const handleGenerate = useCallback(async () => {
    if (!sessionId) return
    try {
      setError(null)
      const result = await generate()
      if (result.success && result.blueprint) {
        onComplete?.(result.blueprint)
      } else {
        setError(result.errors.join(', ') || 'Không thể tạo blueprint.')
      }
    } catch (err) {
      setError('Lỗi tạo blueprint. Vui lòng thử lại.')
      console.error('Failed to generate blueprint:', err)
    }
  }, [sessionId, generate, onComplete])

  // Get current step number for progress
  const getStepNumber = (step: OnboardingStep): number => {
    const steps: OnboardingStep[] = ['welcome', 'domain', 'app_name', 'features', 'scale', 'confirm', 'complete']
    return steps.indexOf(step) + 1
  }

  const currentStep = session?.current_step ?? 'welcome'
  const stepNumber = getStepNumber(currentStep)

  // Render step content
  const renderStepContent = () => {
    // Welcome step (before session starts)
    if (!session) {
      return (
        <div className="text-center space-y-6">
          <div className="text-6xl">🚀</div>
          <h2 className="text-2xl font-bold">Tạo ứng dụng cho doanh nghiệp của bạn</h2>
          <p className="text-muted-foreground">
            Chỉ cần 5 bước đơn giản để tạo ứng dụng quản lý phù hợp với ngành nghề của bạn.
            Hỗ trợ Nhà hàng, Khách sạn và Bán lẻ.
          </p>
          <Button onClick={handleStart} disabled={isLoading} size="lg">
            {isLoading ? 'Đang xử lý...' : 'Bắt đầu ngay'}
          </Button>
        </div>
      )
    }

    // Domain selection
    if (currentStep === 'domain') {
      return (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Doanh nghiệp của bạn thuộc ngành nào?</h3>
          <div className="grid gap-4 md:grid-cols-3">
            {domains?.map((domain: DomainOption) => (
              <Card
                key={domain.key}
                className={`cursor-pointer transition-all hover:border-primary ${
                  session.domain === domain.key ? 'border-primary bg-primary/5' : ''
                }`}
                onClick={() => handleDomainSelect(domain.key)}
              >
                <CardHeader className="text-center pb-2">
                  <div className="text-4xl mb-2">{ICONS[domain.key] || '📦'}</div>
                  <CardTitle className="text-lg">{domain.name}</CardTitle>
                  <CardDescription className="text-sm">{domain.description}</CardDescription>
                </CardHeader>
                <CardContent className="text-center text-xs text-muted-foreground">
                  VD: {domain.example_apps.slice(0, 2).join(', ')}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )
    }

    // App name input
    if (currentStep === 'app_name') {
      return (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Đặt tên cho ứng dụng của bạn</h3>
          <p className="text-sm text-muted-foreground">
            Bạn có thể nhập tiếng Việt có dấu. Ví dụ: Quán Phở 24, Nhà Hàng Hải Sản Biển Đông
          </p>
          <div className="space-y-2">
            <Label htmlFor="app-name">Tên ứng dụng</Label>
            <Input
              id="app-name"
              value={appNameInput}
              onChange={(e) => setAppNameInput(e.target.value)}
              placeholder="Nhập tên ứng dụng..."
              className="text-lg"
              autoFocus
            />
            {session.app_name_display && (
              <p className="text-sm text-muted-foreground">
                Tên đã chuẩn hóa: <code className="bg-muted px-1 rounded">{session.app_name}</code>
              </p>
            )}
          </div>
          <Button
            onClick={handleAppNameSubmit}
            disabled={isLoading || !appNameInput.trim()}
          >
            {isLoading ? 'Đang lưu...' : 'Tiếp tục'}
          </Button>
        </div>
      )
    }

    // Feature selection
    if (currentStep === 'features') {
      return (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Chọn các tính năng bạn cần</h3>
          <p className="text-sm text-muted-foreground">
            Chọn ít nhất 1 tính năng. Bạn có thể thêm tính năng khác sau.
          </p>
          <div className="grid gap-3 md:grid-cols-2">
            {features?.map((feature: FeatureOption) => (
              <div
                key={feature.key}
                className={`flex items-start space-x-3 p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedFeatures.includes(feature.key)
                    ? 'border-primary bg-primary/5'
                    : 'hover:border-muted-foreground/50'
                }`}
                onClick={() => handleFeatureToggle(feature.key)}
              >
                <Checkbox
                  checked={selectedFeatures.includes(feature.key)}
                  onCheckedChange={() => handleFeatureToggle(feature.key)}
                />
                <div className="space-y-1">
                  <p className="font-medium leading-none">{feature.name}</p>
                  <p className="text-sm text-muted-foreground">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              Đã chọn: {selectedFeatures.length} tính năng
            </p>
            <Button
              onClick={handleFeaturesSubmit}
              disabled={isLoading || selectedFeatures.length === 0}
            >
              {isLoading ? 'Đang lưu...' : 'Tiếp tục'}
            </Button>
          </div>
        </div>
      )
    }

    // Scale selection
    if (currentStep === 'scale') {
      return (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Quy mô doanh nghiệp của bạn</h3>
          <p className="text-sm text-muted-foreground">
            Chọn quy mô phù hợp để chúng tôi đề xuất cấu hình tối ưu.
          </p>
          <div className="grid gap-3">
            {scales?.map((scale: ScaleOption) => (
              <Card
                key={scale.key}
                className={`cursor-pointer transition-all hover:border-primary ${
                  session.scale === scale.key ? 'border-primary bg-primary/5' : ''
                }`}
                onClick={() => handleScaleSelect(scale.key)}
              >
                <CardContent className="flex items-center justify-between p-4">
                  <div>
                    <p className="font-medium">{scale.label}</p>
                    <p className="text-sm text-muted-foreground">
                      {scale.employee_min === 0
                        ? `Dưới ${scale.employee_max} nhân viên`
                        : scale.employee_max === 9999
                        ? `Trên ${scale.employee_min} nhân viên`
                        : `${scale.employee_min} - ${scale.employee_max} nhân viên`}
                    </p>
                  </div>
                  <Badge className={TIER_COLORS[scale.cgf_tier] || ''}>
                    {scale.cgf_tier}
                  </Badge>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )
    }

    // Confirm step
    if (currentStep === 'confirm') {
      return (
        <div className="space-y-6">
          <h3 className="text-lg font-semibold">Xác nhận thông tin</h3>
          <div className="space-y-4 bg-muted/50 p-4 rounded-lg">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Ngành nghề:</span>
              <span className="font-medium">
                {ICONS[session.domain || ''] || ''} {domains?.find(d => d.key === session.domain)?.name}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Tên ứng dụng:</span>
              <span className="font-medium">{session.app_name_display || session.app_name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Tính năng:</span>
              <span className="font-medium">{session.features.length} modules</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Quy mô:</span>
              <span className="font-medium">
                {scales?.find(s => s.key === session.scale)?.label}
              </span>
            </div>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" onClick={onCancel}>
              Hủy
            </Button>
            <Button onClick={handleGenerate} disabled={isLoading} className="flex-1">
              {isLoading ? 'Đang tạo...' : '🚀 Tạo ứng dụng'}
            </Button>
          </div>
        </div>
      )
    }

    // Complete step
    if (currentStep === 'complete' && blueprint) {
      return (
        <div className="text-center space-y-6">
          <div className="text-6xl">🎉</div>
          <h2 className="text-2xl font-bold">Tạo thành công!</h2>
          <p className="text-muted-foreground">
            Blueprint đã được tạo với {blueprintStats?.modules_count || 0} modules,{' '}
            {blueprintStats?.entities_count || 0} entities, và{' '}
            {blueprintStats?.endpoints_count || 0} endpoints.
          </p>
          <div className="bg-muted/50 p-4 rounded-lg text-left">
            <pre className="text-xs overflow-auto max-h-64">
              {JSON.stringify(blueprint, null, 2)}
            </pre>
          </div>
          <Button onClick={() => onComplete?.(blueprint)}>
            Tiếp tục tạo code
          </Button>
        </div>
      )
    }

    return null
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <Card>
          <CardHeader>
            {session && currentStep !== 'complete' && (
              <OnboardingProgress current={stepNumber} total={6} />
            )}
            <CardTitle className="text-center mt-4">
              {session ? LABELS_VI[currentStep] : 'Tạo ứng dụng SME'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {error && (
              <div className="mb-4 p-3 bg-destructive/10 text-destructive rounded-lg text-sm">
                {error}
              </div>
            )}
            {renderStepContent()}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

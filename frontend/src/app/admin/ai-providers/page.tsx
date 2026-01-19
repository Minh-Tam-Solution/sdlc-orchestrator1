/**
 * AI Providers Configuration Page - Admin Panel
 * @route /admin/ai-providers
 * @status Sprint 70 - AI Provider Admin UI
 * @description Compact single-page AI provider configuration for platform admins
 */
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  ArrowLeft,
  Bot,
  CheckCircle2,
  XCircle,
  Loader2,
  Eye,
  EyeOff,
  RefreshCw,
  Save,
  RotateCcw,
} from "lucide-react";
import { useToast } from "@/hooks/useToast";
import {
  useAIProviderConfig,
  useUpdateAIProvider,
  useTestAIProvider,
  useRefreshOllamaModels,
  type TestResult,
} from "@/hooks/useAIProviders";

interface ProviderFormState {
  ollama: {
    url: string;
    model: string;
  };
  claude: {
    apiKey: string;
    model: string;
  };
  openai: {
    apiKey: string;
    model: string;
  };
  defaultProvider: string;
  fallbackEnabled: boolean;
  fallbackChain: string[];
}

interface TestState {
  ollama?: TestResult;
  claude?: TestResult;
  openai?: TestResult;
}

export default function AIProvidersPage() {
  const router = useRouter();
  const { toast } = useToast();

  const { data: config, isLoading, error, refetch } = useAIProviderConfig();
  const updateMutation = useUpdateAIProvider();
  const testMutation = useTestAIProvider();
  const refreshModelsMutation = useRefreshOllamaModels();

  const [showClaudeKey, setShowClaudeKey] = useState(false);
  const [showOpenAIKey, setShowOpenAIKey] = useState(false);
  const [testResults, setTestResults] = useState<TestState>({});
  const [testingProvider, setTestingProvider] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [ollamaModelsList, setOllamaModelsList] = useState<string[]>([]);

  // Form state
  const [form, setForm] = useState<ProviderFormState>({
    ollama: { url: "", model: "" },
    claude: { apiKey: "", model: "" },
    openai: { apiKey: "", model: "" },
    defaultProvider: "ollama",
    fallbackEnabled: true,
    fallbackChain: ["ollama", "openai", "claude"],
  });

  // Original state for revert
  const [originalForm, setOriginalForm] = useState<ProviderFormState | null>(null);

  // Initialize form from config
  useEffect(() => {
    if (config) {
      const newForm: ProviderFormState = {
        ollama: {
          url: config.ollama.url || "",
          model: config.ollama.model || "",
        },
        claude: {
          apiKey: "",
          model: config.claude.model || "claude-sonnet-4-5-20250929",
        },
        openai: {
          apiKey: "",
          model: config.openai.model || "gpt-4o",
        },
        defaultProvider: config.default_provider,
        fallbackEnabled: config.fallback_enabled,
        fallbackChain: config.fallback_chain,
      };
      setForm(newForm);
      setOriginalForm(newForm);
    }
  }, [config]);

  const handleTest = async (provider: "ollama" | "claude" | "openai") => {
    setTestingProvider(provider);
    try {
      const result = await testMutation.mutateAsync(provider);
      setTestResults((prev) => ({ ...prev, [provider]: result }));
      if (result.success) {
        toast({
          title: "Connection OK",
          description: `${result.latency_ms}ms`,
        });
      }
    } catch {
      toast({
        title: "Test Failed",
        description: "Connection error",
        variant: "destructive",
      });
    } finally {
      setTestingProvider(null);
    }
  };

  const handleRefreshModels = async () => {
    try {
      const models = await refreshModelsMutation.mutateAsync();
      setOllamaModelsList(models);
      toast({ title: `${models.length} models loaded` });
    } catch {
      toast({
        title: "Refresh failed",
        variant: "destructive",
      });
    }
  };

  const handleSaveAll = async () => {
    setIsSaving(true);
    try {
      // Save Ollama settings
      if (form.ollama.url || form.ollama.model) {
        await updateMutation.mutateAsync({
          provider: "ollama",
          data: {
            url: form.ollama.url,
            model: form.ollama.model,
          },
        });
      }

      // Save Claude settings
      if (form.claude.apiKey || form.claude.model) {
        await updateMutation.mutateAsync({
          provider: "claude",
          data: {
            ...(form.claude.apiKey && { api_key: form.claude.apiKey }),
            model: form.claude.model,
          },
        });
      }

      // Save OpenAI settings
      if (form.openai.apiKey || form.openai.model) {
        await updateMutation.mutateAsync({
          provider: "openai",
          data: {
            ...(form.openai.apiKey && { api_key: form.openai.apiKey }),
            model: form.openai.model,
          },
        });
      }

      // Save fallback settings
      await updateMutation.mutateAsync({
        provider: "fallback",
        data: {
          default_provider: form.defaultProvider,
          fallback_enabled: form.fallbackEnabled,
          fallback_chain: form.fallbackChain,
        },
      });

      await refetch();
      setOriginalForm(form);
      toast({
        title: "Settings Saved",
        description: "AI provider configuration updated",
      });
    } catch {
      toast({
        title: "Save Failed",
        description: "Check configuration and try again",
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleRevert = () => {
    if (originalForm) {
      setForm(originalForm);
      toast({ title: "Changes reverted" });
    }
  };

  const getStatusIndicator = (provider: "ollama" | "claude" | "openai") => {
    if (!config) return null;
    const status = config[provider];
    if (status.configured && status.available) {
      return <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-2" title="Active" />;
    }
    return <span className="inline-block w-2 h-2 rounded-full bg-gray-300 mr-2" title="Not configured" />;
  };

  const getTestButton = (provider: "ollama" | "claude" | "openai") => {
    const isThisTesting = testingProvider === provider;
    const result = testResults[provider];

    if (isThisTesting) {
      return (
        <Button variant="outline" size="sm" disabled className="w-20">
          <Loader2 className="h-3 w-3 animate-spin" />
        </Button>
      );
    }

    if (result) {
      return (
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleTest(provider)}
          className={`w-20 ${result.success ? "text-green-600" : "text-red-600"}`}
        >
          {result.success ? (
            <>
              <CheckCircle2 className="h-3 w-3 mr-1" />
              {result.latency_ms}ms
            </>
          ) : (
            <>
              <XCircle className="h-3 w-3 mr-1" />
              Error
            </>
          )}
        </Button>
      );
    }

    return (
      <Button variant="outline" size="sm" onClick={() => handleTest(provider)} className="w-20">
        Test
      </Button>
    );
  };

  if (error) {
    return (
      <div className="space-y-6 p-6">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => router.push("/admin")}
            className="h-8 w-8 p-0"
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            <h1 className="text-xl font-semibold">AI Providers</h1>
          </div>
        </div>
        <div className="border border-red-200 bg-red-50 rounded-lg p-4">
          <p className="text-red-600 font-medium">Failed to load configuration</p>
          <p className="text-red-500 text-sm mt-1">{error.message}</p>
          <Button variant="outline" size="sm" onClick={() => refetch()} className="mt-3">
            Retry
          </Button>
        </div>
      </div>
    );
  }

  if (isLoading || !config) {
    return (
      <div className="space-y-6 p-6">
        <div className="h-8 w-48 bg-muted rounded animate-pulse" />
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-muted rounded animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  // Use local state for ollama models (fetched async), fallback to config
  const ollamaModels = ollamaModelsList.length > 0
    ? ollamaModelsList
    : (config.available_models?.ollama || []);
  const claudeModels = config.available_models?.claude || [];
  const openaiModels = config.available_models?.openai || [];

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => router.push("/admin")}
            className="h-8 w-8 p-0"
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div className="flex items-center gap-2">
            <Bot className="h-5 w-5" />
            <h1 className="text-xl font-semibold">AI Providers</h1>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleRevert} disabled={isSaving}>
            <RotateCcw className="h-4 w-4 mr-1" />
            Revert
          </Button>
          <Button size="sm" onClick={handleSaveAll} disabled={isSaving}>
            {isSaving ? <Loader2 className="h-4 w-4 mr-1 animate-spin" /> : <Save className="h-4 w-4 mr-1" />}
            Save All
          </Button>
        </div>
      </div>

      {/* OLLAMA */}
      <div className="border rounded-lg p-4 space-y-3">
        <div className="flex items-center">
          {getStatusIndicator("ollama")}
          <span className="font-medium">OLLAMA</span>
          {config.ollama.configured && (
            <span className="ml-2 text-xs text-green-600">Active</span>
          )}
          {!config.ollama.configured && (
            <span className="ml-2 text-xs text-muted-foreground">Not configured</span>
          )}
        </div>
        <div className="grid grid-cols-12 gap-3 items-end">
          <div className="col-span-5">
            <Label htmlFor="ollama-url" className="text-xs text-muted-foreground">URL</Label>
            <Input
              id="ollama-url"
              placeholder="http://api.nhatquangholding.com:11434"
              value={form.ollama.url}
              onChange={(e) => setForm((f) => ({ ...f, ollama: { ...f.ollama, url: e.target.value } }))}
              className="h-9"
            />
          </div>
          <div className="col-span-4">
            <Label htmlFor="ollama-model" className="text-xs text-muted-foreground">Model</Label>
            <Select
              value={form.ollama.model}
              onValueChange={(v) => setForm((f) => ({ ...f, ollama: { ...f.ollama, model: v } }))}
            >
              <SelectTrigger id="ollama-model" className="h-9">
                <SelectValue placeholder="Select model" />
              </SelectTrigger>
              <SelectContent>
                {ollamaModels.length > 0 ? (
                  ollamaModels.map((m) => (
                    <SelectItem key={m} value={m}>{m}</SelectItem>
                  ))
                ) : (
                  <div className="px-2 py-1.5 text-sm text-muted-foreground">No models available</div>
                )}
              </SelectContent>
            </Select>
          </div>
          <div className="col-span-3 flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleRefreshModels}
              disabled={refreshModelsMutation.isPending}
              className="h-9 px-2"
              title="Refresh models"
            >
              <RefreshCw className={`h-4 w-4 ${refreshModelsMutation.isPending ? "animate-spin" : ""}`} />
            </Button>
            {getTestButton("ollama")}
          </div>
        </div>
      </div>

      {/* CLAUDE */}
      <div className="border rounded-lg p-4 space-y-3">
        <div className="flex items-center">
          {getStatusIndicator("claude")}
          <span className="font-medium">CLAUDE</span>
          {config.claude.configured && (
            <span className="ml-2 text-xs text-green-600">Active</span>
          )}
          {!config.claude.configured && (
            <span className="ml-2 text-xs text-muted-foreground">Not configured</span>
          )}
        </div>
        <div className="grid grid-cols-12 gap-3 items-end">
          <div className="col-span-5">
            <Label htmlFor="claude-key" className="text-xs text-muted-foreground">API Key</Label>
            <div className="relative">
              <Input
                id="claude-key"
                type={showClaudeKey ? "text" : "password"}
                placeholder={config.claude.configured ? "sk-ant-••••••••••••" : "sk-ant-..."}
                value={form.claude.apiKey}
                onChange={(e) => setForm((f) => ({ ...f, claude: { ...f.claude, apiKey: e.target.value } }))}
                className="h-9 pr-8"
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-1 top-1/2 -translate-y-1/2 h-6 w-6 p-0"
                onClick={() => setShowClaudeKey(!showClaudeKey)}
              >
                {showClaudeKey ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
              </Button>
            </div>
          </div>
          <div className="col-span-4">
            <Label htmlFor="claude-model" className="text-xs text-muted-foreground">Model</Label>
            <Select
              value={form.claude.model}
              onValueChange={(v) => setForm((f) => ({ ...f, claude: { ...f.claude, model: v } }))}
            >
              <SelectTrigger id="claude-model" className="h-9">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {claudeModels.map((m) => (
                  <SelectItem key={m} value={m}>{m}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="col-span-3">
            {getTestButton("claude")}
          </div>
        </div>
        {testResults.claude && !testResults.claude.success && (
          <p className="text-xs text-red-600">{testResults.claude.error}</p>
        )}
      </div>

      {/* OPENAI */}
      <div className="border rounded-lg p-4 space-y-3">
        <div className="flex items-center">
          {getStatusIndicator("openai")}
          <span className="font-medium">OPENAI</span>
          {config.openai.configured && (
            <span className="ml-2 text-xs text-green-600">Active</span>
          )}
          {!config.openai.configured && (
            <span className="ml-2 text-xs text-muted-foreground">Not configured</span>
          )}
        </div>
        <div className="grid grid-cols-12 gap-3 items-end">
          <div className="col-span-5">
            <Label htmlFor="openai-key" className="text-xs text-muted-foreground">API Key</Label>
            <div className="relative">
              <Input
                id="openai-key"
                type={showOpenAIKey ? "text" : "password"}
                placeholder={config.openai.configured ? "sk-••••••••••••" : "sk-..."}
                value={form.openai.apiKey}
                onChange={(e) => setForm((f) => ({ ...f, openai: { ...f.openai, apiKey: e.target.value } }))}
                className="h-9 pr-8"
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-1 top-1/2 -translate-y-1/2 h-6 w-6 p-0"
                onClick={() => setShowOpenAIKey(!showOpenAIKey)}
              >
                {showOpenAIKey ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
              </Button>
            </div>
          </div>
          <div className="col-span-4">
            <Label htmlFor="openai-model" className="text-xs text-muted-foreground">Model</Label>
            <Select
              value={form.openai.model}
              onValueChange={(v) => setForm((f) => ({ ...f, openai: { ...f.openai, model: v } }))}
            >
              <SelectTrigger id="openai-model" className="h-9">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {openaiModels.map((m) => (
                  <SelectItem key={m} value={m}>{m}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="col-span-3">
            {getTestButton("openai")}
          </div>
        </div>
        {testResults.openai && !testResults.openai.success && (
          <p className="text-xs text-red-600">{testResults.openai.error}</p>
        )}
      </div>

      {/* FALLBACK */}
      <div className="border rounded-lg p-4 space-y-3">
        <span className="font-medium">FALLBACK</span>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <Label htmlFor="default-provider" className="text-sm text-muted-foreground whitespace-nowrap">Default</Label>
            <Select
              value={form.defaultProvider}
              onValueChange={(v) => setForm((f) => ({ ...f, defaultProvider: v }))}
            >
              <SelectTrigger id="default-provider" className="h-9 w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ollama">ollama</SelectItem>
                <SelectItem value="claude">claude</SelectItem>
                <SelectItem value="openai">openai</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="flex items-center gap-3">
            <Label htmlFor="fallback-toggle" className="text-sm text-muted-foreground whitespace-nowrap">Fallback</Label>
            <Switch
              id="fallback-toggle"
              checked={form.fallbackEnabled}
              onCheckedChange={(v) => setForm((f) => ({ ...f, fallbackEnabled: v }))}
            />
          </div>
          {form.fallbackEnabled && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>Order:</span>
              <span className="font-mono text-foreground">
                {form.fallbackChain.join("→")}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

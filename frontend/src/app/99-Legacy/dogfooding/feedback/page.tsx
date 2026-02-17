"use client";

/**
 * Developer Feedback Survey - Sprint 114 Track 2
 *
 * Collects developer satisfaction, NPS scores, and qualitative feedback
 * for WARNING mode governance evaluation.
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Checkbox } from "@/components/ui/checkbox";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  CheckCircle2,
  AlertCircle,
  Frown,
  Meh,
  Smile,
  ThumbsDown,
  ThumbsUp,
  Clock,
  MessageSquare,
  Target,
  ArrowLeft
} from "lucide-react";

// ============================================================================
// Types
// ============================================================================

type FeedbackRating =
  | "very_dissatisfied"
  | "dissatisfied"
  | "neutral"
  | "satisfied"
  | "very_satisfied";

type FeedbackCategory =
  | "friction"
  | "false_positive"
  | "auto_generation"
  | "ui_ux"
  | "documentation"
  | "other";

interface FeedbackFormData {
  rating: FeedbackRating;
  npsScore: number;
  frictionMinutes: number;
  category: FeedbackCategory;
  helpfulAspects: string[];
  painPoints: string[];
  suggestions: string;
  wouldRecommend: boolean;
  prNumber: number | null;
}

// ============================================================================
// Constants
// ============================================================================

const RATING_OPTIONS: { value: FeedbackRating; label: string; icon: React.ReactNode; color: string }[] = [
  { value: "very_dissatisfied", label: "Very Dissatisfied", icon: <Frown className="h-6 w-6" />, color: "text-red-500" },
  { value: "dissatisfied", label: "Dissatisfied", icon: <Frown className="h-6 w-6" />, color: "text-orange-500" },
  { value: "neutral", label: "Neutral", icon: <Meh className="h-6 w-6" />, color: "text-yellow-500" },
  { value: "satisfied", label: "Satisfied", icon: <Smile className="h-6 w-6" />, color: "text-green-500" },
  { value: "very_satisfied", label: "Very Satisfied", icon: <Smile className="h-6 w-6" />, color: "text-emerald-500" },
];

const CATEGORY_OPTIONS: { value: FeedbackCategory; label: string; description: string }[] = [
  { value: "friction", label: "Developer Friction", description: "Time spent dealing with governance" },
  { value: "false_positive", label: "False Positives", description: "Incorrect violation flags" },
  { value: "auto_generation", label: "Auto-Generation", description: "AI-generated content quality" },
  { value: "ui_ux", label: "UI/UX", description: "Dashboard and interface" },
  { value: "documentation", label: "Documentation", description: "Guides and help resources" },
  { value: "other", label: "Other", description: "General feedback" },
];

const HELPFUL_ASPECTS = [
  "Auto-generation saves time",
  "Clear violation messages",
  "Vibecoding Index is intuitive",
  "Dashboard is easy to use",
  "Quick evaluation response",
  "Good documentation",
  "Helpful PR comments",
];

const PAIN_POINTS = [
  "Too many false positives",
  "Slow evaluation time",
  "Confusing error messages",
  "Index calculation unclear",
  "Auto-generation quality issues",
  "Dashboard is slow",
  "Missing documentation",
  "Friction interrupts workflow",
];

// ============================================================================
// Components
// ============================================================================

function NPSScale({ value, onChange }: { value: number; onChange: (v: number) => void }) {
  const getColor = (score: number) => {
    if (score <= 6) return "bg-red-500";
    if (score <= 8) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between text-sm text-muted-foreground">
        <span className="flex items-center gap-1">
          <ThumbsDown className="h-4 w-4" /> Not at all likely
        </span>
        <span className="flex items-center gap-1">
          Extremely likely <ThumbsUp className="h-4 w-4" />
        </span>
      </div>
      <div className="flex gap-2 justify-between">
        {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((score) => (
          <button
            key={score}
            type="button"
            onClick={() => onChange(score * 10 - 50)} // Convert 0-10 to -50 to 50 NPS
            className={`
              w-10 h-10 rounded-lg font-medium transition-all
              ${value === score * 10 - 50
                ? `${getColor(score)} text-white scale-110`
                : "bg-muted hover:bg-muted/80"
              }
            `}
          >
            {score}
          </button>
        ))}
      </div>
      <div className="text-center text-sm">
        Current Score: <Badge variant={value >= 20 ? "default" : value >= -10 ? "secondary" : "destructive"}>
          {((value + 50) / 10).toFixed(0)}/10
        </Badge>
      </div>
    </div>
  );
}

function CheckboxGroup({
  options,
  selected,
  onChange
}: {
  options: string[];
  selected: string[];
  onChange: (selected: string[]) => void;
}) {
  const toggle = (option: string) => {
    if (selected.includes(option)) {
      onChange(selected.filter(s => s !== option));
    } else {
      onChange([...selected, option]);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
      {options.map((option) => (
        <div key={option} className="flex items-center space-x-2">
          <Checkbox
            id={option}
            checked={selected.includes(option)}
            onCheckedChange={() => toggle(option)}
          />
          <Label htmlFor={option} className="text-sm cursor-pointer">
            {option}
          </Label>
        </div>
      ))}
    </div>
  );
}

// ============================================================================
// Main Component
// ============================================================================

export default function DeveloperFeedbackPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<FeedbackFormData>({
    rating: "neutral",
    npsScore: 0,
    frictionMinutes: 5,
    category: "friction",
    helpfulAspects: [],
    painPoints: [],
    suggestions: "",
    wouldRecommend: true,
    prNumber: null,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch("/api/v1/dogfooding/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          rating: formData.rating,
          nps_score: formData.npsScore,
          friction_minutes: formData.frictionMinutes,
          category: formData.category,
          helpful_aspects: formData.helpfulAspects,
          pain_points: formData.painPoints,
          suggestions: formData.suggestions,
          would_recommend: formData.wouldRecommend,
          pr_number: formData.prNumber,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to submit feedback");
      }

      setIsSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="container max-w-2xl py-8">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center space-y-4">
              <CheckCircle2 className="h-16 w-16 text-green-500 mx-auto" />
              <h2 className="text-2xl font-bold">Thank You!</h2>
              <p className="text-muted-foreground">
                Your feedback has been recorded and will help improve the governance system.
              </p>
              <div className="flex gap-4 justify-center pt-4">
                <Button variant="outline" onClick={() => router.push("/app/governance/dogfooding")}>
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back to Dashboard
                </Button>
                <Button onClick={() => {
                  setIsSubmitted(false);
                  setFormData({
                    rating: "neutral",
                    npsScore: 0,
                    frictionMinutes: 5,
                    category: "friction",
                    helpfulAspects: [],
                    painPoints: [],
                    suggestions: "",
                    wouldRecommend: true,
                    prNumber: null,
                  });
                }}>
                  Submit Another Response
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container max-w-3xl py-8">
      <div className="mb-6">
        <Button variant="ghost" onClick={() => router.push("/app/governance/dogfooding")}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dogfooding Dashboard
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <MessageSquare className="h-6 w-6 text-primary" />
            <div>
              <CardTitle>Developer Feedback Survey</CardTitle>
              <CardDescription>
                Sprint 114 - WARNING Mode Dogfooding
              </CardDescription>
            </div>
          </div>
          <Alert>
            <Target className="h-4 w-4" />
            <AlertTitle>Your feedback matters!</AlertTitle>
            <AlertDescription>
              This survey helps us decide whether to proceed to SOFT enforcement mode in Sprint 115.
              All responses are confidential and used for system improvement only.
            </AlertDescription>
          </Alert>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Overall Satisfaction */}
            <div className="space-y-4">
              <Label className="text-base font-semibold">
                1. Overall, how satisfied are you with the governance system?
              </Label>
              <RadioGroup
                value={formData.rating}
                onValueChange={(v) => setFormData({ ...formData, rating: v as FeedbackRating })}
                className="flex justify-between"
              >
                {RATING_OPTIONS.map((option) => (
                  <div key={option.value} className="flex flex-col items-center gap-2">
                    <RadioGroupItem
                      value={option.value}
                      id={option.value}
                      className="sr-only"
                    />
                    <Label
                      htmlFor={option.value}
                      className={`
                        cursor-pointer p-3 rounded-lg border-2 transition-all
                        ${formData.rating === option.value
                          ? "border-primary bg-primary/10"
                          : "border-transparent hover:border-muted"
                        }
                      `}
                    >
                      <div className={option.color}>{option.icon}</div>
                    </Label>
                    <span className="text-xs text-muted-foreground">{option.label.split(" ")[0]}</span>
                  </div>
                ))}
              </RadioGroup>
            </div>

            {/* NPS Score */}
            <div className="space-y-4">
              <Label className="text-base font-semibold">
                2. How likely are you to recommend this governance system to other teams?
              </Label>
              <NPSScale
                value={formData.npsScore}
                onChange={(v) => setFormData({ ...formData, npsScore: v })}
              />
            </div>

            {/* Friction Time */}
            <div className="space-y-4">
              <Label className="text-base font-semibold">
                3. On average, how many minutes of friction do you experience per PR?
              </Label>
              <div className="space-y-4">
                <Slider
                  value={[formData.frictionMinutes]}
                  onValueChange={(v) => setFormData({ ...formData, frictionMinutes: v[0] })}
                  min={0}
                  max={30}
                  step={1}
                  className="w-full"
                />
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>0 min (none)</span>
                  <span className="font-medium text-foreground flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {formData.frictionMinutes} minutes
                  </span>
                  <span>30+ min (high)</span>
                </div>
                {formData.frictionMinutes > 10 && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      High friction detected. Please share specific pain points below.
                    </AlertDescription>
                  </Alert>
                )}
              </div>
            </div>

            {/* Category */}
            <div className="space-y-4">
              <Label className="text-base font-semibold">
                4. What area does your feedback primarily relate to?
              </Label>
              <RadioGroup
                value={formData.category}
                onValueChange={(v) => setFormData({ ...formData, category: v as FeedbackCategory })}
                className="grid grid-cols-2 md:grid-cols-3 gap-3"
              >
                {CATEGORY_OPTIONS.map((option) => (
                  <div key={option.value}>
                    <RadioGroupItem
                      value={option.value}
                      id={`cat-${option.value}`}
                      className="sr-only"
                    />
                    <Label
                      htmlFor={`cat-${option.value}`}
                      className={`
                        cursor-pointer block p-3 rounded-lg border-2 transition-all
                        ${formData.category === option.value
                          ? "border-primary bg-primary/10"
                          : "border-muted hover:border-muted-foreground/30"
                        }
                      `}
                    >
                      <div className="font-medium">{option.label}</div>
                      <div className="text-xs text-muted-foreground">{option.description}</div>
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </div>

            {/* Helpful Aspects */}
            <div className="space-y-4">
              <Label className="text-base font-semibold">
                5. What aspects of the governance system have been helpful? (Select all that apply)
              </Label>
              <CheckboxGroup
                options={HELPFUL_ASPECTS}
                selected={formData.helpfulAspects}
                onChange={(selected) => setFormData({ ...formData, helpfulAspects: selected })}
              />
            </div>

            {/* Pain Points */}
            <div className="space-y-4">
              <Label className="text-base font-semibold">
                6. What pain points have you experienced? (Select all that apply)
              </Label>
              <CheckboxGroup
                options={PAIN_POINTS}
                selected={formData.painPoints}
                onChange={(selected) => setFormData({ ...formData, painPoints: selected })}
              />
            </div>

            {/* Suggestions */}
            <div className="space-y-4">
              <Label htmlFor="suggestions" className="text-base font-semibold">
                7. Any suggestions for improvement?
              </Label>
              <Textarea
                id="suggestions"
                placeholder="Share your thoughts on how we can improve the governance system..."
                value={formData.suggestions}
                onChange={(e) => setFormData({ ...formData, suggestions: e.target.value })}
                rows={4}
              />
            </div>

            {/* Would Recommend */}
            <div className="space-y-4">
              <Label className="text-base font-semibold">
                8. Would you recommend proceeding to SOFT enforcement mode?
              </Label>
              <div className="flex gap-4">
                <Button
                  type="button"
                  variant={formData.wouldRecommend ? "default" : "outline"}
                  onClick={() => setFormData({ ...formData, wouldRecommend: true })}
                  className="flex-1"
                >
                  <ThumbsUp className="h-4 w-4 mr-2" />
                  Yes, proceed to SOFT mode
                </Button>
                <Button
                  type="button"
                  variant={!formData.wouldRecommend ? "destructive" : "outline"}
                  onClick={() => setFormData({ ...formData, wouldRecommend: false })}
                  className="flex-1"
                >
                  <ThumbsDown className="h-4 w-4 mr-2" />
                  No, extend WARNING mode
                </Button>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Submit */}
            <div className="flex justify-end gap-4 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => router.push("/app/governance/dogfooding")}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Submitting..." : "Submit Feedback"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

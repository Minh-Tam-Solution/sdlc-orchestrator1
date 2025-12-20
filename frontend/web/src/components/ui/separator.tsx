/**
 * Separator component (horizontal divider)
 * Simple implementation for visual separation between sections
 */

interface SeparatorProps {
  className?: string
}

export function Separator({ className = '' }: SeparatorProps) {
  return (
    <hr 
      className={`my-8 border-border ${className}`}
      role="separator" 
      aria-orientation="horizontal"
    />
  )
}

import type React from "react";
import { cn } from "@/lib/utils/cn";

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  options: { label: string; value: string }[];
}

export function Select({ className, options, ...props }: SelectProps) {
  return (
    <select
      className={cn(
        "flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary",
        className,
      )}
      {...props}
    >
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}

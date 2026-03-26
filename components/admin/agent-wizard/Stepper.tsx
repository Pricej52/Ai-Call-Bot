interface StepperProps {
  steps: string[];
  activeStep: number;
}

export function Stepper({ steps, activeStep }: StepperProps) {
  return (
    <ol className="grid gap-2 rounded-xl border border-slate-200 bg-white p-4 sm:grid-cols-4">
      {steps.map((label, index) => {
        const isActive = index === activeStep;
        const isComplete = index < activeStep;

        return (
          <li key={label} className="flex items-center gap-3 rounded-lg p-2">
            <span
              className={`inline-flex h-7 w-7 items-center justify-center rounded-full text-xs font-semibold ${
                isComplete
                  ? "bg-emerald-100 text-emerald-700"
                  : isActive
                    ? "bg-blue-100 text-blue-700"
                    : "bg-slate-100 text-slate-500"
              }`}
            >
              {index + 1}
            </span>
            <span className={`text-sm ${isActive ? "font-semibold text-slate-900" : "text-slate-500"}`}>
              {label}
            </span>
          </li>
        );
      })}
    </ol>
  );
}

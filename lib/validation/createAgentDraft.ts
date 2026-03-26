import { z } from "zod";

export const createAgentDraftSchema = z
  .object({
    type: z.object({
      directionType: z.enum(["inbound", "outbound"], {
        required_error: "Choose inbound or outbound.",
      }),
      displayName: z
        .string()
        .min(2, "Type name must be at least 2 characters.")
        .max(80, "Type name must be 80 characters or less."),
    }),
    agent: z.object({
      name: z
        .string()
        .min(2, "Agent name must be at least 2 characters.")
        .max(80, "Agent name must be 80 characters or less."),
      voiceProvider: z.enum(["elevenlabs", "openai", "system"]),
      voiceId: z.string().min(1, "Voice selection is required."),
      language: z.string().min(2, "Language is required."),
      timezone: z.string().min(2, "Timezone is required."),
    }),
    callFlow: z
      .object({
        greetingPrompt: z
          .string()
          .min(20, "Greeting prompt must be at least 20 characters."),
        systemPrompt: z
          .string()
          .min(40, "System prompt must be at least 40 characters."),
        fallbackPrompt: z
          .string()
          .min(10, "Fallback prompt must be at least 10 characters."),
        transferEnabled: z.boolean(),
        transferNumber: z.string().optional(),
        postCallSummaryEnabled: z.boolean(),
      })
      .superRefine((value, ctx) => {
        if (value.transferEnabled && !value.transferNumber) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ["transferNumber"],
            message: "Transfer number is required when transfer is enabled.",
          });
        }

        if (
          value.transferEnabled &&
          value.transferNumber &&
          !/^\+[1-9]\d{7,14}$/.test(value.transferNumber)
        ) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ["transferNumber"],
            message: "Enter transfer number in E.164 format (for example +14155550123).",
          });
        }
      }),
  })
  .strict();

export type CreateAgentDraftForm = z.infer<typeof createAgentDraftSchema>;

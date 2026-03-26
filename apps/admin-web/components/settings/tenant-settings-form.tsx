"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { saveTenantSettings } from "@/lib/api/admin-api";

const settingsSchema = z.object({
  tenantName: z.string().min(2, "Tenant name is required"),
  timezone: z.string().min(2, "Timezone is required"),
  supportEmail: z.string().email("Support email must be valid"),
});

type SettingsValues = z.infer<typeof settingsSchema>;

export function TenantSettingsForm() {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<SettingsValues>({
    resolver: zodResolver(settingsSchema),
    defaultValues: {
      tenantName: "",
      timezone: "UTC",
      supportEmail: "",
    },
  });

  return (
    <form
      className="space-y-4 rounded-lg border border-slate-200 bg-white p-6"
      onSubmit={handleSubmit(async (values) => {
        await saveTenantSettings(values);
        reset(values);
      })}
    >
      <div>
        <Label>Tenant Name</Label>
        <Input {...register("tenantName")} />
        <p className="mt-1 text-xs text-red-600">{errors.tenantName?.message}</p>
      </div>
      <div>
        <Label>Timezone</Label>
        <Input {...register("timezone")} />
        <p className="mt-1 text-xs text-red-600">{errors.timezone?.message}</p>
      </div>
      <div>
        <Label>Support Email</Label>
        <Input {...register("supportEmail")} />
        <p className="mt-1 text-xs text-red-600">{errors.supportEmail?.message}</p>
      </div>

      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Saving..." : "Save Settings"}
      </Button>
    </form>
  );
}

{{/*
Set apiVersion based on .Capabilities.APIVersions
*/}}
{{- define "rbacAPIVersion" -}}
{{- if .Capabilities.APIVersions.Has "rbac.authorization.k8s.io/v1beta1" -}}
rbac.authorization.k8s.io/v1beta1
{{- else if .Capabilities.APIVersions.Has "rbac.authorization.k8s.io/v1alpha1" -}}
rbac.authorization.k8s.io/v1alpha1
{{- else -}}
rbac.authorization.k8s.io/v1
{{- end -}}
{{- end -}}

{{/* Generate manager deployment envs */}}
{{- define "manager.envs" -}}
env:
- name: "TZ"
  value: "{{ .Values.time_zone | default "UTC" | quote }}"
- name: "ADMIN_USERNAME"
  value: "{{ .Values.admin_username | quote }}"
- name: "ADMIN_PASSWORD"
  value: "{{ .Values.admin_password | quote }}"
- name: "ADMIN_EMAIL"
  value: "{{ .Values.admin_email | quote }}"
{{- if eq .Values.global.database_location "off-cluster" }}
- name: DRYCC_DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: manager_db_url
{{- else if eq .Values.global.database_location "on-cluster"  }}
- name: DRYCC_DATABASE_USER
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: user
- name: DRYCC_DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: password
- name: DRYCC_DATABASE_NAME
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: manager_db_name
- name: DRYCC_DATABASE_URL
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@$(DRYCC_DATABASE_SERVICE_HOST):$(DRYCC_DATABASE_SERVICE_PORT)/$(DRYCC_DATABASE_NAME)"
{{- end }}
- name: WORKFLOW_NAMESPACE
  valueFrom:
    fieldRef:
    fieldPath: metadata.namespace
{{- range $key, $value := .Values.environment }}
- name: {{ $key }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}


{{/* Generate manager deployment limits */}}
{{- define "manager.limits" -}}
{{- if or (.Values.limits_cpu) (.Values.limits_memory) }}
resources:
  limits:
{{- if (.Values.limits_cpu) }}
    cpu: {{.Values.limits_cpu}}
{{- end }}
{{- if (.Values.limits_memory) }}
    memory: {{.Values.limits_memory}}
{{- end }}
{{- end }}
{{- end }}
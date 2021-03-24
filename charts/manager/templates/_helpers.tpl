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
# Environmental variable value for $INGRESS_CLASS
- name: "DRYCC_INGRESS_CLASS"
  value: "{{ .Values.global.ingress_class }}"
- name: "K8S_API_VERIFY_TLS"
  value: "{{ .Values.k8s_api_verify_tls }}"
- name: "KUBERNETES_CLUSTER_DOMAIN"
  value: "{{ .Values.global.cluster_domain }}"
- name: "TZ"
  value: {{ .Values.time_zone | default "UTC" | quote }}
{{- if eq .Values.global.database_location "off-cluster" }}
- name: DRYCC_DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: url
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
- name: DRYCC_DATABASE_URL
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@$(DRYCC_DATABASE_SERVICE_HOST):$(DRYCC_DATABASE_SERVICE_PORT)/$(DRYCC_DATABASE_USER)"
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
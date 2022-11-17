{{/*
Set apiVersion based on .Capabilities.APIVersions
*/}}

{{/* Generate manager deployment envs */}}
{{- define "manager.envs" }}
env:
- name: DRYCC_REDIS_ADDRS
  valueFrom:
    secretKeyRef:
      name: redis-creds
      key: addrs
- name: DRYCC_REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: redis-creds
      key: password
{{- if (.Values.databaseUrl) }}
- name: DRYCC_DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: database-url
{{- if (.Values.databaseReplicaUrl) }}
- name: DRYCC_DATABASE_REPLICA_URL
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: database-replica-url
{{- end }}
{{- else if eq .Values.global.databaseLocation "on-cluster"  }}
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
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@drycc-database.{{.Release.Namespace}}.svc.{{.Values.global.clusterDomain}}:5432/manager"
- name: DRYCC_DATABASE_REPLICA_URL
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@drycc-database-replica.{{.Release.Namespace}}.svc.{{.Values.global.clusterDomain}}:5432/manager"
{{- end }}
{{- if (.Values.rabbitmqUrl) }}
- name: DRYCC_RABBITMQ_URL
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: rabbitmq-url
{{- else if eq .Values.global.rabbitmqLocation "on-cluster" }}
- name: "DRYCC_RABBITMQ_USERNAME"
  valueFrom:
    secretKeyRef:
      name: rabbitmq-creds
      key: username
- name: "DRYCC_RABBITMQ_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: rabbitmq-creds
      key: password
- name: "DRYCC_RABBITMQ_URL"
  value: "amqp://$(DRYCC_RABBITMQ_USERNAME):$(DRYCC_RABBITMQ_PASSWORD)@drycc-rabbitmq.{{$.Release.Namespace}}.svc.{{$.Values.global.clusterDomain}}:5672/drycc"
{{- end }}
{{- if eq .Values.global.passportLocation "on-cluster"}}
- name: "DRYCC_PASSPORT_URL"
{{- if .Values.global.certManagerEnabled }}
  value: https://drycc-passport.{{ .Values.global.platformDomain }}
{{- else }}
  value: http://drycc-passport.{{ .Values.global.platformDomain }}
{{- end }}
- name: DRYCC_PASSPORT_KEY
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: drycc-passport-manager-key
- name: DRYCC_PASSPORT_SECRET
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: drycc-passport-manager-secret
{{- else }}
- name: DRYCC_PASSPORT_URL
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: passport-url
- name: DRYCC_PASSPORT_KEY
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: passport-key
- name: DRYCC_PASSPORT_SECRET
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: passport-secret
{{- end }}
- name: STRIPE_PUBLIC_KEY
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: stripe-public-key
- name: STRIPE_SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: stripe-secret-key
- name: STRIPE_WEBHOOK_SECRET
  valueFrom:
    secretKeyRef:
      name: manager-creds
      key: stripe-webhook-secret
{{- range $key, $value := .Values.environment }}
- name: {{ $key }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}

{{/* Generate manager deployment limits */}}
{{- define "manager.limits" -}}
{{- if or (.Values.limitsCpu) (.Values.limitsMemory) }}
resources:
  limits:
{{- if (.Values.limitsCpu) }}
    cpu: {{.Values.limitsCpu}}
{{- end }}
{{- if (.Values.limitsMemory) }}
    memory: {{.Values.limitsMemory}}
{{- end }}
{{- end }}
{{- end }}

{{/* Generate manager deployment volumeMounts */}}
{{- define "manager.volumeMounts" }}
volumeMounts:
  - name: manager-creds
    mountPath: /var/run/secrets/drycc/manager
    readOnly: true
  - name: manager-config
    mountPath: /etc/drycc/manager
    readOnly: true
{{- end }}


{{/* Generate manager deployment volumes */}}
{{- define "manager.volumes" }}
volumes:
  - name: manager-creds
    secret:
      secretName: manager-creds
  - name: manager-config
    configMap:
      name: manager-config
{{- end }}

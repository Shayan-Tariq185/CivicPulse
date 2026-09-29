# Phase 10 - Autoscaling evidence

Fill every blank from YOUR OWN captures. Never estimate or invent a number.

## Setup
- HPA: backend, min 2, max 10, CPU target 60%, scale-up immediate, scale-down window 300 s
- VPA: backend-vpa, updateMode Off (recommendations only)
- Load: `hey -z 3m -c 40` against `/api/v1/complaints` via the Ingress (rate limit raised for the test only)

## Baseline (before load)
- `kubectl top pods -n civicpulse` idle backend CPU per pod: ______ m
- Replicas: ______

## Load test #1 (original requests: cpu ____ m / memory ____ Mi)
- Load start: ______   Load end: ______
- Peak CPU % of request: ______
- Peak replicas: ______   Time to peak: ______ s
- Scale-up lag (load start -> first extra replica): ______ s
- Scale-down began: ______ s after load end
- hey summary: requests/sec ______, p95 latency ______, non-2xx ______

## VPA recommendation (`kubectl describe vpa backend-vpa -n civicpulse`)
| | CPU | Memory |
|---|---|---|
| Lower Bound | | |
| Target | | |
| Upper Bound | | |

## Change made
- Updated backend `requests` in `k8s/base/backend.yaml` from ______ to ______ because ______

## Load test #2 (new requests)
- Peak replicas: ______   Scale-up lag: ______ s
- What changed vs test #1 and why: ______

## Files saved
- docs/evidence/hpa-watch.txt, hey-output.txt, hpa-chart.png
- Screenshots: kubectl top, hpa watch mid-load, vpa describe

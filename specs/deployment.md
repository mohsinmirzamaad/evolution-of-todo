# Deployment Specification

## Phase IV — Local Kubernetes Deployment

## Objective
Deploy the Phase III Todo Chatbot on local Kubernetes using Minikube.

## Tech Stack
- Containerization: Docker
- Docker AI: Gordon
- Orchestration: Kubernetes (Minikube)
- Package Manager: Helm Charts
- AI DevOps: kubectl-ai

## Services to Deploy
1. backend — FastAPI + MCP + OpenAI Agents SDK (port 8000)
2. frontend — Next.js + ChatKit (port 3000)

## Environment Variables Required

### Backend
- DATABASE_URL
- BETTER_AUTH_SECRET
- OPENAI_API_KEY

### Frontend
- DATABASE_URL
- BETTER_AUTH_SECRET
- NEXT_PUBLIC_API_URL
- BETTER_AUTH_URL
- NEXT_PUBLIC_OPENAI_DOMAIN_KEY

## Helm Chart Structure
helm/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   └── secrets.yaml

## Deployment Steps
1. Build Docker images for frontend and backend
2. Load images into Minikube
3. Create Kubernetes secrets for env vars
4. Deploy using Helm charts
5. Verify pods are running
6. Access app via minikube service
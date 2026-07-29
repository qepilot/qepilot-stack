# 🚀 Deployment Guide

This project is configured for automatic deployment to Vercel from the `main` branch.

## GitHub Actions Setup

### Required Secrets

Add these secrets to your GitHub repository settings:

1. **VERCEL_TOKEN**: Your Vercel account token
   - Go to [Vercel Account Settings](https://vercel.com/account/tokens)
   - Create a new token with appropriate permissions
   - Add as `VERCEL_TOKEN` in GitHub Secrets

2. **VERCEL_ORG_ID**: Your Vercel organization ID
   - Run `vercel link` in your project
   - Copy the `orgId` from `.vercel/project.json`
   - Add as `VERCEL_ORG_ID` in GitHub Secrets

3. **VERCEL_PROJECT_ID**: Your Vercel project ID
   - Run `vercel link` in your project
   - Copy the `projectId` from `.vercel/project.json`
   - Add as `VERCEL_PROJECT_ID` in GitHub Secrets

### Getting the IDs

Run these commands in your project root:

```bash
# Link to Vercel project
vercel link

# Get your IDs from the generated file
cat .vercel/project.json
```

## Deployment Flow

- ✅ **Push to main** → Automatic production deploy to stack.qapilot.live
- ✅ **Other branches** → Manual deploy only (no auto-deploy)
- ✅ **Pull Requests** → No deployment

## Manual Deployment

For testing other branches:

```bash
# Deploy current branch to preview URL
vercel

# Deploy current branch to production
vercel --prod
```

## Domain Configuration

The main branch deploys to the custom domain: **stack.qapilot.live**

Configured in Vercel dashboard under Project Settings → Domains.
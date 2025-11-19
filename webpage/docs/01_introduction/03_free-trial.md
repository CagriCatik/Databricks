
# Databricks Free Trial and Community Edition Sign-Up Guide

This guide explains how to sign up for Databricks using either the **14-day full-featured free trial** (linked to a cloud provider) or the **Community Edition**, a lightweight single-user environment designed for individual learning and experimentation.

---

## Prerequisites

Before signing up:

- Active internet connection
- A personal or corporate email address
- (Optional) An AWS, Azure, or GCP account for Free Trial provisioning

---

## Free Trial Sign-Up (Cloud-Based Full Platform)

To create a fully functional workspace backed by a cloud provider:

1. Open a browser and visit:[https://databricks.com](https://databricks.com)
2. Click **Get started for free** at the top of the homepage.
3. Fill out the registration form:

- **First Name**: Your given name
- **Last Name**: Your surname
- **Company**: Your organization or enter `Personal`
- **Email Address**: Valid business or personal email
- **Title**: Your job title (e.g., Data Engineer)
- **Phone Number**: Optional
- **Country**: Select from dropdown

1. Click **Get started for free** to proceed.
2. Databricks provisions a 14-day trial workspace on your chosen cloud (AWS, Azure, or GCP).
3. Continue to the **Email Verification and Password Setup** section.

---

## Community Edition Sign-Up (Lightweight Personal Workspace)

The Community Edition offers a permanently free, simplified workspace for personal use.

1. Go to: [https://community.cloud.databricks.com](https://community.cloud.databricks.com)
   - Alternatively, click **Get started with Community Edition** on the main Databricks site.
2. Complete the CAPTCHA challenge to confirm you're human:
   - Match icons or solve as instructed
3. Submit the form to trigger the verification email.
    > **Note**: Community Edition does not require or link to an external cloud provider account.

---

## Email Verification and Password Setup

After submitting the registration:

1. Check your email inbox for a message from Databricks.
2. Click the verification link provided.
3. On the password setup screen:

- Enter a password meeting Databricks security requirements
- Re-enter to confirm
- Click **Set password** or **Reset password**

4. Once completed, the browser redirects to your new workspace.

---

## Accessing Your Workspace

- **Free Trial**: Use the workspace URL provided in the registration email (e.g., `https://<region>.azuredatabricks.net`).
- **Community Edition**: Return to: [https://community.cloud.databricks.com](https://community.cloud.databricks.com)
- Use your registered email and password to log in.

> **Tip**: Bookmark your workspace URL for future access.

---

## Comparison: Free Trial vs. Community Edition

| Feature                | Free Trial                               | Community Edition                  |
|------------------------|-------------------------------------------|------------------------------------|
| Duration               | 14 days                                   | Indefinite                         |
| Cloud Provider         | AWS, Azure, or GCP                        | Databricks-hosted                  |
| Support                | Email support, official docs              | Community forums only              |
| Cluster Configuration  | Full custom multi-node clusters           | Fixed single-node cluster          |
| Collaboration Features | Multi-user workspaces                     | Single-user only                   |

---

## Next Steps

- Launch a cluster and open a notebook.
- Start a tutorial on:
- Data ingestion using Auto Loader
- ETL with Delta Lake
- ML experiments with MLflow
- Continue with the next section: **Provisioning and Managing Clusters in Free Trial and Community Edition**.

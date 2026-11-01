# SuprSend

**Author:** adheshsuryatej
**Version:** 0.0.1
**Type:** tool
**Source:** https://github.com/ADHESHsuryatej/dify-plugin-suprsend

## Description

[SuprSend](https://www.suprsend.com) is notification infrastructure for product and dev teams: one API for email, SMS, push, in-app inbox, WhatsApp and Slack, with user preferences and batching built in.

This plugin lets Dify agents, chatflows and workflows send notifications and manage users in SuprSend.

## Tools

| Tool | What it does |
| --- | --- |
| **Trigger Workflow** | Sends a notification by triggering a SuprSend workflow for a user, with optional template data, emails, phone numbers and tenant. |
| **Create or Update User** | Creates or updates a user with name, emails, phone numbers, timezone and custom properties. |
| **Update User Preference** | Opts a user in or out of a notification category, optionally for one tenant. |
| **Add User to List** | Adds a user to a SuprSend subscriber list. |

## Setup

1. Sign up or log in at [app.suprsend.com](https://app.suprsend.com).
2. Go to **Developers > API Keys** and copy a key for the workspace you want to use (for example staging or production). The key decides which workspace the plugin acts on.
3. In Dify, install the SuprSend plugin, open **Tools > SuprSend > Authorize**, and paste the API key.

The plugin connects to `https://hub.suprsend.com` over HTTPS. No other setup is needed.

## Usage

- **Trigger Workflow** needs the workflow slug (SuprSend dashboard > Workflows) and the user's distinct ID. Pass template variables in **Data** as a JSON object, for example `{"order_id": "123"}`.
- **Update User Preference** needs a category slug (SuprSend dashboard > Notification Categories).
- **Add User to List** needs a list ID (SuprSend dashboard > Lists). Read-only lists such as All Subscribers can't be added to.
- Emails and phone numbers are comma-separated. Phone numbers use international format, for example `+14155550123`.

## Privacy

See [PRIVACY.md](PRIVACY.md).

## Support

- Docs: https://docs.suprsend.com
- Email: support@suprsend.com
- Source and issues: https://github.com/ADHESHsuryatej/dify-plugin-suprsend

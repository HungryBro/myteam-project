# n8n Workflows

This directory contains the n8n workflows (Cron Jobs) for the HungryBro/myteam-project.

## Workflows Overview

| Filename | Name | Schedule | Agent | Active | Discord Channel |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01-youtube-morning-scan.json` | Youtube Morning Scan | 07:00 ทุกวัน | Analyst | Yes | `#company_reports` |
| `02-morning-research.json` | Morning Research | 08:00 ทุกวัน | Analyst | Yes | `#company_reports` |
| `03-crypto-trade-execution.json` | Crypto Trade Execution | 09:00 ทุกวัน | Crypto Executor | No | `#crypto_trades` |
| `04-midday-scan.json` | Midday Scan | 14:00 ทุกวัน | Analyst | Yes | `#company_reports` |
| `05-youtube-evening-scan.json` | Youtube Evening Scan | 18:00 ทุกวัน | Analyst | Yes | `#company_reports` |
| `06-daily-summary.json` | Daily Summary | 20:00 ทุกวัน | Chief | Yes | `#company_reports` |
| `07-forex-asian-session.json` | Forex Asian Session | 06:00 จ-ศ | Forex Executor | Yes | `#forex_trades` |
| `08-forex-london-session.json` | Forex London Session | 14:00 จ-ศ | Forex Executor | Yes | `#forex_trades` |
| `09-forex-ny-session.json` | Forex NY Session | 19:00 จ-ศ | Forex Executor | Yes | `#forex_trades` |
| `10-forex-weekend-close.json` | Forex Weekend Close | 22:00 ศ | Forex Executor | Yes | `#forex_trades` |
| `11-weekly-review.json` | Weekly Review | 21:00 อา | Chief | Yes | `#company_reports` |
| `12-system-health-check.json` | System Health Check | ทุก 5 นาที | System | Yes | `#system_logs` |
| `13-openrouter-usage.json` | OpenRouter Usage Summary | 23:00 ทุกวัน | System | Yes | `#openrouter_setting` |
| `14-economic-calendar.json` | Economic Calendar | 06:00 ทุกวัน | Analyst | Yes | `#economic_calendar` |

## How to Import Workflows into n8n

1. Open your n8n instance in the browser.
2. Go to the **Workflows** section.
3. Click on **Add Workflow**.
4. In the top right corner, click on the **...** (Options) menu.
5. Select **Import from File**.
6. Choose the JSON file you want to import from this directory.
7. Once imported, you may need to configure the credentials for the HTTP Request and Discord Webhook nodes.
8. Save and activate the workflow.

## Workflow Structure

Each workflow is designed with the following structure:
- **Cron/Schedule Trigger node**: Triggers the workflow at the specified time.
- **HTTP Request node**: Calls the OpenClaw Gateway or other services to execute the agent's task.
- **Discord Webhook node**: Sends the result or notification to the appropriate Discord channel.

# AceDataCloudMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-acedatacloud -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-acedatacloud.svg)](https://pypi.org/project/mcp-acedatacloud/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for
**managing your [AceDataCloud](https://platform.acedata.cloud) account** through
the [platform management API](https://platform.acedata.cloud/documents/platform-token).

Check your balance, look up usage and spend, manage API keys, list services,
create and pay recharge orders, manage platform tokens, list models, and use
account permissions to edit and publish blogs or announcements — directly from
Claude, VS Code, Studio, or any MCP-compatible client.

> This is the **management / console** API (`platform.acedata.cloud`) — different
> from the data-generation MCP servers (Suno, Midjourney, …) that call
> `api.acedata.cloud`.

<!-- BEGIN GENERATED TOOL REFERENCE -->
## Tool Reference

### Account reads

| Tool | Description | Required permissions |
|------|-------------|----------------------|
| `acedatacloud_check_frame_ancestor` | Site Domains Frame | sites:read |
| `acedatacloud_check_site_domain` | Site Domains Check | sites:read |
| `acedatacloud_export_orders` | Export bounded order CSV. | orders:read |
| `acedatacloud_export_usage` | Export bounded usage CSV. | usage:read |
| `acedatacloud_get_access_grants_id` | Get access grants id. Backend account permissions and ownership checks apply. | access-control:read |
| `acedatacloud_get_access_policies_id` | Get access policies id. Backend account permissions and ownership checks apply. | access-control:read |
| `acedatacloud_get_access_request` | Access Detail | authenticated |
| `acedatacloud_get_access_requests_id` | Get access requests id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_admin_ace_snapshots_snapshot_id` | Get admin ace snapshots snapshot id. Backend account permissions and ownership checks apply. | ace-snapshot:read |
| `acedatacloud_get_admin_users_analytics` | Get admin users analytics. Backend account permissions and ownership checks apply. | users:read:any |
| `acedatacloud_get_announcements_admin_id` | Get announcements admin id. Backend account permissions and ownership checks apply. | announcements:read |
| `acedatacloud_get_announcements_unread_count` | Get announcements unread count. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_application` | Get one application and service details. | applications:read |
| `acedatacloud_get_applications_deployment_events` | Get applications deployment events. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_get_applications_deployment_logs` | Get applications deployment logs. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_get_applications_deployment_status` | Get applications deployment status. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_get_applications_id` | Get applications id. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_get_applications_recharge_card_eligibility` | Get applications recharge card eligibility. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_auto_recharge` | Get auto recharge. | auto-recharge:read |
| `acedatacloud_get_auto_recharge_configs_id` | Get auto recharge configs id. Backend account permissions and ownership checks apply. | auto-recharge:read |
| `acedatacloud_get_balance` | Summarize remaining Credits. | applications:read |
| `acedatacloud_get_blog_draft` | Read full editable blog source. | blog:read |
| `acedatacloud_get_blogs_admin_id` | Get blogs admin id. Backend account permissions and ownership checks apply. | blog:read |
| `acedatacloud_get_coin_infos_id` | Get coin infos id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_coin_wallet_summary` | Get coin wallet summary. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_configuration_capabilities_checks` | Get configuration capabilities checks. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_get_configuration_domains` | Get configuration domains. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_get_configuration_models_model` | Get configuration models model. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_get_configuration_providers_checks` | Get configuration providers checks. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_get_configuration_providers_pid` | Get configuration providers pid. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_get_configuration_summary` | Get configuration summary. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_get_content_reports_admin_id` | Get content reports admin id. Backend account permissions and ownership checks apply. | content-reports:read |
| `acedatacloud_get_credential` | Get one credential with secrets masked. | credentials:read |
| `acedatacloud_get_credentials_id` | Get credentials id. Backend account permissions and ownership checks apply. | credentials:read |
| `acedatacloud_get_deployment_events` | Get deployment scheduling events. | applications:read |
| `acedatacloud_get_deployment_logs` | Get bounded deployment logs. | applications:read |
| `acedatacloud_get_deployment_status` | Get live deployment status. | applications:read |
| `acedatacloud_get_distribution_cases_compensation_preview` | Get distribution cases compensation preview. Backend account permissions and ownership checks apply. | distribution-risk:read |
| `acedatacloud_get_distribution_cases_id` | Get distribution cases id. Backend account permissions and ownership checks apply. | distribution-risk:read |
| `acedatacloud_get_distribution_histories_id` | Get distribution histories id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_distribution_histories_platform_rank` | Get distribution histories platform rank. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_distribution_histories_rank` | Get distribution histories rank. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_distribution_histories_trend` | Get distribution histories trend. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_distribution_rank` | Distribution Rank | authenticated |
| `acedatacloud_get_distribution_redemptions_preview` | Get distribution redemptions preview. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_distribution_risk_bans_id` | Get distribution risk bans id. Backend account permissions and ownership checks apply. | distribution-risk:read |
| `acedatacloud_get_distribution_risk_bypasses_id` | Get distribution risk bypasses id. Backend account permissions and ownership checks apply. | distribution-risk:read |
| `acedatacloud_get_distribution_statuses_id` | Get distribution statuses id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_distribution_trend` | Distribution Trend | authenticated |
| `acedatacloud_get_email_audiences_profiles_user_id` | Get email audiences profiles user id. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_get_email_audiences_summary` | Get email audiences summary. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_get_email_campaigns_audience_candidates` | Get email campaigns audience candidates. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_get_email_campaigns_id` | Get email campaigns id. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_get_email_campaigns_preview` | Get email campaigns preview. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_get_email_campaigns_report` | Get email campaigns report. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_get_email_overview` | Get email overview. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_get_email_provider_health` | Get email provider health. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_get_feature_flags_evaluate` | Get feature flags evaluate. Backend account permissions and ownership checks apply. | feature-flags:read |
| `acedatacloud_get_feature_flags_id` | Get feature flags id. Backend account permissions and ownership checks apply. | feature-flags:read |
| `acedatacloud_get_feature_flags_scorecard` | Get feature flags scorecard. Backend account permissions and ownership checks apply. | feature-flags:read |
| `acedatacloud_get_invoice` | Get one invoice. | authenticated |
| `acedatacloud_get_invoice_download` | Get a signed invoice URL. | authenticated |
| `acedatacloud_get_invoices_admin_download` | Get invoices admin download. Backend account permissions and ownership checks apply. | invoices:read:any |
| `acedatacloud_get_invoices_admin_id` | Get invoices admin id. Backend account permissions and ownership checks apply. | invoices:read:any |
| `acedatacloud_get_invoices_admin_stats` | Get invoices admin stats. Backend account permissions and ownership checks apply. | invoices:read:any |
| `acedatacloud_get_invoices_download` | Get invoices download. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_invoices_id` | Get invoices id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_marketing_attribution_active_users` | Get marketing attribution active users. Backend account permissions and ownership checks apply. | marketing-attribution:read |
| `acedatacloud_get_marketing_attribution_analytics` | Get marketing attribution analytics. Backend account permissions and ownership checks apply. | marketing-attribution:read |
| `acedatacloud_get_marketing_attribution_summary` | Get marketing attribution summary. Backend account permissions and ownership checks apply. | marketing-attribution:read |
| `acedatacloud_get_order` | Get one order. | orders:read |
| `acedatacloud_get_order_discounts_id` | Get order discounts id. Backend account permissions and ownership checks apply. | order-discounts:read:any |
| `acedatacloud_get_order_invoice` | Get an order's active invoice. | authenticated |
| `acedatacloud_get_order_summary` | Summarize caller orders. | orders:read |
| `acedatacloud_get_orders_admin_context` | Get orders admin context. Backend account permissions and ownership checks apply. | orders:read:any |
| `acedatacloud_get_orders_export` | Get orders export. Backend account permissions and ownership checks apply. | orders:read |
| `acedatacloud_get_orders_invoice` | Get orders invoice. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_orders_payment_options` | Get orders payment options. Backend account permissions and ownership checks apply. | orders:read |
| `acedatacloud_get_orders_revenue_summary` | Get orders revenue summary. Backend account permissions and ownership checks apply. | revenue:read |
| `acedatacloud_get_orders_revenue_trend` | Get orders revenue trend. Backend account permissions and ownership checks apply. | revenue:read |
| `acedatacloud_get_orders_summary` | Get orders summary. Backend account permissions and ownership checks apply. | orders:read |
| `acedatacloud_get_platform_distribution_rank` | Distribution Platform_Rank | authenticated |
| `acedatacloud_get_platform_tokens_id` | Get platform tokens id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_platform_tokens_me` | Get platform tokens me. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_proxy_usage` | Get proxy usage detail. | usage:read |
| `acedatacloud_get_recharge_cards_allocations_id` | Get recharge cards allocations id. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_get_recharge_cards_allocations_wallet` | Get recharge cards allocations wallet. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_get_site` | Sites Detail | sites:read |
| `acedatacloud_get_site_banner` | Site Banners Detail | sites:read |
| `acedatacloud_get_site_banners_id` | Get site banners id. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_get_site_capability_override` | Site Capability Detail | sites:read |
| `acedatacloud_get_site_capability_overrides_id` | Get site capability overrides id. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_get_site_document_override` | Site Document Detail | sites:read |
| `acedatacloud_get_site_document_overrides_id` | Get site document overrides id. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_get_site_domain` | Site Domains Detail | sites:read |
| `acedatacloud_get_site_domains_id` | Get site domains id. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_get_site_home_sections_id` | Get site home sections id. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_get_site_service_override` | Site Service Detail | sites:read |
| `acedatacloud_get_site_service_overrides_id` | Get site service overrides id. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_get_sites_id` | Get sites id. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_get_survey` | Surveys Detail | authenticated |
| `acedatacloud_get_survey_response` | Surveys Response | authenticated |
| `acedatacloud_get_surveys_admin_templates_id` | Get surveys admin templates id. Backend account permissions and ownership checks apply. | surveys:read |
| `acedatacloud_get_surveys_responses_me` | Get surveys responses me. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_surveys_templates_alias` | Get surveys templates alias. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_translation_capabilities` | Translations Capabilities | authenticated |
| `acedatacloud_get_translations_capabilities` | Get translations capabilities. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_get_usage` | Get API usage detail. | usage:read |
| `acedatacloud_get_usage_apis_aggregate` | Get usage apis aggregate. Backend account permissions and ownership checks apply. | usage:read |
| `acedatacloud_get_usage_apis_export` | Get usage apis export. Backend account permissions and ownership checks apply. | usage:read |
| `acedatacloud_get_usage_apis_id` | Get usage apis id. Backend account permissions and ownership checks apply. | usage:read |
| `acedatacloud_get_usage_apis_status_codes` | Get usage apis status codes. Backend account permissions and ownership checks apply. | usage:read |
| `acedatacloud_get_usage_proxies_id` | Get usage proxies id. Backend account permissions and ownership checks apply. | usage:read |
| `acedatacloud_get_user_info` | Current authenticated account profile. | authenticated |
| `acedatacloud_get_wallet_summary` | Coin Wallet Summary | authenticated |
| `acedatacloud_get_webhook_subscriptions_id` | Get webhook subscriptions id. Backend account permissions and ownership checks apply. | webhooks:read |
| `acedatacloud_get_webhooks_id` | Get webhooks id. Backend account permissions and ownership checks apply. | webhooks:read |
| `acedatacloud_get_x402_authorization` | X402 Current | authenticated |
| `acedatacloud_get_x402_payment_authorization` | Get x402 payment authorization. Backend account permissions and ownership checks apply. | coin:read |
| `acedatacloud_list_access_grants` | List access grants. Backend account permissions and ownership checks apply. | access-control:read |
| `acedatacloud_list_access_policies` | List access policies. Backend account permissions and ownership checks apply. | access-control:read |
| `acedatacloud_list_access_requests` | Access List | authenticated |
| `acedatacloud_list_access_requests_detail` | List access requests. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_admin_ace_snapshots` | List admin ace snapshots. Backend account permissions and ownership checks apply. | ace-snapshot:read |
| `acedatacloud_list_admin_ace_snapshots_entries` | List admin ace snapshots entries. Backend account permissions and ownership checks apply. | ace-snapshot:read |
| `acedatacloud_list_announcements_admin` | List announcements admin. Backend account permissions and ownership checks apply. | announcements:read |
| `acedatacloud_list_applications` | List account subscriptions. | applications:read |
| `acedatacloud_list_applications_detail` | List applications. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_list_auto_recharge_configs` | List auto recharge configs. Backend account permissions and ownership checks apply. | auto-recharge:read |
| `acedatacloud_list_auto_recharges` | List auto-recharge configs. | auto-recharge:read |
| `acedatacloud_list_billing_profiles` | List billing profiles. | authenticated |
| `acedatacloud_list_billing_profiles_detail` | List billing profiles. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_blog_drafts` | List blog drafts and published editorial records. | blog:read |
| `acedatacloud_list_blogs_admin` | List blogs admin. Backend account permissions and ownership checks apply. | blog:read |
| `acedatacloud_list_coin_info` | Coin Info | authenticated |
| `acedatacloud_list_coin_infos` | List coin infos. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_coin_policies` | List coin policies. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_configuration_models` | List configuration models. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_list_configuration_models_v2` | List configuration models v2. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_list_configuration_providers` | List configuration providers. Backend account permissions and ownership checks apply. | provider-routing:read |
| `acedatacloud_list_content_reports_admin` | List content reports admin. Backend account permissions and ownership checks apply. | content-reports:read |
| `acedatacloud_list_credentials` | List API credentials with secrets masked. | credentials:read |
| `acedatacloud_list_credentials_detail` | List credentials. Backend account permissions and ownership checks apply. | credentials:read |
| `acedatacloud_list_distribution_histories` | List distribution histories. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_distribution_levels` | Distribution Levels | authenticated |
| `acedatacloud_list_distribution_levels_detail` | List distribution levels. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_distribution_redemptions` | List distribution redemptions. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_distribution_risk_bans` | List distribution risk bans. Backend account permissions and ownership checks apply. | distribution-risk:read |
| `acedatacloud_list_distribution_risk_bypasses` | List distribution risk bypasses. Backend account permissions and ownership checks apply. | distribution-risk:read |
| `acedatacloud_list_distribution_risk_histories` | List distribution risk histories. Backend account permissions and ownership checks apply. | distribution-risk:read |
| `acedatacloud_list_distribution_statuses` | List distribution statuses. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_distributions` | Get referral status. | authenticated |
| `acedatacloud_list_email_campaigns` | List email campaigns. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_list_email_campaigns_recipients` | List email campaigns recipients. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_list_email_events` | List email events. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_list_email_marketing_preferences` | List email marketing preferences. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_email_preferences` | Preferences List | authenticated |
| `acedatacloud_list_email_subscriptions` | List email subscriptions. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_list_email_suppressions` | List email suppressions. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_list_feature_flags` | List feature flags. Backend account permissions and ownership checks apply. | feature-flags:read |
| `acedatacloud_list_invoices` | List invoices. | authenticated |
| `acedatacloud_list_invoices_admin` | List invoices admin. Backend account permissions and ownership checks apply. | invoices:read:any |
| `acedatacloud_list_invoices_detail` | List invoices. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_models` | List OpenAI-compatible chat models. | authenticated |
| `acedatacloud_list_order_discounts` | List order discounts. Backend account permissions and ownership checks apply. | order-discounts:read:any |
| `acedatacloud_list_orders` | List recharge orders. | orders:read |
| `acedatacloud_list_orders_detail` | List orders. Backend account permissions and ownership checks apply. | orders:read |
| `acedatacloud_list_platform_tokens` | List management tokens with values masked. | authenticated |
| `acedatacloud_list_platform_tokens_detail` | List platform tokens. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_proxy_usage` | List proxy usage. | usage:read |
| `acedatacloud_list_recharge_cards_admin` | List recharge cards admin. Backend account permissions and ownership checks apply. | recharge-cards:read:any |
| `acedatacloud_list_recharge_cards_allocations` | List recharge cards allocations. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_list_site_banners` | Site Banners List | sites:read |
| `acedatacloud_list_site_banners_detail` | List site banners. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_list_site_capability_overrides` | Site Capability List | sites:read |
| `acedatacloud_list_site_capability_overrides_detail` | List site capability overrides. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_list_site_document_overrides` | Site Document List | sites:read |
| `acedatacloud_list_site_document_overrides_detail` | List site document overrides. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_list_site_domains` | Site Domains List | sites:read |
| `acedatacloud_list_site_domains_detail` | List site domains. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_list_site_home_sections` | List site home sections. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_list_site_service_overrides` | Site Service List | sites:read |
| `acedatacloud_list_site_service_overrides_detail` | List site service overrides. Backend account permissions and ownership checks apply. | sites:read |
| `acedatacloud_list_sites` | Sites List | sites:read |
| `acedatacloud_list_surveys` | Surveys List | authenticated |
| `acedatacloud_list_surveys_admin_responses` | List surveys admin responses. Backend account permissions and ownership checks apply. | surveys:read |
| `acedatacloud_list_surveys_admin_templates` | List surveys admin templates. Backend account permissions and ownership checks apply. | surveys:read |
| `acedatacloud_list_surveys_templates` | List surveys templates. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_list_usage` | List recent API usage records. | usage:read |
| `acedatacloud_list_usage_apis` | List usage apis. Backend account permissions and ownership checks apply. | usage:read |
| `acedatacloud_list_usage_proxies` | List usage proxies. Backend account permissions and ownership checks apply. | usage:read |
| `acedatacloud_list_usage_status_codes` | List usage status codes. | usage:read |
| `acedatacloud_list_webhook_subscriptions` | List webhook subscriptions. Backend account permissions and ownership checks apply. | webhooks:read |
| `acedatacloud_list_webhooks` | List webhooks. Backend account permissions and ownership checks apply. | webhooks:read |
| `acedatacloud_list_webhooks_events` | List webhooks events. Backend account permissions and ownership checks apply. | webhooks:read |
| `acedatacloud_preview_invoice` | Preview invoice amount. | authenticated |
| `acedatacloud_quote_auto_recharge` | Quote auto recharge. | auto-recharge:read |
| `acedatacloud_usage_summary` | Aggregate API spend by API. | usage:read |

### Catalog & docs

| Tool | Description | Required permissions |
|------|-------------|----------------------|
| `acedatacloud_get_api_spec` | Get one API's OpenAPI definition by path. | public |
| `acedatacloud_get_apis_id` | Get apis id. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_apis_usage` | Get apis usage. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_app_version` | Get app version. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_attribution_landing_inviter_id` | Get attribution landing inviter id. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_blog_post` | Read a localized published blog post. | public |
| `acedatacloud_get_blogs_slug` | Get blogs slug. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_coin_policies_id` | Get coin policies id. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_config` | Get config. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_datasets_id` | Get datasets id. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_distribution_risk` | Get distribution risk. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_distribution_risk_format` | Get distribution risk format. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_doc` | Fetch one documentation page by UUID. | public |
| `acedatacloud_get_documents_lookup_value` | Get documents lookup value. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_documents_openapi.json` | Get documents openapi.json. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_integrations_id` | Get integrations id. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_model` | Find models by ID or name. | public |
| `acedatacloud_get_models_catalog` | Get models catalog. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_models_introduction` | Get models introduction. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_models_slug` | Get models slug. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_orders_id` | Get orders id. Backend account permissions and ownership checks apply. | orders:read |
| `acedatacloud_get_pricing` | Get one service's display pricing. | public |
| `acedatacloud_get_recharge_cards_allocations_token` | Get recharge cards allocations token. Backend account permissions and ownership checks apply. | applications:read |
| `acedatacloud_get_search` | Get search. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_service` | Get one service by UUID or alias. | public |
| `acedatacloud_get_services_apis` | Get services apis. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_services_lookup_value` | Get services lookup value. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_services_proxies` | Get services proxies. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_site_domains_check` | Get site domains check. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_site_domains_frame_ancestors` | Get site domains frame ancestors. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_get_x402_solana_latest_blockhash` | Get x402 solana latest blockhash. Backend account permissions and ownership checks apply. | coin:read |
| `acedatacloud_list_announcements` | List published announcements. | public |
| `acedatacloud_list_announcements_detail` | List announcements. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_apis` | List API endpoints and billing metadata. | public |
| `acedatacloud_list_apis_detail` | List apis. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_blog_posts` | List published blog posts. | public |
| `acedatacloud_list_blogs` | List blogs. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_datasets` | List downloadable datasets. | public |
| `acedatacloud_list_datasets_detail` | List datasets. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_docs` | Browse documentation pages. | public |
| `acedatacloud_list_documents` | List documents. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_integrations` | List platform integrations. | public |
| `acedatacloud_list_integrations_detail` | List integrations. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_model_catalog` | List rich model metadata and pricing. | public |
| `acedatacloud_list_models_detail` | List models. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_services` | List or search available services. | public |
| `acedatacloud_list_services_detail` | List services. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_showcases` | List showcases. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_site_banners_public` | List site banners public. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_site_home_sections_public` | List site home sections public. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_list_sites_detail` | List sites. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_search_docs` | Search public documentation. | public |

### Writes

| Tool | Description | Required permissions |
|------|-------------|----------------------|
| `acedatacloud_apply_invoice` | Apply for an invoice. | authenticated |
| `acedatacloud_cancel_access_request` | Access Cancel | authenticated |
| `acedatacloud_cancel_invoice` | Cancel an invoice. | authenticated |
| `acedatacloud_confirm_auto_recharge_setup` | Confirm saved card setup. | auto-recharge:write |
| `acedatacloud_confirm_wallet_challenge` | Coin Wallet Confirm | authenticated |
| `acedatacloud_confirm_x402_authorization` | X402 Confirm | authenticated |
| `acedatacloud_confirm_x402_revocation` | X402 Revoke | authenticated |
| `acedatacloud_control_deployment` | Start a stopped deployment. | applications:write |
| `acedatacloud_create_access_grants` | Create access grants. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_create_access_grants_grandfather` | Create access grants grandfather. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_create_access_policies` | Create access policies. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_create_access_request` | Access Create | authenticated |
| `acedatacloud_create_access_requests` | Create access requests. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_access_requests_approve` | Create access requests approve. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_create_access_requests_reject` | Create access requests reject. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_create_admin_ace_snapshots_preview` | Create admin ace snapshots preview. Backend account permissions and ownership checks apply. | ace-snapshot:read |
| `acedatacloud_create_admin_ace_snapshots_publish` | Create admin ace snapshots publish. Backend account permissions and ownership checks apply. | ace-snapshot:publish |
| `acedatacloud_create_announcement` | Publish a platform announcement. | announcements:write |
| `acedatacloud_create_announcements_admin` | Create announcements admin. Backend account permissions and ownership checks apply. | announcements:write |
| `acedatacloud_create_announcements_admin_polish` | Create announcements admin polish. Backend account permissions and ownership checks apply. | announcements:write |
| `acedatacloud_create_announcements_admin_translate` | Create announcements admin translate. Backend account permissions and ownership checks apply. | announcements:write |
| `acedatacloud_create_announcements_read` | Create announcements read. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_announcements_read_all` | Create announcements read all. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_api_request_access_eligibility` | Create api request access eligibility. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_application` | Create an application subscription. | applications:write |
| `acedatacloud_create_applications` | Create applications. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_applications_deployment_deploy` | Create applications deployment deploy. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_applications_deployment_restart` | Create applications deployment restart. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_applications_deployment_save_config` | Create applications deployment save config. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_applications_deployment_start` | Create applications deployment start. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_applications_deployment_stop` | Create applications deployment stop. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_applications_deployment_teardown` | Create applications deployment teardown. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_applications_sponsor` | Create applications sponsor. Backend account permissions and ownership checks apply. | applications:write:any |
| `acedatacloud_create_applications_update_allow_consume_global` | Create applications update allow consume global. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_applications_update_disabled` | Create applications update disabled. Backend account permissions and ownership checks apply. | applications:write:any |
| `acedatacloud_create_applications_update_remaining_amount` | Create applications update remaining amount. Backend account permissions and ownership checks apply. | credits:write:any |
| `acedatacloud_create_attribution_resolve` | Create attribution resolve. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_create_auto_recharge` | Create auto recharge. | auto-recharge:write |
| `acedatacloud_create_auto_recharge_configs` | Create auto recharge configs. Backend account permissions and ownership checks apply. | auto-recharge:write |
| `acedatacloud_create_auto_recharge_configs_cancel_setup` | Create auto recharge configs cancel setup. Backend account permissions and ownership checks apply. | auto-recharge:write |
| `acedatacloud_create_auto_recharge_configs_confirm_setup` | Create auto recharge configs confirm setup. Backend account permissions and ownership checks apply. | auto-recharge:write |
| `acedatacloud_create_auto_recharge_configs_disable` | Create auto recharge configs disable. Backend account permissions and ownership checks apply. | auto-recharge:write |
| `acedatacloud_create_auto_recharge_configs_quote` | Create auto recharge configs quote. Backend account permissions and ownership checks apply. | auto-recharge:read |
| `acedatacloud_create_auto_recharge_configs_setup` | Create auto recharge configs setup. Backend account permissions and ownership checks apply. | auto-recharge:write |
| `acedatacloud_create_blog_draft` | Save an unpublished blog draft. | blog:write |
| `acedatacloud_create_blogs_admin` | Create blogs admin. Backend account permissions and ownership checks apply. | blog:write |
| `acedatacloud_create_card_fingerprints_action_name` | Create card fingerprints action name. Backend account permissions and ownership checks apply. | orders:write:any |
| `acedatacloud_create_coin_infos_update_balance` | Create coin infos update balance. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_coin_wallet_calculator` | Create coin wallet calculator. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_coin_wallet_challenge` | Create coin wallet challenge. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_coin_wallet_confirm` | Create coin wallet confirm. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_coin_wallet_unbind` | Create coin wallet unbind. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_configuration_providers` | Create configuration providers. Backend account permissions and ownership checks apply. | provider-routing:write |
| `acedatacloud_create_configuration_providers_capabilities` | Create configuration providers capabilities. Backend account permissions and ownership checks apply. | provider-routing:write |
| `acedatacloud_create_content_reports` | Create content reports. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_credential` | Create an API credential. | credentials:write |
| `acedatacloud_create_credentials` | Create credentials. Backend account permissions and ownership checks apply. | credentials:write |
| `acedatacloud_create_datasets_download` | Create datasets download. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_distribution_cases_compensate` | Create distribution cases compensate. Backend account permissions and ownership checks apply. | distribution-risk:write |
| `acedatacloud_create_distribution_cases_revert_compensation` | Create distribution cases revert compensation. Backend account permissions and ownership checks apply. | distribution-risk:write |
| `acedatacloud_create_distribution_redemptions_redeem` | Create distribution redemptions redeem. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_distribution_risk_bans` | Create distribution risk bans. Backend account permissions and ownership checks apply. | distribution-risk:write |
| `acedatacloud_create_distribution_risk_bans_revoke` | Create distribution risk bans revoke. Backend account permissions and ownership checks apply. | distribution-risk:write |
| `acedatacloud_create_distribution_risk_bypasses` | Create distribution risk bypasses. Backend account permissions and ownership checks apply. | distribution-risk:write |
| `acedatacloud_create_distribution_risk_bypasses_revoke` | Create distribution risk bypasses revoke. Backend account permissions and ownership checks apply. | distribution-risk:write |
| `acedatacloud_create_distribution_statuses_initialize` | Create distribution statuses initialize. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_distribution_statuses_update_level` | Create distribution statuses update level. Backend account permissions and ownership checks apply. | distribution:write:any |
| `acedatacloud_create_distribution_statuses_update_reward` | Create distribution statuses update reward. Backend account permissions and ownership checks apply. | distribution:write:any |
| `acedatacloud_create_email_audiences_candidates` | Create email audiences candidates. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_create_email_audiences_resolve` | Create email audiences resolve. Backend account permissions and ownership checks apply. | email-marketing:read |
| `acedatacloud_create_email_campaigns` | Create email campaigns. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_create_email_control` | Create email control. Backend account permissions and ownership checks apply. | email-marketing:send |
| `acedatacloud_create_email_provider_health` | Create email provider health. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_create_email_suppressions` | Create email suppressions. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_create_email_suppressions_deactivate` | Create email suppressions deactivate. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_create_feature_flags` | Create feature flags. Backend account permissions and ownership checks apply. | feature-flags:write |
| `acedatacloud_create_files` | Create files. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_invoices` | Create invoices. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_invoices_admin_file` | Create invoices admin file. Backend account permissions and ownership checks apply. | invoices:write:any |
| `acedatacloud_create_invoices_admin_upload_link` | Create invoices admin upload link. Backend account permissions and ownership checks apply. | invoices:write:any |
| `acedatacloud_create_invoices_cancel` | Create invoices cancel. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_invoices_preview` | Create invoices preview. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_logo_assets_analyze` | Create logo assets analyze. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_logo_assets_process` | Create logo assets process. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_order` | Create a recharge order. | orders:write |
| `acedatacloud_create_order_discounts` | Create order discounts. Backend account permissions and ownership checks apply. | order-discounts:write:any |
| `acedatacloud_create_orders` | Create orders. Backend account permissions and ownership checks apply. | orders:write |
| `acedatacloud_create_orders_admin_create` | Create orders admin create. Backend account permissions and ownership checks apply. | orders:write:any |
| `acedatacloud_create_orders_apple_verify` | Create orders apple verify. Backend account permissions and ownership checks apply. | orders:write |
| `acedatacloud_create_orders_distribution` | Create orders distribution. Backend account permissions and ownership checks apply. | distribution:write:any |
| `acedatacloud_create_orders_finish` | Create orders finish. Backend account permissions and ownership checks apply. | orders:write:any |
| `acedatacloud_create_orders_pay` | Create orders pay. Backend account permissions and ownership checks apply. | public |
| `acedatacloud_create_orders_refresh` | Create orders refresh. Backend account permissions and ownership checks apply. | orders:write |
| `acedatacloud_create_orders_refund` | Create orders refund. Backend account permissions and ownership checks apply. | orders:refund:any |
| `acedatacloud_create_orders_update_details` | Create orders update details. Backend account permissions and ownership checks apply. | orders:write:any |
| `acedatacloud_create_orders_update_price` | Create orders update price. Backend account permissions and ownership checks apply. | orders:write:any |
| `acedatacloud_create_payment_risk_holds_release` | Create payment risk holds release. Backend account permissions and ownership checks apply. | orders:refund:any |
| `acedatacloud_create_platform_token` | Create a management token. | authenticated |
| `acedatacloud_create_platform_tokens` | Create platform tokens. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_recharge_cards_admin_issue` | Create recharge cards admin issue. Backend account permissions and ownership checks apply. | recharge-cards:write:any |
| `acedatacloud_create_recharge_cards_allocations` | Create recharge cards allocations. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_recharge_cards_allocations_claim` | Create recharge cards allocations claim. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_recharge_cards_allocations_close` | Create recharge cards allocations close. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_recharge_cards_recipients_resolve` | Create recharge cards recipients resolve. Backend account permissions and ownership checks apply. | applications:write |
| `acedatacloud_create_recharge_cards_redeem` | Create recharge cards redeem. Backend account permissions and ownership checks apply. | recharge-cards:redeem |
| `acedatacloud_create_site_banner` | Site Banners Create | sites:write |
| `acedatacloud_create_site_banners` | Create site banners. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_site_capability_override` | Site Capability Create | sites:write |
| `acedatacloud_create_site_capability_overrides` | Create site capability overrides. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_site_document_override` | Site Document Create | sites:write |
| `acedatacloud_create_site_document_overrides` | Create site document overrides. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_site_domain` | Site Domains Create | sites:write |
| `acedatacloud_create_site_domains` | Create site domains. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_site_domains_verify` | Create site domains verify. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_site_home_sections` | Create site home sections. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_site_service_override` | Site Service Create | sites:write |
| `acedatacloud_create_site_service_overrides` | Create site service overrides. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_sites` | Create sites. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_sites_initialize` | Create sites initialize. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_sites_menu_translations` | Create sites menu translations. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_create_surveys_admin_templates` | Create surveys admin templates. Backend account permissions and ownership checks apply. | surveys:write |
| `acedatacloud_create_surveys_responses` | Create surveys responses. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_translations_disable` | Create translations disable. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_translations_enable` | Create translations enable. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_utils_share_images` | Create utils share images. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_create_wallet_challenge` | Coin Wallet Challenge | authenticated |
| `acedatacloud_create_webhook_subscriptions` | Create webhook subscriptions. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_create_webhooks` | Create webhooks. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_create_webhooks_test` | Create webhooks test. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_create_x402_payment_authorization_confirm` | Create x402 payment authorization confirm. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_create_x402_payment_authorization_disable` | Create x402 payment authorization disable. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_create_x402_payment_authorization_enable` | Create x402 payment authorization enable. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_create_x402_payment_authorization_revoke_confirm` | Create x402 payment authorization revoke confirm. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_create_x402_payment_authorization_revoke_setup` | Create x402 payment authorization revoke setup. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_create_x402_payment_authorization_setup` | Create x402 payment authorization setup. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_create_x402_transaction_prepare` | Create x402 transaction prepare. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_create_x402_transaction_status` | Create x402 transaction status. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_create_x402_transaction_submit` | Create x402 transaction submit. Backend account permissions and ownership checks apply. | coin:write |
| `acedatacloud_delete_access_grants_id` | Delete access grants id. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_delete_access_policies_id` | Delete access policies id. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_delete_access_requests_id` | Delete access requests id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_delete_admin_ace_snapshots_snapshot_id` | Delete admin ace snapshots snapshot id. Backend account permissions and ownership checks apply. | ace-snapshot:publish |
| `acedatacloud_delete_announcements_admin_id` | Delete announcements admin id. Backend account permissions and ownership checks apply. | announcements:write |
| `acedatacloud_delete_auto_recharge` | Delete auto recharge. | auto-recharge:write |
| `acedatacloud_delete_auto_recharge_configs_id` | Delete auto recharge configs id. Backend account permissions and ownership checks apply. | auto-recharge:write |
| `acedatacloud_delete_blog_post` | Delete a blog and its translations. | blog:write |
| `acedatacloud_delete_blogs_admin_id` | Delete blogs admin id. Backend account permissions and ownership checks apply. | blog:write |
| `acedatacloud_delete_configuration_capabilities_capability_id` | Delete configuration capabilities capability id. Backend account permissions and ownership checks apply. | provider-routing:write |
| `acedatacloud_delete_configuration_providers_pid` | Delete configuration providers pid. Backend account permissions and ownership checks apply. | provider-routing:write |
| `acedatacloud_delete_credential` | Revoke an API credential. | credentials:write |
| `acedatacloud_delete_credentials_id` | Delete credentials id. Backend account permissions and ownership checks apply. | credentials:write |
| `acedatacloud_delete_email_campaigns_id` | Delete email campaigns id. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_delete_feature_flags_id` | Delete feature flags id. Backend account permissions and ownership checks apply. | feature-flags:write |
| `acedatacloud_delete_order_discounts_id` | Delete order discounts id. Backend account permissions and ownership checks apply. | order-discounts:write:any |
| `acedatacloud_delete_platform_token` | Revoke a management token. | authenticated |
| `acedatacloud_delete_platform_tokens_id` | Delete platform tokens id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_delete_site_banner` | Site Banners Delete | sites:write |
| `acedatacloud_delete_site_banners_id` | Delete site banners id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_delete_site_capability_override` | Site Capability Delete | sites:write |
| `acedatacloud_delete_site_capability_overrides_id` | Delete site capability overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_delete_site_document_override` | Site Document Delete | sites:write |
| `acedatacloud_delete_site_document_overrides_id` | Delete site document overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_delete_site_domain` | Site Domains Delete | sites:write |
| `acedatacloud_delete_site_domains_id` | Delete site domains id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_delete_site_home_sections_id` | Delete site home sections id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_delete_site_service_override` | Site Service Delete | sites:write |
| `acedatacloud_delete_site_service_overrides_id` | Delete site service overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_delete_sites_id` | Delete sites id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_delete_surveys_admin_templates_id` | Delete surveys admin templates id. Backend account permissions and ownership checks apply. | surveys:write |
| `acedatacloud_delete_webhook_subscriptions_id` | Delete webhook subscriptions id. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_delete_webhooks_id` | Delete webhooks id. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_deploy_application` | Start or redeploy an application workload. | applications:write |
| `acedatacloud_disable_auto_recharge` | Disable auto recharge. | auto-recharge:write |
| `acedatacloud_disable_translation` | Translations Disable | authenticated |
| `acedatacloud_disable_x402_authorization` | X402 Disable | authenticated |
| `acedatacloud_enable_translation` | Translations Enable | authenticated |
| `acedatacloud_enable_x402_authorization` | X402 Enable | authenticated |
| `acedatacloud_get_webhooks_headers_name` | Get webhooks headers name. Backend account permissions and ownership checks apply. | webhooks:reveal |
| `acedatacloud_initialize_distribution` | Distribution Initialize | authenticated |
| `acedatacloud_initialize_site` | Sites Initialize | sites:write |
| `acedatacloud_pay_order` | Create an order payment session. | authenticated |
| `acedatacloud_publish_blog_post` | Publish now or schedule public visibility. | blog:write, blog:publish |
| `acedatacloud_refresh_coin_info` | Coin Refresh | authenticated |
| `acedatacloud_refresh_order` | Refresh payment state. | orders:write |
| `acedatacloud_replace_access_grants_id` | Replace access grants id. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_replace_access_policies_id` | Replace access policies id. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_replace_announcements_admin_id` | Replace announcements admin id. Backend account permissions and ownership checks apply. | announcements:write |
| `acedatacloud_replace_auto_recharge_configs_id` | Replace auto recharge configs id. Backend account permissions and ownership checks apply. | auto-recharge:write |
| `acedatacloud_replace_blogs_admin_id` | Replace blogs admin id. Backend account permissions and ownership checks apply. | blog:write |
| `acedatacloud_replace_content_reports_admin_id` | Replace content reports admin id. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_replace_credentials_id` | Replace credentials id. Backend account permissions and ownership checks apply. | credentials:write |
| `acedatacloud_replace_email_campaigns_id` | Replace email campaigns id. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_replace_email_marketing_preferences_topic` | Replace email marketing preferences topic. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_replace_feature_flags_id` | Replace feature flags id. Backend account permissions and ownership checks apply. | feature-flags:write |
| `acedatacloud_replace_order_discounts_id` | Replace order discounts id. Backend account permissions and ownership checks apply. | order-discounts:write:any |
| `acedatacloud_replace_site_banners_id` | Replace site banners id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_replace_site_capability_overrides_id` | Replace site capability overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_replace_site_document_overrides_id` | Replace site document overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_replace_site_domains_id` | Replace site domains id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_replace_site_home_sections_id` | Replace site home sections id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_replace_site_service_overrides_id` | Replace site service overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_replace_sites_id` | Replace sites id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_replace_surveys_admin_templates_id` | Replace surveys admin templates id. Backend account permissions and ownership checks apply. | surveys:write |
| `acedatacloud_replace_webhook_subscriptions_id` | Replace webhook subscriptions id. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_replace_webhooks_id` | Replace webhooks id. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_report_content` | Reports Create | authenticated |
| `acedatacloud_rotate_credential` | Rotate and disclose a credential secret once. | authenticated |
| `acedatacloud_run_email_campaigns_activate` | Run email campaigns activate. Backend account permissions and ownership checks apply. | email-marketing:send |
| `acedatacloud_run_email_campaigns_cancel` | Run email campaigns cancel. Backend account permissions and ownership checks apply. | email-marketing:send |
| `acedatacloud_run_email_campaigns_create_carryover` | Run email campaigns create carryover. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_run_email_campaigns_pause` | Run email campaigns pause. Backend account permissions and ownership checks apply. | email-marketing:send |
| `acedatacloud_run_email_campaigns_prepare` | Run email campaigns prepare. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_run_email_campaigns_prepare_carryover` | Run email campaigns prepare carryover. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_run_email_campaigns_preview_audience` | Run email campaigns preview audience. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_run_email_campaigns_release_next_wave` | Run email campaigns release next wave. Backend account permissions and ownership checks apply. | email-marketing:send |
| `acedatacloud_run_email_campaigns_resume` | Run email campaigns resume. Backend account permissions and ownership checks apply. | email-marketing:send |
| `acedatacloud_run_email_campaigns_retry_failed` | Run email campaigns retry failed. Backend account permissions and ownership checks apply. | email-marketing:send |
| `acedatacloud_run_email_campaigns_revise` | Run email campaigns revise. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_run_email_campaigns_send` | Run email campaigns send. Backend account permissions and ownership checks apply. | email-marketing:send |
| `acedatacloud_save_deployment_config` | Save a deployment configuration draft. | applications:write |
| `acedatacloud_set_site_menu_translation` | Sites Menu Translation | sites:write |
| `acedatacloud_setup_auto_recharge` | Create card setup state. | auto-recharge:write |
| `acedatacloud_setup_x402_authorization` | X402 Setup | authenticated |
| `acedatacloud_submit_survey` | Surveys Submit | authenticated |
| `acedatacloud_teardown_deployment` | Destroy a workload and delete its application. | applications:write |
| `acedatacloud_unpublish_blog_post` | Return a public blog post to draft. | blog:write, blog:publish |
| `acedatacloud_update_access_grants_id` | Update access grants id. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_update_access_policies_id` | Update access policies id. Backend account permissions and ownership checks apply. | access-control:write |
| `acedatacloud_update_announcements_admin_id` | Update announcements admin id. Backend account permissions and ownership checks apply. | announcements:write |
| `acedatacloud_update_application_balance_policy` | Update global-balance fallback policy. | applications:write |
| `acedatacloud_update_auto_recharge` | Update auto recharge. | auto-recharge:write |
| `acedatacloud_update_auto_recharge_configs_id` | Update auto recharge configs id. Backend account permissions and ownership checks apply. | auto-recharge:write |
| `acedatacloud_update_blog_post` | Edit draft or published blog source. | blog:write |
| `acedatacloud_update_blogs_admin_id` | Update blogs admin id. Backend account permissions and ownership checks apply. | blog:write |
| `acedatacloud_update_coin_wallet_visibility` | Update coin wallet visibility. Backend account permissions and ownership checks apply. | authenticated |
| `acedatacloud_update_configuration_capabilities_capability_id` | Update configuration capabilities capability id. Backend account permissions and ownership checks apply. | provider-routing:write |
| `acedatacloud_update_configuration_providers_pid` | Update configuration providers pid. Backend account permissions and ownership checks apply. | provider-routing:write |
| `acedatacloud_update_content_reports_admin_id` | Update content reports admin id. Backend account permissions and ownership checks apply. | content-reports:write |
| `acedatacloud_update_credential` | Update credential limits and API scope. | credentials:write |
| `acedatacloud_update_credentials_id` | Update credentials id. Backend account permissions and ownership checks apply. | credentials:write |
| `acedatacloud_update_email_campaigns_id` | Update email campaigns id. Backend account permissions and ownership checks apply. | email-marketing:write |
| `acedatacloud_update_email_preference` | Preferences Update | authenticated |
| `acedatacloud_update_feature_flags_id` | Update feature flags id. Backend account permissions and ownership checks apply. | feature-flags:write |
| `acedatacloud_update_invoices_admin_id` | Update invoices admin id. Backend account permissions and ownership checks apply. | invoices:write:any |
| `acedatacloud_update_order_discounts_id` | Update order discounts id. Backend account permissions and ownership checks apply. | order-discounts:write:any |
| `acedatacloud_update_recharge_cards_admin_id` | Update recharge cards admin id. Backend account permissions and ownership checks apply. | recharge-cards:write:any |
| `acedatacloud_update_site` | Sites Update | sites:write |
| `acedatacloud_update_site_banner` | Site Banners Update | sites:write |
| `acedatacloud_update_site_banners_id` | Update site banners id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_update_site_capability_override` | Site Capability Update | sites:write |
| `acedatacloud_update_site_capability_overrides_id` | Update site capability overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_update_site_document_override` | Site Document Update | sites:write |
| `acedatacloud_update_site_document_overrides_id` | Update site document overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_update_site_domain` | Site Domains Update | sites:write |
| `acedatacloud_update_site_domains_id` | Update site domains id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_update_site_home_sections_id` | Update site home sections id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_update_site_service_override` | Site Service Update | sites:write |
| `acedatacloud_update_site_service_overrides_id` | Update site service overrides id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_update_sites_id` | Update sites id. Backend account permissions and ownership checks apply. | sites:write |
| `acedatacloud_update_surveys_admin_templates_id` | Update surveys admin templates id. Backend account permissions and ownership checks apply. | surveys:write |
| `acedatacloud_update_webhook_subscriptions_id` | Update webhook subscriptions id. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_update_webhooks_id` | Update webhooks id. Backend account permissions and ownership checks apply. | webhooks:write |
| `acedatacloud_verify_apple_order` | Verify and fulfill Apple IAP. | orders:write |
| `acedatacloud_verify_site_domain` | Site Domains Verify | sites:write |

Calling a write/admin tool **without** `confirm=true` returns a redacted
dry-run preview and performs no HTTP request.

<!-- END GENERATED TOOL REFERENCE -->

## Quick Start

### Hosted OAuth

Connect to `https://mcp.acedata.cloud/mcp` with an OAuth-capable MCP client and
review the account capabilities shown on the authorization page:

| Tools | Requested scopes |
|---|---|
| Account profile, email, preferences | `profile:read`, `profile:write`, `email:read` |
| Subscriptions, balances, deployments | `applications:read`, `applications:write` |
| API keys | `credentials:read`, `credentials:write` |
| Usage and spend | `usage:read` |
| Orders, payment actions, invoices | `orders:read`, `orders:write`, `billing-profile:read` |
| Auto recharge | `auto-recharge:read`, `auto-recharge:write` |
| Platform tokens | `platform-tokens:read`, `platform-tokens:write` |
| Wallet and payment authorization | `coin:read`, `coin:write` |
| Referrals | `distribution:read` |
| Managed sites, domains, banners and overrides | `sites:read`, `sites:write` |

Documentation, service/pricing catalogs, API definitions and public model
catalogs are public reads and require no OAuth scope. Administrative tools
still require the account's existing backend roles and object/site access.

After consent, the hosted server reuses or creates a durable platform token.
Tool calls use that token and the account's current permissions; the OAuth
scope list describes consent and is not a scope ceiling stored on the platform
token. The token stays valid until revoked. Mutating tools retain their
`confirm=true` checks.

### 1. Get a platform token

Create one at [platform.acedata.cloud/console/platform-tokens](https://platform.acedata.cloud/console/platform-tokens).
It starts with `platform-` and never expires.

> Use a **platform token**, not the per-service `api.acedata.cloud` token — the
> latter returns 401 against the management API.

### 2. Install

```bash
pip install mcp-acedatacloud
```

### 3. Configure your client

**Claude Desktop / VS Code (stdio):**

```json
{
  "mcpServers": {
    "acedatacloud": {
      "command": "mcp-acedatacloud",
      "env": {
        "ACEDATACLOUD_PLATFORM_TOKEN": "platform-v1-xxxxxxxx"
      }
    }
  }
}
```

**Hosted (HTTP) — token per request:**

```json
{
  "mcpServers": {
    "acedatacloud": {
      "url": "https://mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer platform-v1-xxxxxxxx" }
    }
  }
}
```

## Example prompts

- "Draft a Chinese product blog in Markdown, show it for review, then save it."
- "Read blog draft `<id>` and publish it after I approve the content."
- "Schedule blog `<id>` for 2026-10-10T09:00:00+08:00."
- "How many credits do I have left?"
- "What did I spend on Suno in the last 7 days?"
- "List my API keys and show which ones have a spend cap."
- "Create a new API key on application `<id>` named ci." → previews, then run with confirm.
- "Top up application `<id>` with package `<id>` and give me the Stripe pay link."

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ACEDATACLOUD_PLATFORM_TOKEN` | — | **Required.** Platform token. |
| `PLATFORM_API_BASE_URL` | `https://platform.acedata.cloud` | Management API base. |
| `PLATFORM_REQUEST_TIMEOUT` | `30` | Request timeout (seconds). |
| `LOG_LEVEL` | `INFO` | Logging level. |

## Development

```bash
pip install -e ".[dev,test,http]"
pytest -m "not integration"      # unit tests
ruff check .                      # lint
mypy core tools                   # type-check
mcp-acedatacloud --transport http --port 8000
```

## Notes

- Amounts (`remaining_amount`, `used_amount`, totals) are in **Credits**, not USD.
- Newly created credential/platform tokens are returned in full **only once** —
  store them immediately.
- Credential rotation = delete + recreate (no in-place rotate endpoint).
- Blog editorial tools use `blog:read`, `blog:write`, and `blog:publish` permissions.
  Direct grants and permission groups work without making the account a superuser.
- Hosted OAuth resolves the signed-in account's canonical permissions dynamically.
  The consent page displays the actual scopes; accounts without blog grants receive none.
  Reconnect OAuth to review newly granted permissions. Existing durable platform tokens
  follow current account permissions, including revocations, on each request.
- Announcement tools require the corresponding account permission.

## Management API coverage

The checked-in route ledger in `contracts/management_surface.json` covers the
current Platform management API. Every business operation maps to a native typed
tool; callbacks, internal/device protocols, website asset delivery and methods
rejected by the backend have explicit exclusion reasons. Existing account tools
retain their subject-scoped queries. Administrative tools use the backend's
canonical permission names and ownership checks.

Hosted `tools/list` is filtered using the current platform credential's effective
permissions from `/platform-tokens/me/`. Deploy the Backend subject response and
the Auth consent changes before this MCP. File upload inputs and binary outputs
are Base64 artifacts bounded to 2 MiB; signed download links are returned directly.

To refresh the generated surface with the Backend runtime and then the MCP runtime:

```bash
<backend-python> scripts/export_platform_management.py --backend <PlatformBackend> --output /tmp/platform-routes.json
python scripts/compile_platform_management.py --input /tmp/platform-routes.json --backend <PlatformBackend>
```

Both scripts live at the monorepo root. The exporter uses synthetic configuration
and does not read a production .env or execute endpoint handlers.

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/acedatacloud-mcp)

## License

MIT — see [LICENSE](LICENSE).

# AceDataCloudMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-acedatacloud -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-acedatacloud.svg)](https://pypi.org/project/mcp-acedatacloud/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for
**managing your [AceDataCloud](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_readme_platform) account** through
the [platform management API](https://platform.acedata.cloud/documents/platform-token?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_readme_documents_platform-token).

Check your balance, look up usage and spend, manage API keys, list services,
create and pay recharge orders, manage platform tokens, list models, and use
account permissions to edit and publish blogs or announcements — directly from
Claude, VS Code, Studio, or any MCP-compatible client.

> This is the **management / console** API (`platform.acedata.cloud`) — different
> from the data-generation MCP servers (Suno, Midjourney, …) that call
> `api.acedata.cloud`.

<!-- BEGIN GENERATED TOOL REFERENCE -->
## Tool Reference

The default curated catalog advertises **348 tools** before
account-permission filtering, including `acedatacloud_get_usage_guide`.
The complete compatibility registry retains **519 tools**.
Discovery is grouped by business task, not by one tool per REST endpoint.

| Not advertised by default | Count |
|---------------------------|-------|
| alternate full-replacement update | 20 |
| client rendering, telemetry or protocol helper | 19 |
| duplicate native route | 128 |
| prefer the task-oriented catalog reader | 4 |

### Categories

| Category | Public | Account | Workspace | Admin |
|----------|--------|---------|-----------|-------|
| Account & API keys | 0 | 11 | 0 | 1 |
| Catalog & documentation | 19 | 2 | 0 | 0 |
| Applications & deployments | 0 | 13 | 0 | 4 |
| Usage & billing | 1 | 41 | 0 | 28 |
| Sites & branding | 1 | 0 | 38 | 0 |
| Community & wallet | 1 | 31 | 0 | 12 |
| Content & announcements | 4 | 0 | 19 | 0 |
| Email marketing & analytics | 0 | 0 | 0 | 37 |
| Access control & automation | 0 | 5 | 13 | 20 |
| Payment authorization | 0 | 10 | 0 | 0 |
| Administration & risk | 0 | 0 | 0 | 35 |
| Files & utilities | 0 | 1 | 0 | 0 |

Workspace tools cover delegated editing and site/webhook management.
Admin tools require their exact permission grants, not just an admin label.

### Account & API keys

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_create_credential` | Create an API credential. | account | credentials:write |
| `acedatacloud_create_platform_token` | Create a management token. | account | authenticated |
| `acedatacloud_delete_credential` | Revoke an API credential. | account | credentials:write |
| `acedatacloud_delete_platform_token` | Revoke a management token. | account | authenticated |
| `acedatacloud_get_credential` | Get one credential with secrets masked. | account | credentials:read |
| `acedatacloud_get_platform_tokens_id` | Get platform tokens id. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_get_user_info` | Current authenticated account profile. | account | authenticated |
| `acedatacloud_list_credentials` | List API credentials with secrets masked. | account | credentials:read |
| `acedatacloud_list_credentials_detail` | List credentials. Backend account permissions and ownership checks apply. | admin | credentials:read, credentials:write:any |
| `acedatacloud_list_platform_tokens` | List management tokens with values masked. | account | authenticated |
| `acedatacloud_rotate_credential` | Rotate and disclose a credential secret once. | account | authenticated |
| `acedatacloud_update_credential` | Update credential limits and API scope. | account | credentials:write |

### Catalog & documentation

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_create_datasets_download` | Create datasets download. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_get_api_spec` | Get one API's OpenAPI definition by path. | public | public |
| `acedatacloud_get_apis_id` | Get apis id. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_get_apis_usage` | Get apis usage. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_get_datasets_id` | Get datasets id. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_get_doc` | Fetch one documentation page by UUID. | public | public |
| `acedatacloud_get_documents_openapi.json` | Get documents openapi.json. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_get_integrations_id` | Get integrations id. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_get_model` | Find models by ID or name. | public | public |
| `acedatacloud_get_pricing` | Get one service's display pricing. | public | public |
| `acedatacloud_get_service` | Get one service by UUID or alias. | public | public |
| `acedatacloud_get_services_apis` | Get services apis. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_get_services_proxies` | Get services proxies. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_list_apis` | List API endpoints and billing metadata. | public | public |
| `acedatacloud_list_datasets` | List downloadable datasets. | public | public |
| `acedatacloud_list_docs` | Browse documentation pages. | public | public |
| `acedatacloud_list_integrations` | List platform integrations. | public | public |
| `acedatacloud_list_model_catalog` | List rich model metadata and pricing. | public | public |
| `acedatacloud_list_models` | List OpenAI-compatible chat models. | account | authenticated |
| `acedatacloud_list_services` | List or search available services. | public | public |
| `acedatacloud_search_docs` | Search public documentation. | public | public |

### Applications & deployments

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_control_deployment` | Start a stopped deployment. | account | applications:write |
| `acedatacloud_create_application` | Create an application subscription. | account | applications:write |
| `acedatacloud_create_applications_sponsor` | Create applications sponsor. Backend account permissions and ownership checks apply. | admin | applications:write:any |
| `acedatacloud_create_applications_update_disabled` | Create applications update disabled. Backend account permissions and ownership checks apply. | admin | applications:write:any |
| `acedatacloud_create_applications_update_remaining_amount` | Create applications update remaining amount. Backend account permissions and ownership checks apply. | admin | credits:write:any |
| `acedatacloud_deploy_application` | Start or redeploy an application workload. | account | applications:write |
| `acedatacloud_get_application` | Get one application and service details. | account | applications:read |
| `acedatacloud_get_applications_recharge_card_eligibility` | Get applications recharge card eligibility. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_get_balance` | Summarize remaining Credits. | account | applications:read |
| `acedatacloud_get_deployment_events` | Get deployment scheduling events. | account | applications:read |
| `acedatacloud_get_deployment_logs` | Get bounded deployment logs. | account | applications:read |
| `acedatacloud_get_deployment_status` | Get live deployment status. | account | applications:read |
| `acedatacloud_list_applications` | List account subscriptions. | account | applications:read |
| `acedatacloud_list_applications_detail` | List applications. Backend account permissions and ownership checks apply. | admin | applications:read, applications:read:any |
| `acedatacloud_save_deployment_config` | Save a deployment configuration draft. | account | applications:write |
| `acedatacloud_teardown_deployment` | Destroy a workload and delete its application. | account | applications:write |
| `acedatacloud_update_application_balance_policy` | Update global-balance fallback policy. | account | applications:write |

### Usage & billing

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_apply_invoice` | Apply for an invoice. | account | authenticated |
| `acedatacloud_cancel_invoice` | Cancel an invoice. | account | authenticated |
| `acedatacloud_confirm_auto_recharge_setup` | Confirm saved card setup. | account | auto-recharge:write |
| `acedatacloud_create_auto_recharge` | Create auto recharge. | account | auto-recharge:write |
| `acedatacloud_create_auto_recharge_configs_cancel_setup` | Create auto recharge configs cancel setup. Backend account permissions and ownership checks apply. | account | auto-recharge:write |
| `acedatacloud_create_card_fingerprints_action_name` | Create card fingerprints action name. Backend account permissions and ownership checks apply. | admin | orders:write:any |
| `acedatacloud_create_invoices_admin_file` | Create invoices admin file. Backend account permissions and ownership checks apply. | admin | invoices:write:any |
| `acedatacloud_create_invoices_admin_upload_link` | Create invoices admin upload link. Backend account permissions and ownership checks apply. | admin | invoices:write:any |
| `acedatacloud_create_order` | Create a recharge order. | account | orders:write |
| `acedatacloud_create_order_discounts` | Create order discounts. Backend account permissions and ownership checks apply. | admin | order-discounts:write:any |
| `acedatacloud_create_orders_admin_create` | Create orders admin create. Backend account permissions and ownership checks apply. | admin | orders:write:any |
| `acedatacloud_create_orders_distribution` | Create orders distribution. Backend account permissions and ownership checks apply. | admin | distribution:write:any |
| `acedatacloud_create_orders_finish` | Create orders finish. Backend account permissions and ownership checks apply. | admin | orders:write:any |
| `acedatacloud_create_orders_refund` | Create orders refund. Backend account permissions and ownership checks apply. | admin | orders:refund:any |
| `acedatacloud_create_orders_update_details` | Create orders update details. Backend account permissions and ownership checks apply. | admin | orders:write:any |
| `acedatacloud_create_orders_update_price` | Create orders update price. Backend account permissions and ownership checks apply. | admin | orders:write:any |
| `acedatacloud_create_recharge_cards_admin_issue` | Create recharge cards admin issue. Backend account permissions and ownership checks apply. | admin | recharge-cards:write:any |
| `acedatacloud_create_recharge_cards_allocations` | Create recharge cards allocations. Backend account permissions and ownership checks apply. | account | applications:write |
| `acedatacloud_create_recharge_cards_allocations_claim` | Create recharge cards allocations claim. Backend account permissions and ownership checks apply. | account | applications:write |
| `acedatacloud_create_recharge_cards_allocations_close` | Create recharge cards allocations close. Backend account permissions and ownership checks apply. | account | applications:write |
| `acedatacloud_create_recharge_cards_recipients_resolve` | Create recharge cards recipients resolve. Backend account permissions and ownership checks apply. | account | applications:write |
| `acedatacloud_create_recharge_cards_redeem` | Create recharge cards redeem. Backend account permissions and ownership checks apply. | account | recharge-cards:redeem |
| `acedatacloud_delete_auto_recharge` | Delete auto recharge. | account | auto-recharge:write |
| `acedatacloud_delete_order_discounts_id` | Delete order discounts id. Backend account permissions and ownership checks apply. | admin | order-discounts:write:any |
| `acedatacloud_disable_auto_recharge` | Disable auto recharge. | account | auto-recharge:write |
| `acedatacloud_export_orders` | Export bounded order CSV. | account | orders:read |
| `acedatacloud_export_usage` | Export bounded usage CSV. | account | usage:read |
| `acedatacloud_get_auto_recharge` | Get auto recharge. | account | auto-recharge:read |
| `acedatacloud_get_invoice` | Get one invoice. | account | authenticated |
| `acedatacloud_get_invoice_download` | Get a signed invoice URL. | account | authenticated |
| `acedatacloud_get_invoices_admin_download` | Get invoices admin download. Backend account permissions and ownership checks apply. | admin | invoices:read:any |
| `acedatacloud_get_invoices_admin_id` | Get invoices admin id. Backend account permissions and ownership checks apply. | admin | invoices:read:any |
| `acedatacloud_get_invoices_admin_stats` | Get invoices admin stats. Backend account permissions and ownership checks apply. | admin | invoices:read:any |
| `acedatacloud_get_order` | Get one order. | account | orders:read |
| `acedatacloud_get_order_discounts_id` | Get order discounts id. Backend account permissions and ownership checks apply. | admin | order-discounts:read:any |
| `acedatacloud_get_order_invoice` | Get an order's active invoice. | account | authenticated |
| `acedatacloud_get_order_summary` | Summarize caller orders. | account | orders:read |
| `acedatacloud_get_orders_admin_context` | Get orders admin context. Backend account permissions and ownership checks apply. | admin | orders:read:any |
| `acedatacloud_get_orders_payment_options` | Get orders payment options. Backend account permissions and ownership checks apply. | account | orders:read |
| `acedatacloud_get_orders_revenue_summary` | Get orders revenue summary. Backend account permissions and ownership checks apply. | admin | revenue:read |
| `acedatacloud_get_orders_revenue_trend` | Get orders revenue trend. Backend account permissions and ownership checks apply. | admin | revenue:read |
| `acedatacloud_get_proxy_usage` | Get proxy usage detail. | account | usage:read |
| `acedatacloud_get_recharge_cards_allocations_id` | Get recharge cards allocations id. Backend account permissions and ownership checks apply. | account | applications:read |
| `acedatacloud_get_recharge_cards_allocations_token` | Get recharge cards allocations token. Backend account permissions and ownership checks apply. | public | applications:read |
| `acedatacloud_get_recharge_cards_allocations_wallet` | Get recharge cards allocations wallet. Backend account permissions and ownership checks apply. | account | applications:read |
| `acedatacloud_get_usage` | Get API usage detail. | account | usage:read |
| `acedatacloud_list_auto_recharges` | List auto-recharge configs. | account | auto-recharge:read |
| `acedatacloud_list_billing_profiles` | List billing profiles. | account | authenticated |
| `acedatacloud_list_invoices` | List invoices. | account | authenticated |
| `acedatacloud_list_invoices_admin` | List invoices admin. Backend account permissions and ownership checks apply. | admin | invoices:read:any |
| `acedatacloud_list_order_discounts` | List order discounts. Backend account permissions and ownership checks apply. | admin | order-discounts:read:any |
| `acedatacloud_list_orders` | List recharge orders. | account | orders:read |
| `acedatacloud_list_orders_detail` | List orders. Backend account permissions and ownership checks apply. | admin | orders:read, orders:read:any |
| `acedatacloud_list_proxy_usage` | List proxy usage. | account | usage:read |
| `acedatacloud_list_recharge_cards_admin` | List recharge cards admin. Backend account permissions and ownership checks apply. | admin | recharge-cards:read:any |
| `acedatacloud_list_recharge_cards_allocations` | List recharge cards allocations. Backend account permissions and ownership checks apply. | account | applications:read |
| `acedatacloud_list_usage` | List recent API usage records. | account | usage:read |
| `acedatacloud_list_usage_apis` | List usage apis. Backend account permissions and ownership checks apply. | admin | usage:read, usage:read:any |
| `acedatacloud_list_usage_proxies` | List usage proxies. Backend account permissions and ownership checks apply. | admin | usage:read, usage:read:any |
| `acedatacloud_list_usage_status_codes` | List usage status codes. | account | usage:read |
| `acedatacloud_pay_order` | Create an order payment session. | account | authenticated |
| `acedatacloud_preview_invoice` | Preview invoice amount. | account | authenticated |
| `acedatacloud_quote_auto_recharge` | Quote auto recharge. | account | auto-recharge:read |
| `acedatacloud_refresh_order` | Refresh payment state. | account | orders:write |
| `acedatacloud_setup_auto_recharge` | Create card setup state. | account | auto-recharge:write |
| `acedatacloud_update_auto_recharge` | Update auto recharge. | account | auto-recharge:write |
| `acedatacloud_update_invoices_admin_id` | Update invoices admin id. Backend account permissions and ownership checks apply. | admin | invoices:write:any |
| `acedatacloud_update_order_discounts_id` | Update order discounts id. Backend account permissions and ownership checks apply. | admin | order-discounts:write:any |
| `acedatacloud_update_recharge_cards_admin_id` | Update recharge cards admin id. Backend account permissions and ownership checks apply. | admin | recharge-cards:write:any |
| `acedatacloud_usage_summary` | Aggregate API spend by API. | account | usage:read |

### Sites & branding

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_create_site_banner` | Site Banners Create | workspace | sites:write |
| `acedatacloud_create_site_capability_override` | Site Capability Create | workspace | sites:write |
| `acedatacloud_create_site_document_override` | Site Document Create | workspace | sites:write |
| `acedatacloud_create_site_domain` | Site Domains Create | workspace | sites:write |
| `acedatacloud_create_site_home_sections` | Create site home sections. Backend account permissions and ownership checks apply. | workspace | sites:write |
| `acedatacloud_create_site_service_override` | Site Service Create | workspace | sites:write |
| `acedatacloud_create_sites` | Create sites. Backend account permissions and ownership checks apply. | workspace | sites:write |
| `acedatacloud_delete_site_banner` | Site Banners Delete | workspace | sites:write |
| `acedatacloud_delete_site_capability_override` | Site Capability Delete | workspace | sites:write |
| `acedatacloud_delete_site_document_override` | Site Document Delete | workspace | sites:write |
| `acedatacloud_delete_site_domain` | Site Domains Delete | workspace | sites:write |
| `acedatacloud_delete_site_home_sections_id` | Delete site home sections id. Backend account permissions and ownership checks apply. | workspace | sites:write |
| `acedatacloud_delete_site_service_override` | Site Service Delete | workspace | sites:write |
| `acedatacloud_delete_sites_id` | Delete sites id. Backend account permissions and ownership checks apply. | workspace | sites:write |
| `acedatacloud_get_site` | Sites Detail | workspace | sites:read |
| `acedatacloud_get_site_banner` | Site Banners Detail | workspace | sites:read |
| `acedatacloud_get_site_capability_override` | Site Capability Detail | workspace | sites:read |
| `acedatacloud_get_site_document_override` | Site Document Detail | workspace | sites:read |
| `acedatacloud_get_site_domain` | Site Domains Detail | workspace | sites:read |
| `acedatacloud_get_site_home_sections_id` | Get site home sections id. Backend account permissions and ownership checks apply. | workspace | sites:read |
| `acedatacloud_get_site_service_override` | Site Service Detail | workspace | sites:read |
| `acedatacloud_initialize_site` | Sites Initialize | workspace | sites:write |
| `acedatacloud_list_site_banners` | Site Banners List | workspace | sites:read |
| `acedatacloud_list_site_capability_overrides` | Site Capability List | workspace | sites:read |
| `acedatacloud_list_site_document_overrides` | Site Document List | workspace | sites:read |
| `acedatacloud_list_site_domains` | Site Domains List | workspace | sites:read |
| `acedatacloud_list_site_home_sections` | List site home sections. Backend account permissions and ownership checks apply. | workspace | sites:read |
| `acedatacloud_list_site_home_sections_public` | List site home sections public. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_list_site_service_overrides` | Site Service List | workspace | sites:read |
| `acedatacloud_list_sites` | Sites List | workspace | sites:read |
| `acedatacloud_set_site_menu_translation` | Sites Menu Translation | workspace | sites:write |
| `acedatacloud_update_site` | Sites Update | workspace | sites:write |
| `acedatacloud_update_site_banner` | Site Banners Update | workspace | sites:write |
| `acedatacloud_update_site_capability_override` | Site Capability Update | workspace | sites:write |
| `acedatacloud_update_site_document_override` | Site Document Update | workspace | sites:write |
| `acedatacloud_update_site_domain` | Site Domains Update | workspace | sites:write |
| `acedatacloud_update_site_home_sections_id` | Update site home sections id. Backend account permissions and ownership checks apply. | workspace | sites:write |
| `acedatacloud_update_site_service_override` | Site Service Update | workspace | sites:write |
| `acedatacloud_verify_site_domain` | Site Domains Verify | workspace | sites:write |

### Community & wallet

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_confirm_wallet_challenge` | Coin Wallet Confirm | account | authenticated |
| `acedatacloud_create_coin_wallet_calculator` | Create coin wallet calculator. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_create_coin_wallet_unbind` | Create coin wallet unbind. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_create_distribution_redemptions_redeem` | Create distribution redemptions redeem. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_create_distribution_statuses_update_level` | Create distribution statuses update level. Backend account permissions and ownership checks apply. | admin | distribution:write:any |
| `acedatacloud_create_distribution_statuses_update_reward` | Create distribution statuses update reward. Backend account permissions and ownership checks apply. | admin | distribution:write:any |
| `acedatacloud_create_surveys_admin_templates` | Create surveys admin templates. Backend account permissions and ownership checks apply. | admin | surveys:write |
| `acedatacloud_create_wallet_challenge` | Coin Wallet Challenge | account | authenticated |
| `acedatacloud_delete_surveys_admin_templates_id` | Delete surveys admin templates id. Backend account permissions and ownership checks apply. | admin | surveys:write |
| `acedatacloud_disable_translation` | Translations Disable | account | authenticated |
| `acedatacloud_enable_translation` | Translations Enable | account | authenticated |
| `acedatacloud_get_coin_infos_id` | Get coin infos id. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_get_coin_policies_id` | Get coin policies id. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_get_content_reports_admin_id` | Get content reports admin id. Backend account permissions and ownership checks apply. | admin | content-reports:read |
| `acedatacloud_get_distribution_histories_id` | Get distribution histories id. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_get_distribution_rank` | Distribution Rank | account | authenticated |
| `acedatacloud_get_distribution_redemptions_preview` | Get distribution redemptions preview. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_get_distribution_statuses_id` | Get distribution statuses id. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_get_distribution_trend` | Distribution Trend | account | authenticated |
| `acedatacloud_get_platform_distribution_rank` | Distribution Platform_Rank | account | authenticated |
| `acedatacloud_get_survey` | Surveys Detail | account | authenticated |
| `acedatacloud_get_survey_response` | Surveys Response | account | authenticated |
| `acedatacloud_get_surveys_admin_templates_id` | Get surveys admin templates id. Backend account permissions and ownership checks apply. | admin | surveys:read |
| `acedatacloud_get_translation_capabilities` | Translations Capabilities | account | authenticated |
| `acedatacloud_get_wallet_summary` | Coin Wallet Summary | account | authenticated |
| `acedatacloud_initialize_distribution` | Distribution Initialize | account | authenticated |
| `acedatacloud_list_coin_info` | Coin Info | account | authenticated |
| `acedatacloud_list_coin_policies` | List coin policies. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_list_content_reports_admin` | List content reports admin. Backend account permissions and ownership checks apply. | admin | content-reports:read |
| `acedatacloud_list_distribution_levels` | Distribution Levels | account | authenticated |
| `acedatacloud_list_distribution_redemptions` | List distribution redemptions. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_list_distribution_statuses` | List distribution statuses. Backend account permissions and ownership checks apply. | admin | distribution:read:any |
| `acedatacloud_list_distributions` | Get referral status. | account | authenticated |
| `acedatacloud_list_email_preferences` | Preferences List | account | authenticated |
| `acedatacloud_list_surveys` | Surveys List | account | authenticated |
| `acedatacloud_list_surveys_admin_responses` | List surveys admin responses. Backend account permissions and ownership checks apply. | admin | surveys:read |
| `acedatacloud_list_surveys_admin_templates` | List surveys admin templates. Backend account permissions and ownership checks apply. | admin | surveys:read |
| `acedatacloud_refresh_coin_info` | Coin Refresh | account | authenticated |
| `acedatacloud_report_content` | Reports Create | account | authenticated |
| `acedatacloud_submit_survey` | Surveys Submit | account | authenticated |
| `acedatacloud_update_coin_wallet_visibility` | Update coin wallet visibility. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_update_content_reports_admin_id` | Update content reports admin id. Backend account permissions and ownership checks apply. | admin | content-reports:write |
| `acedatacloud_update_email_preference` | Preferences Update | account | authenticated |
| `acedatacloud_update_surveys_admin_templates_id` | Update surveys admin templates id. Backend account permissions and ownership checks apply. | admin | surveys:write |

### Content & announcements

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_approve_blog_post` | Approve a submitted version as a different account from its creator. | workspace | blog:read, blog:publish |
| `acedatacloud_create_announcement` | Publish a platform announcement. | workspace | announcements:write |
| `acedatacloud_create_announcements_admin_polish` | Create announcements admin polish. Backend account permissions and ownership checks apply. | workspace | announcements:write |
| `acedatacloud_create_announcements_admin_translate` | Create announcements admin translate. Backend account permissions and ownership checks apply. | workspace | announcements:write |
| `acedatacloud_create_blog_draft` | Save an unpublished blog draft. | workspace | blog:write |
| `acedatacloud_delete_announcements_admin_id` | Delete announcements admin id. Backend account permissions and ownership checks apply. | workspace | announcements:write |
| `acedatacloud_delete_blog_post` | Delete a blog and its translations. | workspace | blog:write |
| `acedatacloud_get_announcements_admin_id` | Get announcements admin id. Backend account permissions and ownership checks apply. | workspace | announcements:read |
| `acedatacloud_get_blog_draft` | Read full editable blog source. | workspace | blog:read |
| `acedatacloud_get_blog_post` | Read a localized published blog post. | public | public |
| `acedatacloud_list_announcements` | List published announcements. | public | public |
| `acedatacloud_list_announcements_admin` | List announcements admin. Backend account permissions and ownership checks apply. | workspace | announcements:read |
| `acedatacloud_list_blog_drafts` | List blog drafts and published editorial records. | workspace | blog:read |
| `acedatacloud_list_blog_posts` | List published blog posts. | public | public |
| `acedatacloud_list_showcases` | List showcases. Backend account permissions and ownership checks apply. | public | public |
| `acedatacloud_publish_blog_post` | Publish an approved draft now or schedule its public visibility. | workspace | blog:write, blog:publish |
| `acedatacloud_reject_blog_post` | Reject a submitted version with a reason. | workspace | blog:read, blog:publish |
| `acedatacloud_submit_blog_post` | Submit a draft or rejected post for review. | workspace | blog:write |
| `acedatacloud_unpublish_blog_post` | Return a public blog post to draft. | workspace | blog:write, blog:publish |
| `acedatacloud_update_announcements_admin_id` | Update announcements admin id. Backend account permissions and ownership checks apply. | workspace | announcements:write |
| `acedatacloud_update_blog_post` | Edit draft source; unpublish before changing public content. | workspace | blog:write |
| `acedatacloud_withdraw_blog_approval` | Withdraw approval before publication. | workspace | blog:read, blog:publish |
| `acedatacloud_withdraw_blog_submission` | Withdraw a pending review request. | workspace | blog:write |

### Email marketing & analytics

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_create_email_audiences_candidates` | Create email audiences candidates. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_create_email_audiences_resolve` | Create email audiences resolve. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_create_email_campaigns` | Create email campaigns. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_create_email_control` | Create email control. Backend account permissions and ownership checks apply. | admin | email-marketing:send |
| `acedatacloud_create_email_provider_health` | Create email provider health. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_create_email_suppressions` | Create email suppressions. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_create_email_suppressions_deactivate` | Create email suppressions deactivate. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_delete_email_campaigns_id` | Delete email campaigns id. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_get_email_audiences_profiles_user_id` | Get email audiences profiles user id. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_get_email_audiences_summary` | Get email audiences summary. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_get_email_campaigns_audience_candidates` | Get email campaigns audience candidates. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_get_email_campaigns_id` | Get email campaigns id. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_get_email_campaigns_preview` | Get email campaigns preview. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_get_email_campaigns_report` | Get email campaigns report. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_get_email_overview` | Get email overview. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_get_email_provider_health` | Get email provider health. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_get_marketing_attribution_active_users` | Get marketing attribution active users. Backend account permissions and ownership checks apply. | admin | marketing-attribution:read |
| `acedatacloud_get_marketing_attribution_analytics` | Get marketing attribution analytics. Backend account permissions and ownership checks apply. | admin | marketing-attribution:read |
| `acedatacloud_get_marketing_attribution_summary` | Get marketing attribution summary. Backend account permissions and ownership checks apply. | admin | marketing-attribution:read |
| `acedatacloud_list_email_campaigns` | List email campaigns. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_list_email_campaigns_recipients` | List email campaigns recipients. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_list_email_events` | List email events. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_list_email_subscriptions` | List email subscriptions. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_list_email_suppressions` | List email suppressions. Backend account permissions and ownership checks apply. | admin | email-marketing:read |
| `acedatacloud_run_email_campaigns_activate` | Run email campaigns activate. Backend account permissions and ownership checks apply. | admin | email-marketing:send |
| `acedatacloud_run_email_campaigns_cancel` | Run email campaigns cancel. Backend account permissions and ownership checks apply. | admin | email-marketing:send |
| `acedatacloud_run_email_campaigns_create_carryover` | Run email campaigns create carryover. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_run_email_campaigns_pause` | Run email campaigns pause. Backend account permissions and ownership checks apply. | admin | email-marketing:send |
| `acedatacloud_run_email_campaigns_prepare` | Run email campaigns prepare. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_run_email_campaigns_prepare_carryover` | Run email campaigns prepare carryover. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_run_email_campaigns_preview_audience` | Run email campaigns preview audience. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_run_email_campaigns_release_next_wave` | Run email campaigns release next wave. Backend account permissions and ownership checks apply. | admin | email-marketing:send |
| `acedatacloud_run_email_campaigns_resume` | Run email campaigns resume. Backend account permissions and ownership checks apply. | admin | email-marketing:send |
| `acedatacloud_run_email_campaigns_retry_failed` | Run email campaigns retry failed. Backend account permissions and ownership checks apply. | admin | email-marketing:send |
| `acedatacloud_run_email_campaigns_revise` | Run email campaigns revise. Backend account permissions and ownership checks apply. | admin | email-marketing:write |
| `acedatacloud_run_email_campaigns_send` | Run email campaigns send. Backend account permissions and ownership checks apply. | admin | email-marketing:send |
| `acedatacloud_update_email_campaigns_id` | Update email campaigns id. Backend account permissions and ownership checks apply. | admin | email-marketing:write |

### Access control & automation

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_cancel_access_request` | Access Cancel | account | authenticated |
| `acedatacloud_create_access_grants` | Create access grants. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_create_access_grants_grandfather` | Create access grants grandfather. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_create_access_policies` | Create access policies. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_create_access_request` | Access Create | account | authenticated |
| `acedatacloud_create_access_requests_approve` | Create access requests approve. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_create_access_requests_reject` | Create access requests reject. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_create_api_request_access_eligibility` | Create api request access eligibility. Backend account permissions and ownership checks apply. | account | authenticated |
| `acedatacloud_create_feature_flags` | Create feature flags. Backend account permissions and ownership checks apply. | admin | feature-flags:write |
| `acedatacloud_create_webhook_subscriptions` | Create webhook subscriptions. Backend account permissions and ownership checks apply. | workspace | webhooks:write |
| `acedatacloud_create_webhooks` | Create webhooks. Backend account permissions and ownership checks apply. | workspace | webhooks:write |
| `acedatacloud_create_webhooks_test` | Create webhooks test. Backend account permissions and ownership checks apply. | workspace | webhooks:write |
| `acedatacloud_delete_access_grants_id` | Delete access grants id. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_delete_access_policies_id` | Delete access policies id. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_delete_feature_flags_id` | Delete feature flags id. Backend account permissions and ownership checks apply. | admin | feature-flags:write |
| `acedatacloud_delete_webhook_subscriptions_id` | Delete webhook subscriptions id. Backend account permissions and ownership checks apply. | workspace | webhooks:write |
| `acedatacloud_delete_webhooks_id` | Delete webhooks id. Backend account permissions and ownership checks apply. | workspace | webhooks:write |
| `acedatacloud_get_access_grants_id` | Get access grants id. Backend account permissions and ownership checks apply. | admin | access-control:read |
| `acedatacloud_get_access_policies_id` | Get access policies id. Backend account permissions and ownership checks apply. | admin | access-control:read |
| `acedatacloud_get_access_request` | Access Detail | account | authenticated |
| `acedatacloud_get_feature_flags_evaluate` | Get feature flags evaluate. Backend account permissions and ownership checks apply. | admin | feature-flags:read |
| `acedatacloud_get_feature_flags_id` | Get feature flags id. Backend account permissions and ownership checks apply. | admin | feature-flags:read |
| `acedatacloud_get_feature_flags_scorecard` | Get feature flags scorecard. Backend account permissions and ownership checks apply. | admin | feature-flags:read |
| `acedatacloud_get_webhook_subscriptions_id` | Get webhook subscriptions id. Backend account permissions and ownership checks apply. | workspace | webhooks:read |
| `acedatacloud_get_webhooks_headers_name` | Get webhooks headers name. Backend account permissions and ownership checks apply. | workspace | webhooks:reveal |
| `acedatacloud_get_webhooks_id` | Get webhooks id. Backend account permissions and ownership checks apply. | workspace | webhooks:read |
| `acedatacloud_list_access_grants` | List access grants. Backend account permissions and ownership checks apply. | admin | access-control:read |
| `acedatacloud_list_access_policies` | List access policies. Backend account permissions and ownership checks apply. | admin | access-control:read |
| `acedatacloud_list_access_requests` | Access List | account | authenticated |
| `acedatacloud_list_feature_flags` | List feature flags. Backend account permissions and ownership checks apply. | admin | feature-flags:read |
| `acedatacloud_list_webhook_subscriptions` | List webhook subscriptions. Backend account permissions and ownership checks apply. | workspace | webhooks:read |
| `acedatacloud_list_webhooks` | List webhooks. Backend account permissions and ownership checks apply. | workspace | webhooks:read |
| `acedatacloud_list_webhooks_events` | List webhooks events. Backend account permissions and ownership checks apply. | workspace | webhooks:read |
| `acedatacloud_update_access_grants_id` | Update access grants id. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_update_access_policies_id` | Update access policies id. Backend account permissions and ownership checks apply. | admin | access-control:write |
| `acedatacloud_update_feature_flags_id` | Update feature flags id. Backend account permissions and ownership checks apply. | admin | feature-flags:write |
| `acedatacloud_update_webhook_subscriptions_id` | Update webhook subscriptions id. Backend account permissions and ownership checks apply. | workspace | webhooks:write |
| `acedatacloud_update_webhooks_id` | Update webhooks id. Backend account permissions and ownership checks apply. | workspace | webhooks:write |

### Payment authorization

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_confirm_x402_authorization` | X402 Confirm | account | authenticated |
| `acedatacloud_confirm_x402_revocation` | X402 Revoke | account | authenticated |
| `acedatacloud_create_x402_payment_authorization_revoke_setup` | Create x402 payment authorization revoke setup. Backend account permissions and ownership checks apply. | account | coin:write |
| `acedatacloud_create_x402_transaction_prepare` | Create x402 transaction prepare. Backend account permissions and ownership checks apply. | account | coin:write |
| `acedatacloud_create_x402_transaction_status` | Create x402 transaction status. Backend account permissions and ownership checks apply. | account | coin:write |
| `acedatacloud_create_x402_transaction_submit` | Create x402 transaction submit. Backend account permissions and ownership checks apply. | account | coin:write |
| `acedatacloud_disable_x402_authorization` | X402 Disable | account | authenticated |
| `acedatacloud_enable_x402_authorization` | X402 Enable | account | authenticated |
| `acedatacloud_get_x402_authorization` | X402 Current | account | authenticated |
| `acedatacloud_setup_x402_authorization` | X402 Setup | account | authenticated |

### Administration & risk

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_create_admin_ace_snapshots_preview` | Create admin ace snapshots preview. Backend account permissions and ownership checks apply. | admin | ace-snapshot:read |
| `acedatacloud_create_admin_ace_snapshots_publish` | Create admin ace snapshots publish. Backend account permissions and ownership checks apply. | admin | ace-snapshot:publish |
| `acedatacloud_create_configuration_providers` | Create configuration providers. Backend account permissions and ownership checks apply. | admin | provider-routing:write |
| `acedatacloud_create_configuration_providers_capabilities` | Create configuration providers capabilities. Backend account permissions and ownership checks apply. | admin | provider-routing:write |
| `acedatacloud_create_distribution_cases_compensate` | Create distribution cases compensate. Backend account permissions and ownership checks apply. | admin | distribution-risk:write |
| `acedatacloud_create_distribution_cases_revert_compensation` | Create distribution cases revert compensation. Backend account permissions and ownership checks apply. | admin | distribution-risk:write |
| `acedatacloud_create_distribution_risk_bans` | Create distribution risk bans. Backend account permissions and ownership checks apply. | admin | distribution-risk:write |
| `acedatacloud_create_distribution_risk_bans_revoke` | Create distribution risk bans revoke. Backend account permissions and ownership checks apply. | admin | distribution-risk:write |
| `acedatacloud_create_distribution_risk_bypasses` | Create distribution risk bypasses. Backend account permissions and ownership checks apply. | admin | distribution-risk:write |
| `acedatacloud_create_distribution_risk_bypasses_revoke` | Create distribution risk bypasses revoke. Backend account permissions and ownership checks apply. | admin | distribution-risk:write |
| `acedatacloud_create_payment_risk_holds_release` | Create payment risk holds release. Backend account permissions and ownership checks apply. | admin | orders:refund:any |
| `acedatacloud_delete_admin_ace_snapshots_snapshot_id` | Delete admin ace snapshots snapshot id. Backend account permissions and ownership checks apply. | admin | ace-snapshot:publish |
| `acedatacloud_delete_configuration_capabilities_capability_id` | Delete configuration capabilities capability id. Backend account permissions and ownership checks apply. | admin | provider-routing:write |
| `acedatacloud_delete_configuration_providers_pid` | Delete configuration providers pid. Backend account permissions and ownership checks apply. | admin | provider-routing:write |
| `acedatacloud_get_admin_ace_snapshots_snapshot_id` | Get admin ace snapshots snapshot id. Backend account permissions and ownership checks apply. | admin | ace-snapshot:read |
| `acedatacloud_get_admin_users_analytics` | Get admin users analytics. Backend account permissions and ownership checks apply. | admin | users:read:any |
| `acedatacloud_get_configuration_capabilities_checks` | Get configuration capabilities checks. Backend account permissions and ownership checks apply. | admin | provider-routing:read |
| `acedatacloud_get_configuration_domains` | Get configuration domains. Backend account permissions and ownership checks apply. | admin | provider-routing:read |
| `acedatacloud_get_configuration_models_model` | Get configuration models model. Backend account permissions and ownership checks apply. | admin | provider-routing:read |
| `acedatacloud_get_configuration_providers_checks` | Get configuration providers checks. Backend account permissions and ownership checks apply. | admin | provider-routing:read |
| `acedatacloud_get_configuration_providers_pid` | Get configuration providers pid. Backend account permissions and ownership checks apply. | admin | provider-routing:read |
| `acedatacloud_get_configuration_summary` | Get configuration summary. Backend account permissions and ownership checks apply. | admin | provider-routing:read |
| `acedatacloud_get_distribution_cases_compensation_preview` | Get distribution cases compensation preview. Backend account permissions and ownership checks apply. | admin | distribution-risk:read |
| `acedatacloud_get_distribution_cases_id` | Get distribution cases id. Backend account permissions and ownership checks apply. | admin | distribution-risk:read |
| `acedatacloud_get_distribution_risk_bans_id` | Get distribution risk bans id. Backend account permissions and ownership checks apply. | admin | distribution-risk:read |
| `acedatacloud_get_distribution_risk_bypasses_id` | Get distribution risk bypasses id. Backend account permissions and ownership checks apply. | admin | distribution-risk:read |
| `acedatacloud_list_admin_ace_snapshots` | List admin ace snapshots. Backend account permissions and ownership checks apply. | admin | ace-snapshot:read |
| `acedatacloud_list_admin_ace_snapshots_entries` | List admin ace snapshots entries. Backend account permissions and ownership checks apply. | admin | ace-snapshot:read |
| `acedatacloud_list_configuration_models` | List administrative model routing and health cards, including status, active provider, latency, check statistics and provider coverage. Supports q, status and provider filters. | admin | provider-routing:read |
| `acedatacloud_list_configuration_providers` | List configuration providers. Backend account permissions and ownership checks apply. | admin | provider-routing:read |
| `acedatacloud_list_distribution_risk_bans` | List distribution risk bans. Backend account permissions and ownership checks apply. | admin | distribution-risk:read |
| `acedatacloud_list_distribution_risk_bypasses` | List distribution risk bypasses. Backend account permissions and ownership checks apply. | admin | distribution-risk:read |
| `acedatacloud_list_distribution_risk_histories` | List distribution risk histories. Backend account permissions and ownership checks apply. | admin | distribution-risk:read |
| `acedatacloud_update_configuration_capabilities_capability_id` | Update configuration capabilities capability id. Backend account permissions and ownership checks apply. | admin | provider-routing:write |
| `acedatacloud_update_configuration_providers_pid` | Update configuration providers pid. Backend account permissions and ownership checks apply. | admin | provider-routing:write |

### Files & utilities

| Tool | Description | Audience | Required permissions |
|------|-------------|----------|----------------------|
| `acedatacloud_create_files` | Create files. Backend account permissions and ownership checks apply. | account | authenticated |

Calling a write/admin tool **without** `confirm=true` returns a redacted
dry-run preview and performs no HTTP request.

<!-- END GENERATED TOOL REFERENCE -->

## Connect to the account MCP

This is the **management** MCP at `https://mcp.acedata.cloud/mcp`. It uses a **platform token**, not the per-service `ACEDATACLOUD_API_TOKEN` used by generation MCPs. Choose one route:

| Route | Use it when | Credential |
|---|---|---|
| Hosted OAuth | Your MCP client supports remote OAuth | Add the URL only, sign in, and review the actual account permissions on the consent screen. DCR registers the client, not an API key. |
| Hosted platform token | Your client cannot complete OAuth or needs an explicit management credential | Send `Authorization: Bearer platform-…` in the client's HTTP header. |
| Local stdio | Your client launches local MCP processes | Install `mcp-acedatacloud` and set `ACEDATACLOUD_PLATFORM_TOKEN` for that process. |

Hosted OAuth reuses or creates a durable platform token. Review the consent screen for the account capabilities being requested; the account's current backend permissions still govern individual tools, and OAuth consent does not grant administrator access. Sensitive writes require their documented confirmation steps. Platform tokens are returned in full only when created; keep them private. [Platform token documentation](https://platform.acedata.cloud/documents/platform-token?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_readme_documents_platform-token).

### Hosted OAuth clients

- **Claude / Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Review consent. The Desktop local JSON file is a separate local-process mechanism. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user acedatacloud https://mcp.acedata.cloud/mcp`, then `claude mcp login acedatacloud`. Check `/mcp`. [Claude Code guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add `https://mcp.acedata.cloud/mcp` as a remote MCP server and finish browser sign-in. Personal config is `~/.cursor/mcp.json`; project config is `<project>/.cursor/mcp.json`. [Cursor guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter the URL, finish sign-in, and check **MCP: List Servers**. The VS Code workspace format is `<project>/.vscode/mcp.json`; its newer portable format is `<project>/.mcp.json`. [VS Code guide](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add acedatacloud --url https://mcp.acedata.cloud/mcp`, then `codex mcp login acedatacloud`. User settings live in `~/.codex/config.toml`. [Official Codex guide](https://developers.openai.com/codex/mcp/).

Cursor URL-only example:

```json
{"mcpServers":{"acedatacloud":{"url":"https://mcp.acedata.cloud/mcp"}}}
```

VS Code-specific workspace example:

```json
{"servers":{"acedatacloud":{"type":"http","url":"https://mcp.acedata.cloud/mcp"}}}
```

### Explicit platform token

Create a token at [AceDataCloud Platform](https://platform.acedata.cloud/console/platform-tokens?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_readme_platform_token). It begins with `platform-`. A per-service `api.acedata.cloud` token will fail against management actions. Do not paste a real token into a committed project file. An invalid fixed header will not fall back to OAuth in Claude Code.

For Claude Code, the shell expands the token when adding the server, so protect the saved user config:

```bash
export ACEDATACLOUD_PLATFORM_TOKEN='YOUR_PLATFORM_TOKEN'
claude mcp add --transport http --scope user acedatacloud https://mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_PLATFORM_TOKEN"
```

For a shared Claude Code project config, merge only the variable reference into `<project>/.mcp.json`; each user sets the environment variable independently:

```json
{
  "mcpServers": {
    "acedatacloud": {
      "type": "http",
      "url": "https://mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_PLATFORM_TOKEN}"}
    }
  }
}
```

Cursor uses `${env:ACEDATACLOUD_PLATFORM_TOKEN}` in `~/.cursor/mcp.json` or an uncommitted project config. In VS Code, **MCP: Open User Configuration** supports a masked `${input:platform-token}` value in the `headers` entry; keep that input in the user/workspace format rather than portable `.mcp.json`. [Cursor config](https://cursor.com/docs/mcp) · [VS Code config](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

### Local stdio

```bash
python -m pip install mcp-acedatacloud
export ACEDATACLOUD_PLATFORM_TOKEN='YOUR_PLATFORM_TOKEN'
mcp-acedatacloud
```

Claude Desktop's local-process config is opened from its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "acedatacloud": {
      "command": "uvx",
      "args": ["mcp-acedatacloud"],
      "env": {"ACEDATACLOUD_PLATFORM_TOKEN": "YOUR_PLATFORM_TOKEN"}
    }
  }
}
```

Keep the user-level file private. `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`. This is a local MCP process and is separate from Claude's remote connector.

### Verify permissions

A healthy MCP connection and tool list show that the client discovered the server. Start with a read such as `acedatacloud_get_user_info` or `acedatacloud_get_balance` to verify your account context. Catalog tools can be public reads; seeing them does not prove your platform token can perform account writes. Follow the confirmation flow for mutations and reread the result. For 401, check the token type or OAuth session; for 403, check the account's actual permission grant. Amounts are in Credits, not USD.

## Example prompts

- "Draft a Chinese product blog in Markdown, show it for review, then save it."
- "Submit blog draft `<id>` for review, then as a different account approve or reject it with a comment."
- "Publish the peer-approved blog draft `<id>` from a non-reviewer account."
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
- Blog categories are `product-updates`, `tech-sharing` (the draft default),
  `product-recommendations`, and `industry-insights`, or an existing administrator-defined
  slug. Legacy aliases `product`, `engineering`, `model-news`, and `comparison` are
  still accepted and normalized by the Backend.
- Category changes revoke draft approval. The category migration also pauses scheduled
  posts whose category changed; reread the draft and obtain fresh peer approval before
  publishing or rescheduling it.
- Blog publication requires a submitted draft approved by a different account with
  `blog:read` and `blog:publish`. Rejection requires a reason; approval may include a comment.
  The publisher must also differ from the reviewer. Read `review_version` before review;
  content edits revoke approval, and withdrawal returns a published post to draft.
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

### Discovery and compatibility

The default `ACEDATACLOUD_TOOL_PROFILE=curated` advertises task-oriented tools
instead of duplicate generated REST aliases, redundant PUT variants and web-client
helpers (rendering, read receipts, telemetry and protocol plumbing). It keeps
personal-account, site, editorial and administrative business workflows. The
usage guide lists only tools visible to the current credential.
Each advertised API tool also carries `acedatacloud/category` and
`acedatacloud/audience` metadata in its MCP `_meta` field.

Legacy names, arguments and routes remain callable for existing integrations;
hidden aliases are **not redirected** to another implementation. The complete
API coverage ledger and schema snapshot remain unchanged. Set
`ACEDATACLOUD_TOOL_PROFILE=full` explicitly for compatibility discovery or
diagnostics. This restores discovery only: permissions, ownership checks,
secret redaction and `confirm=true` requirements still apply.

Cross-account collection tools stay discoverable only with the matching
`:any` permission. Personal-account tools continue to scope queries to the
authenticated subject. An unrelated administrative permission never promotes
an account query into a cross-account query.

To refresh the generated surface with the Backend runtime and then the MCP runtime:

```bash
<backend-python> scripts/export_platform_management.py --backend <PlatformBackend> --output /tmp/platform-routes.json
python scripts/compile_platform_management.py --input /tmp/platform-routes.json --backend <PlatformBackend>
```

Both scripts live at the monorepo root. The exporter uses synthetic configuration
and does not read a production .env or execute endpoint handlers.

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/acedatacloud-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_readme_quick_start)

## License

MIT — see [LICENSE](LICENSE).

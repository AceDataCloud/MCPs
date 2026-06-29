package com.acedatacloud.mcp.acedatacloud

import com.intellij.notification.NotificationGroupManager
import com.intellij.notification.NotificationType
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.options.ShowSettingsUtil
import com.intellij.openapi.project.Project
import com.intellij.openapi.startup.ProjectActivity

class McpAcedatacloudStartupActivity : ProjectActivity {

    override suspend fun execute(project: Project) {
        val settings = McpAcedatacloudSettings.getInstance()
        if (settings.state.hasShownSetupNotification) return

        settings.state.hasShownSetupNotification = true

        val notification = NotificationGroupManager.getInstance()
            .getNotificationGroup("Ace Data Cloud MCP")
            .createNotification(
                "Ace Data Cloud MCP",
                "Configure your API token and set up AI Assistant MCP integration.",
                NotificationType.INFORMATION,
            )

        notification.addAction(object : AnAction("Open Settings") {
            override fun actionPerformed(e: AnActionEvent) {
                ShowSettingsUtil.getInstance()
                    .showSettingsDialog(project, McpAcedatacloudSettingsConfigurable::class.java)
                notification.expire()
            }
        })

        notification.notify(project)
    }
}

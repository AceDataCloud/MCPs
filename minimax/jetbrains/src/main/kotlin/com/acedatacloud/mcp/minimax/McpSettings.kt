package com.acedatacloud.mcp.minimax

import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage

@Service(Service.Level.APP)
@State(name = "McpSettings_minimax", storages = [Storage("McpMinimaxSettings.xml")])
class McpSettings : PersistentStateComponent<McpSettings.State> {

    data class State(
        var apiToken: String = "",
        var hasShownSetupNotification: Boolean = false
    )

    private var myState = State()

    override fun getState(): State = myState

    override fun loadState(state: State) {
        myState = state
    }

    companion object {
        fun getInstance(): McpSettings =
            ApplicationManager.getApplication().getService(McpSettings::class.java)
    }

    fun getStdioConfig(): String {
        val token = myState.apiToken.ifEmpty { "YOUR_API_TOKEN" }
        return """{"mcpServers": {"minimax": {"command": "uvx", "args": ["mcp-minimax"], "env": {"ACEDATACLOUD_API_TOKEN": "$token"}}}}"""
    }

    fun getHttpConfig(): String {
        val token = myState.apiToken.ifEmpty { "YOUR_API_TOKEN" }
        return """{"mcpServers": {"minimax": {"url": "https://minimax.mcp.acedata.cloud/mcp", "headers": {"Authorization": "Bearer $token"}}}}"""
    }
}

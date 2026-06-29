package com.acedatacloud.mcp.acedatacloud

import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage

@Service(Service.Level.APP)
@State(name = "McpAcedatacloudSettings", storages = [Storage("McpAcedatacloudSettings.xml")])
class McpAcedatacloudSettings : PersistentStateComponent<McpAcedatacloudSettings.State> {

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
        fun getInstance(): McpAcedatacloudSettings =
            ApplicationManager.getApplication().getService(McpAcedatacloudSettings::class.java)
    }

    fun getStdioConfig(): String {
        val token = myState.apiToken.ifEmpty { "YOUR_API_TOKEN" }
        return """{
  "mcpServers": {
    "acedatacloud": {
      "command": "uvx",
      "args": ["mcp-acedatacloud"],
      "env": {
        "ACEDATACLOUD_PLATFORM_TOKEN": "$token"
      }
    }
  }
}"""
    }

    fun getHttpConfig(): String {
        val token = myState.apiToken.ifEmpty { "YOUR_API_TOKEN" }
        return """{
  "mcpServers": {
    "acedatacloud": {
      "url": "https://mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer $token"
      }
    }
  }
}"""
    }
}

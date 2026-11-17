plugins {
    id("java")
    id("org.jetbrains.kotlin.jvm") version "2.1.20"
    id("org.jetbrains.intellij.platform") version "2.6.0"
}

group = providers.gradleProperty("pluginGroup").get()
version = providers.gradleProperty("pluginVersion").get()

kotlin {
    jvmToolchain(21)
}

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        create(providers.gradleProperty("platformType"), providers.gradleProperty("platformVersion"))
    }
}

intellijPlatform {
    pluginConfiguration {
        name = providers.gradleProperty("pluginName")
        version = providers.gradleProperty("pluginVersion")

        ideaVersion {
            sinceBuild = providers.gradleProperty("pluginSinceBuild")
        }
    }

    signing {
        certificateChain = providers.environmentVariable("CERTIFICATE_CHAIN")
        privateKey = providers.environmentVariable("PRIVATE_KEY")
        password = providers.environmentVariable("PRIVATE_KEY_PASSWORD")
    }

    publishing {
        token = providers.environmentVariable("PUBLISH_TOKEN")
        channels = providers.gradleProperty("pluginVersion")
            .map { listOf(it.substringAfter('-', "").substringBefore('.').ifEmpty { "default" }) }
    }

    pluginVerification {
        ides {
            recommended()
        }
    }
}

tasks {
    wrapper {
        gradleVersion = providers.gradleProperty("gradleVersion").get()
    }
}


// Brand bytes are generated from the immutable CDN asset, never stored in source.
val prepareOfficialBrandIcon by tasks.registering(Exec::class) {
    workingDir = rootProject.projectDir.parentFile
    commandLine("python3", "scripts/fetch_brand_assets.py", "--target", "jetbrains")
    inputs.file(rootProject.file("../brand-assets.json"))
    inputs.file(rootProject.file("../scripts/fetch_brand_assets.py"))
    outputs.files(
        rootProject.file("src/main/resources/META-INF/pluginIcon.png"),
        rootProject.file("src/main/resources/META-INF/pluginIcon.svg"),
        rootProject.file("src/main/resources/META-INF/pluginIcon_dark.svg"),
    )
}
tasks.named("processResources") { dependsOn(prepareOfficialBrandIcon) }

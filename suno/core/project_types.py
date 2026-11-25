"""Action-specific inputs for the public Suno Studio project API."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Identifier = Annotated[str, Field(min_length=1)]
NonNegative = Annotated[float, Field(ge=0)]
ProjectModel = Literal[
    "chirp-v3-5",
    "chirp-v4",
    "chirp-v4-5",
    "chirp-v4-5-plus",
    "chirp-v5",
    "chirp-v5-5",
    "chirp-v6",
    "chirp-v6-wild",
    "chirp-v6-mini",
]


class ProjectInput(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class CreateProject(ProjectInput):
    action: Literal["create"]
    title: str = Field(min_length=1, max_length=200)


class RetrieveProject(ProjectInput):
    action: Literal["retrieve"]
    id: Identifier


class SaveProject(ProjectInput):
    action: Literal["save"]
    id: Identifier
    state: dict[str, Any] = Field(
        description="Complete project state; preserve existing fields and tracks."
    )
    version_id: Identifier | None = Field(
        default=None, description="Latest version from retrieve; use it to detect conflicts."
    )
    title: str | None = None


class VersionedProject(ProjectInput):
    id: Identifier
    version_id: Identifier = Field(
        description="Latest project version; never silently replace a stale version."
    )


class AsyncProject(VersionedProject):
    async_: bool = Field(default=True, alias="async")
    callback_url: str | None = None


class UploadProjectAudio(AsyncProject):
    action: Literal["upload"]
    audio_url: str = Field(min_length=1)


class BeatRange(ProjectInput):
    start_beats: NonNegative | None = None
    end_beats: NonNegative | None = None

    @model_validator(mode="after")
    def validate_beat_range(self) -> "BeatRange":
        if self.end_beats is not None and self.end_beats <= (self.start_beats or 0):
            raise ValueError("end_beats must be greater than start_beats")
        return self


class AddProjectTrack(AsyncProject, BeatRange):
    action: Literal["add_track"]
    audio_id: Identifier
    name: str | None = None
    gain: NonNegative = 1
    title: str | None = None
    color: str | None = None


class SourceSection(AsyncProject):
    source_audio_id: Identifier
    model: ProjectModel
    start_seconds: NonNegative
    end_seconds: NonNegative
    title: str | None = None
    tags: str | None = None
    prompt: str | None = None
    negative_tags: str | None = None

    @model_validator(mode="after")
    def validate_seconds(self) -> "SourceSection":
        if self.end_seconds <= self.start_seconds:
            raise ValueError("end_seconds must be greater than start_seconds")
        return self


class GenerateProjectTrack(SourceSection):
    action: Literal["generate_track"]
    render_audio_id: Identifier = Field(
        description="Audio ID from a completed project render, not a URL."
    )
    stem_control_tags: str = Field(
        min_length=1, description="New part description, e.g. add Piano."
    )
    instrumental: bool = True
    vocal_gender: Literal["f", "m", "unspecified"] = "unspecified"


class ReplaceProjectSection(SourceSection):
    action: Literal["replace_section"]
    replacement_lyrics: str | None = None
    fixed: bool | None = None

    @model_validator(mode="after")
    def validate_fixed_range(self) -> "ReplaceProjectSection":
        if self.fixed and self.end_seconds - self.start_seconds >= 26:
            raise ValueError("fixed section must be shorter than 26 seconds")
        return self


class CommitProjectCandidate(AsyncProject, BeatRange):
    action: Literal["commit_candidate"]
    operation_id: Identifier
    candidate_id: Identifier
    track_id: Identifier
    name: str | None = None
    gain: NonNegative = 1


class RemoveProjectTrack(VersionedProject):
    action: Literal["remove_track"]
    track_id: Identifier


class RenderProject(AsyncProject, BeatRange):
    action: Literal["render"]
    title: str = Field(min_length=1)
    lyrics: str | None = None
    tags: str | None = None


SunoProjectRequest = Annotated[
    CreateProject
    | RetrieveProject
    | SaveProject
    | UploadProjectAudio
    | AddProjectTrack
    | GenerateProjectTrack
    | ReplaceProjectSection
    | CommitProjectCandidate
    | RemoveProjectTrack
    | RenderProject,
    Field(discriminator="action"),
]

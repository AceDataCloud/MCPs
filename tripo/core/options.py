"""Public Tripo processing options, flattened onto the service JSON body."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

GenerationModel = Literal[
    "v3.1-20260211", "v3.0-20250812", "v2.5-20250123", "P1-20260311", "P2-20260801"
]
Views = Annotated[list[str | None], Field(min_length=2, max_length=4)]
Prompt = Annotated[str, Field(min_length=1, max_length=1024)]
TaskIds = Annotated[list[str], Field(min_length=1, max_length=100)]
Motions = Annotated[list[str], Field(min_length=1, max_length=5)]
RigFormat = Literal["GLB", "FBX"]
ExportFormat = Literal["GLTF", "FBX", "USDZ", "OBJ", "STL", "3MF"]


class TextureOptions(BaseModel):
    """Optional settings for texture synthesis."""

    model_config = ConfigDict(extra="forbid")
    model: Literal["v2.5-20250123", "v3.0-20250812", "v3.5-20260815"] | None = None
    texture_alignment: Literal["original_image", "geometry"] | None = None
    pbr: bool | None = None
    texture_seed: int | None = None
    bake: bool | None = None
    delight: bool | None = None
    part_names: list[str] | None = None
    compress: Literal["geometry"] | None = None


class ConvertOptions(BaseModel):
    """Optional mesh, texture and export settings for format conversion."""

    model_config = ConfigDict(extra="forbid")
    quad: bool | None = None
    force_symmetry: bool | None = None
    face_limit: Annotated[int, Field(gt=0)] | None = None
    flatten_bottom: bool | None = None
    flatten_bottom_threshold: float | None = None
    texture_size: Annotated[int, Field(gt=0)] | None = None
    texture_format: Literal["JPEG", "PNG", "WEBP", "BMP"] | None = None
    bake: bool | None = None
    pack_uv: bool | None = None
    export_vertex_colors: bool | None = None
    pivot_to_center_bottom: bool | None = None
    scale_factor: Annotated[float, Field(gt=0)] | None = None
    with_animation: bool | None = None
    animate_in_place: bool | None = None
    part_names: list[str] | None = None
    export_orientation: Literal["+x", "-x", "+y", "-y"] | None = None
    fbx_preset: Literal["blender", "3dsmax", "mixamo", "bake_scale"] | None = None
    texture_packaging: Literal["embedded", "zip"] | None = None

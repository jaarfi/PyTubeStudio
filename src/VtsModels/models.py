"""
Contains all the data structure for the different requests you can send to VTS
"""

from typing import Literal, Optional, Annotated, Union, List
from pydantic import (
    BaseModel,
    ConfigDict,
    AliasGenerator,
    Field,
    field_validator,
    StringConstraints,
)
from pydantic.alias_generators import to_camel, to_snake

print(to_snake("authenticationToken"))


class _ModelRequests(BaseModel):
    """
    Base for all Data Structures
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_camel, validation_alias=to_snake
        ),
        protected_namespaces=[],
    )


class _ModelResponses(BaseModel):
    """
    Base for all Data Structures
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_snake, validation_alias=to_camel
        ),
        protected_namespaces=[],
    )


class BaseRequest(_ModelRequests):
    """
    The Base for all coming requests
    """

    api_name: str = "VTubeStudioPublicAPI"
    """Name of the API"""
    api_version: str = "1.0"
    """Version of the API"""
    request_id: str = "SomeID"
    """Id for the request, does not have to be unique"""
    message_type: str
    """Defining which request gets sent to VTubeStudio"""
    data: _ModelRequests | None
    """The data associated with the request type, some requests dont have any data"""


class BaseResponse(_ModelResponses):
    """
    The Base for all incoming responses
    """

    api_name: str
    """Name of the API"""
    api_version: str
    """Version of the API"""
    request_id: str = Field(validation_alias="requestID")
    """Id for the response, matches the provided ID when sending the request"""
    message_type: str
    """Defining which response this is, can be matched to the request messageType, every response can be an APIError"""
    data: _ModelRequests
    """The data associated with the response"""


class ErrorResponse(_ModelResponses):
    error_id: int = Field(validation_alias="errorID")
    message: str


class APIStateRequest(BaseRequest):
    """Request the current state of the API"""

    message_type: Literal["APIStateRequest"] = "APIStateRequest"
    data: None = None


class APIStateResponseData(_ModelResponses):
    active: bool
    v_tube_studio_version: str
    current_session_authenticated: bool


class APIStateResponse(BaseResponse):
    message_type: Literal["APIStateResponse", "APIError"]
    data: Union[APIStateResponseData, ErrorResponse]


class AuthenticationTokenRequestData(_ModelRequests):
    """
    Data structure for an AuthenticationTokenRequest
    """

    plugin_name: str = "PyTubeStudio"
    """Name of the Plugin"""
    plugin_developer: str = "twitch.tv/jaarfi"
    """Name of the Developer"""
    plugin_icon: str | None = None
    """optional: Base64 encoded PNG or JPG with exact dimensions of 128x128"""


class AuthenticationTokenRequest(BaseRequest):
    """
    Request an Authentication Token, this token is valid even after restarting the plugin or VTS.

    This will trigger a PopUp inside of VTubeStudio provided that Plugins are enabled.
    """

    message_type: Literal["AuthenticationTokenRequest"] = "AuthenticationTokenRequest"
    data: AuthenticationTokenRequestData = AuthenticationTokenRequestData()


class AuthenticationTokenResponseDataSuccesful(_ModelResponses):
    authentication_token: Annotated[str, StringConstraints(max_length=64)]
    """The auth token associated with this plugin. When provided with the plugin name and dev that requested it, it can be used to authotize a single session"""


class AuthenticationTokenResponse(BaseResponse):
    message_type: Literal["AuthenticationTokenResponse", "APIError"]
    data: Union[
        AuthenticationTokenResponseDataSuccesful,
        ErrorResponse,
    ]


class AuthenticationRequestData(_ModelRequests):
    """
    Data structure for an AuthenticationRequest
    """

    plugin_name: str = "PyTubeStudio"
    """Name of the Plugin, has to match the provided name upon requesting a token"""
    plugin_developer: str = "jaarfi"
    """Name of the Developer, has to match the provided dev upon requesting a token"""
    authentication_token: str
    """The authentication Token that a AuthenticationTokenRequest returned"""


class AuthenticationRequest(BaseRequest):
    """
    Request an Authentication for this session using a token, this has to be done once per session.

    Data has to match the data provided when requesting the token.
    """

    message_type: Literal["AuthenticationRequest"] = "AuthenticationRequest"
    data: AuthenticationRequestData


class AuthenticationResponseData(_ModelResponses):
    authenticated: bool
    reason: str


class AuthenticationResponse(BaseResponse):
    message_type: Literal["AuthenticationResponse", "APIError"]
    data: Union[AuthenticationResponseData, ErrorResponse]


class StatisticsRequest(BaseRequest):
    message_type: Literal["StatisticsRequest"] = "StatisticsRequest"
    data: None = None


class StatisticsResponseData(_ModelResponses):
    uptime: int
    framerate: int
    v_tube_studio_version: str
    allowed_plugins: int
    connected_plugins: int
    started_with_steam: bool
    window_width: int
    window_height: int
    window_is_fullscreen: bool


class StatisticsResponse(BaseResponse):
    message_type: Literal["StatisticsResponse"] = "StatisticsResponse"
    data: StatisticsResponseData


class VTSFolderInfoRequest(BaseRequest):
    message_type: Literal["VTSFolderInfoRequest"] = "VTSFolderInfoRequest"
    data: None = None


class VTSFolderInfoResponseData(_ModelResponses):
    models: str
    backgrounds: str
    items: str
    config: str
    logs: str
    backup: str


class VTSFolderInfoResponse(BaseResponse):
    message_type: Literal["VTSFolderInfoResponse"] = "VTSFolderInfoResponse"
    data: VTSFolderInfoResponseData


class CurrentModelRequest(BaseRequest):
    message_type: Literal["CurrentModelRequest"] = "CurrentModelRequest"
    data: None = None


class ModelPosition(_ModelResponses):
    position_x: float
    position_y: float
    rotation: float
    size: float


class CurrentModelResponseData(_ModelResponses):
    model_loaded: bool
    model_name: str
    model_id: str = Field(validation_alias="modelID")
    vts_model_name: str
    vts_model_icon_name: str
    live_2d_model_name: str = Field(validation_alias="live2DModelName")
    model_load_time: int
    """how long it takes to load this model"""
    time_since_model_loaded: int
    number_of_live_2d_parameters: int = Field(
        validation_alias="numberOfLive2DParameters"
    )
    number_of_live_2d_artmeshes: int = Field(validation_alias="numberOfLive2DArtmeshes")
    has_physics_file: bool
    number_of_textures: int
    texture_resolution: int
    model_position: ModelPosition


class CurrentModelResponse(BaseResponse):
    message_type: Literal["CurrentModelResponse"] = "CurrentModelResponse"
    data: CurrentModelResponseData


class AvailableModelsRequest(BaseRequest):
    message_type: Literal["AvailableModelsRequest"] = "AvailableModelsRequest"
    data: None = None


class SingleAvailableModel(_ModelResponses):
    model_loaded: bool
    model_name: str
    model_id: str = Field(validation_alias="modelID")
    vts_model_name: str
    vts_model_icon_name: str


class AvailableModelsResponseData(_ModelResponses):
    number_of_models: int
    available_models: Optional[List[SingleAvailableModel]]


class AvailableModelsResponse(BaseResponse):
    message_type: Literal["AvailableModelsResponse"] = "AvailableModelsResponse"
    data: AvailableModelsResponseData


class ModelLoadRequestData(_ModelRequests):
    model_id: str = Field(serialization_alias="modelID")
    """Unique Id of Model to load"""


class ModelLoadRequest(BaseRequest):
    message_type: Literal["ModelLoadRequest"] = "ModelLoadRequest"
    data: ModelLoadRequestData


class ModelLoadResponseData(_ModelResponses):
    model_id: str = Field(validation_alias="modelID")


class ModelLoadResponse(BaseResponse):
    message_type: Literal["ModelLoadResponse", "APIError"]
    data: Union[ModelLoadResponseData, ErrorResponse]


class MoveModelRequestData(_ModelRequests):
    time_in_seconds: float = Field(ge=0, le=2)
    """ 0 <= time_in_seconds <= 2
    The time the movement should take in seconds, if set to 0 the model will instantly appear in the new position"""
    values_are_relative_to_model: bool = False
    """If the values are relative to the model, they get added to the models current values, otherwise they are absolute"""
    position_x: Optional[float] = Field(default=None, ge=-1, le=1)
    """ -1 <= position_x <= 1
    0 positions the middle of the model in the middle of the x-axis, """
    position_y: Optional[float] = Field(default=None, ge=-1, le=1)
    """ -1 <= position_x <= 1
    0 positions the middle of the model in the middle of the y-axis, """
    rotation: Optional[float] = Field(default=None, ge=-360, le=360)
    """ -360 <= rotation <= 360
    Desired rotation in degrees, positive rotate clockwise, negative rotates counter-clockwise
    """
    size: Optional[float] = Field(default=-80, ge=-100, le=100)
    """The size the model should shrink/enlargen to, -80 is a fairly normal size (provided its absolute)"""


class MoveModelRequest(BaseRequest):
    message_type: Literal["MoveModelRequest"] = "MoveModelRequest"
    data: MoveModelRequestData


class EmptyData(_ModelResponses):
    class Config:
        extra = "forbid"


class MoveModelResponse(BaseResponse):
    message_type: Literal["MoveModelResponse", "APIError"]
    data: Union[EmptyData, ErrorResponse]


class HotkeysInCurrentModelRequestData(_ModelRequests):
    model_id: Optional[str] = Field(default=None, serialization_alias="modelID")
    """optional: if not provided, hotkeys for currently loaded model are returned"""

    live_2d_item_file_name: Optional[str] = Field(
        default=None, serialization_alias="live2DItemFileName"
    )
    """optional: return hotkeys for this live2d item instead, if this and modelid are provided, only modelid is used"""


class HotkeysInCurrentModelRequest(BaseRequest):
    message_type: Literal["HotkeysInCurrentModelRequest"] = (
        "HotkeysInCurrentModelRequest"
    )
    data: HotkeysInCurrentModelRequestData = HotkeysInCurrentModelRequestData()


class SingleAvailableHotkey(_ModelResponses):
    name: str
    type: str
    description: str
    file: str
    hotkey_id: str = Field(validation_alias="hotkeyID")
    key_combination: list
    on_screen_button_id: int = Field(validation_alias="onScreenButtonID")


class HotkeysInCurrentModelResponseData(_ModelResponses):
    model_loaded: bool
    model_name: str
    model_id: str = Field(validation_alias="modelID")
    available_hotkeys: List[SingleAvailableHotkey]


class HotkeysInCurrentModelResponse(BaseResponse):
    message_type: Literal["HotkeysInCurrentModelResponse"] = (
        "HotkeysInCurrentModelResponse"
    )
    data: HotkeysInCurrentModelResponseData


class HotkeyTriggerRequestData(_ModelRequests):
    hotkey_id: str = Field(serialization_alias="hotkeyID")
    """Either the unique id of the hotkey to be pressed or the hotkey name (case-insensitive). If 2 have the same name, the first one to show up in the UI will be executed"""
    item_instance_id: Optional[str] = Field(
        default=None, serialization_alias="itemInstanceID"
    )
    """optional: if left empty or not sent, hotkey is triggered for currently loaded model, if provided it triggers hotkey for item"""


class HotkeyTriggerRequest(BaseRequest):
    """
    Sends a Hotkey Trigger Request to VTS

    There is 5frame cooldown per hotkey
    If sent in rapid succession, they will get queued. Queuemax is 32 with 1 being triggered every 5 frames
    """

    message_type: Literal["HotkeyTriggerRequest"] = "HotkeyTriggerRequest"
    data: HotkeyTriggerRequestData


class HotkeyTriggerResponseData(_ModelResponses):
    hotkey_id: str = Field(validation_alias="hotkeyID")


class HotkeyTriggerResponse(BaseResponse):
    message_type: Literal["HotkeyTriggerResponse", "APIError"]
    data: Union[HotkeyTriggerResponseData, ErrorResponse]


class ExpressionStateRequestData(_ModelRequests):
    details: bool = True
    """request more details, specifically request usedInHotkeys and parameters"""
    expression_file: Optional[str] = None
    """optional: if provided, only data for that expression is returned, has to end in .exp3.json"""

    @field_validator("expression_file")
    @classmethod
    def must_be_expression_json(cls, v: str) -> str:
        if not v.endswith(".exp3.json"):
            raise ValueError("Not an expression File")
        return v


class ExpressionStateRequest(BaseRequest):
    message_type: Literal["ExpressionStateRequest"] = "ExpressionStateRequest"
    data: ExpressionStateRequestData = ExpressionStateRequestData()


class SingleUsedInHotkeys(_ModelResponses):
    name: str
    id: str


class ExpressionSingleParameter(_ModelResponses):
    name: str
    value: float


class SingleExpression(_ModelResponses):
    name: str
    file: str
    active: bool
    deactivate_when_key_is_let_go: bool
    auto_deactivate_after_seconds: bool
    seconds_remaining: int
    used_in_hotkeys: List[SingleUsedInHotkeys]
    parameters: List[ExpressionSingleParameter]


class ExpressionStateResponseData(_ModelResponses):
    model_loaded: bool
    model_name: str
    model_id: str = Field(validation_alias="modelID")
    expressions: List[SingleExpression]


class ExpressionStateResponse(BaseResponse):
    message_type: Literal["ExpressionStateResponse", "APIError"]
    data: Union[ExpressionStateResponseData, ErrorResponse]


class ExpressionActivationRequestData(_ModelRequests):
    expression_file: str
    """has to end in .exp3.json"""

    @field_validator("expression_file")
    @classmethod
    def must_be_expression_json(cls, v: str) -> str:
        if not v.endswith(".exp3.json"):
            raise ValueError("Not an expression File")
        return v

    active: bool


class ExpressionActivationRequest(BaseRequest):
    message_type: Literal["ExpressionActivationRequest"] = "ExpressionActivationRequest"
    data: ExpressionActivationRequestData


class ExpressionActivationResponse(BaseResponse):
    message_type: Literal["ExpressionActivationResponse", "APIError"]
    data: Union[EmptyData, ErrorResponse]


class ArtMeshListRequest(BaseRequest):
    message_type: Literal["ArtMeshListRequest"] = "ArtMeshListRequest"
    data: None = None


class ArtMeshListResponseData(_ModelResponses):
    model_loaded: bool
    number_of_art_mesh_names: int
    number_of_art_mesh_tags: int
    art_mesh_names: List[str]
    art_mesh_tags: List[str]


class ArtMeshListResponse(BaseResponse):
    message_type: Literal["ArtMeshListResponse"]
    data: ArtMeshListResponseData


class ColorTint(_ModelRequests):
    color_r: int = Field(default=255, ge=0, le=255)
    """0 <= color_r <= 255, 255 for no tinting"""
    color_g: int = Field(default=255, ge=0, le=255)
    """0 <= color_g <= 255, 255 for no tinting"""
    color_b: int = Field(default=255, ge=0, le=255)
    """0 <= color_b <= 255, 255 for no tinting"""
    color_a: int = Field(default=255, ge=0, le=255)
    """0 <= color_a <= 255, 255 for no tinting"""
    mix_with_scene_lighting_color: Optional[float] = Field(default=1, ge=0, le=1)
    """1 will completely overwrite the current color"""


class ArtMeshMatcher(_ModelRequests):
    tint_all: bool = False
    art_mesh_number: Optional[List[int]] = None
    name_exact: Optional[List[str]] = None
    name_contains: Optional[List[str]] = None
    tag_exact: Optional[List[str]] = None
    tag_contains: Optional[List[str]] = None


class ColorTintRequestData(_ModelRequests):
    color_tint: ColorTint = ColorTint()
    art_mesh_matcher: ArtMeshMatcher = ArtMeshMatcher()


class ColorTintRequest(BaseRequest):
    message_type: Literal["ColorTintRequest"] = "ColorTintRequest"
    data: ColorTintRequestData = ColorTintRequestData()


class ColorTintResponseData(_ModelResponses):
    matched_art_meshes: int


class ColorTintResponse(BaseResponse):
    message_type: Literal["ColorTintResponse", "APIError"]
    data: Union[ColorTintResponseData, ErrorResponse]


class SceneColorOverlayInfoRequest(BaseRequest):
    message_type: Literal["SceneColorOverlayInfoRequest"] = (
        "SceneColorOverlayInfoRequest"
    )
    data: None = None


class CapturePart(_ModelResponses):
    active: bool
    color_r: int
    color_g: int
    color_b: int


class SceneColorOverlayInfoResponseData(_ModelResponses):
    active: bool
    items_included: bool
    is_window_capture: bool
    base_brightness: int
    color_boost: int
    smoothing: int
    color_overlay_r: int
    color_overlay_g: int
    color_overlay_b: int
    color_avg_r: int
    color_avg_g: int
    color_avg_b: int
    left_capture_part: CapturePart
    middle_capture_part: CapturePart
    right_capture_part: CapturePart


class SceneColorOverlayInfoResponse(BaseResponse):
    message_type: Literal["SceneColorOverlayInfoResponse"]
    data: SceneColorOverlayInfoResponseData


class FaceFoundRequest(BaseRequest):
    message_type: Literal["FaceFoundRequest"] = "FaceFoundRequest"
    data: None = None


class FaceFoundResponseData(_ModelResponses):
    found: bool


class FaceFoundResponse(BaseResponse):
    message_type: Literal["FaceFoundResponse"] = "FaceFoundResponse"
    data: FaceFoundResponseData


class InputParameterListRequest(BaseRequest):
    message_type: Literal["InputParameterListRequest"] = "InputParameterListRequest"
    data: None = None


class SingleParameter(_ModelResponses):
    name: str
    added_by: str
    value: float
    min: float
    max: float
    default_value: float


class InputParameterListResponseData(_ModelResponses):
    model_loaded: bool
    model_name: str
    model_id: str = Field(validation_alias="modelID")
    custom_parameters: List[SingleParameter]
    default_parameters: List[SingleParameter]


class InputParameterListResponse(BaseResponse):
    message_type: Literal["InputParameterListResponse"]
    data: InputParameterListResponseData


class ParameterValueRequestData(_ModelRequests):
    name: str


class ParameterValueRequest(BaseRequest):
    message_type: Literal["ParameterValueRequest"] = "ParameterValueRequest"
    data: ParameterValueRequestData


class ParameterValueResponse(BaseResponse):
    message_type: Literal["ParameterValueResponse", "APIError"]
    data: Union[SingleParameter, ErrorResponse]


class Live2DParameterListRequest(BaseRequest):
    message_type: Literal["Live2DParameterListRequest"] = "Live2DParameterListRequest"
    data: None = None


class SingleParameterWithoutAddedBy(_ModelResponses):
    name: str
    value: float
    min: int
    max: int
    default_value: float


class Live2DParameterListResponseData(_ModelResponses):
    model_loaded: bool
    model_name: str
    model_id: str = Field(validation_alias="modelID")
    parameters: List[SingleParameterWithoutAddedBy]


class Live2DParameterListResponse(BaseResponse):
    message_type: Literal["Live2DParameterListResponse"]
    data: Live2DParameterListResponseData


class ParameterCreationRequestData(_ModelRequests):
    parameter_name: Annotated[str, StringConstraints(min_length=4, max_length=32)]
    explanation: Annotated[str, StringConstraints(max_length=256)]
    min: int
    max: int
    default_value: float = Field(ge=-1000000, lt=1000000)


class ParameterCreationRequest(BaseRequest):
    message_type: Literal["ParameterCreationRequest"] = "ParameterCreationRequest"
    data: ParameterCreationRequestData


class ParameterCreationResponseData(_ModelResponses):
    parameter_name: str


class ParameterCreationResponse(BaseResponse):
    message_type: Literal["ParameterCreationResponse", "APIError"]
    data: Union[ParameterCreationResponseData, ErrorResponse]


class ParameterDeletionRequestData(_ModelRequests):
    parameter_name: str


class ParameterDeletionRequest(BaseRequest):
    message_type: Literal["ParameterDeletionRequest"] = "ParameterDeletionRequest"
    data: ParameterDeletionRequestData


class ParameterDeletionResponseData(_ModelResponses):
    parameter_name: str


class ParameterDeletionResponse(BaseResponse):
    message_type: Literal["ParameterDeletionResponse"]
    data: ParameterDeletionResponseData


class ParameterValue(_ModelRequests):
    id: str
    value: float = Field(ge=-1000000, le=1000000)
    weight: Optional[float] = Field(default=1, ge=0, le=1)


class InjectParameterDataRequestData(_ModelRequests):
    face_found: bool = False
    mode: Optional[Literal["set", "add"]] = None
    parameter_values: List[ParameterValue]


class InjectParameterDataRequest(BaseRequest):
    message_type: Literal["InjectParameterDataRequest"] = "InjectParameterDataRequest"
    data: InjectParameterDataRequestData


class InjectParameterDataResponse(BaseResponse):
    message_type: Literal["InjectParameterDataResponse", "APIError"]
    data: Union[EmptyData, ErrorResponse]


class GetCurrentModelPhysicsRequest(BaseRequest):
    message_type: Literal["GetCurrentModelPhysicsRequest"] = (
        "GetCurrentModelPhysicsRequest"
    )
    data: None = None


class PhysicsGroup(_ModelResponses):
    group_id: str = Field(validation_alias="groupID")
    group_name: str
    strength_multiplier: float
    wind_multiplier: float


class GetCurrentModelPhysicsResponseData(_ModelResponses):
    model_loaded: bool
    model_name: str
    model_id: str = Field(validation_alias="modelID")
    model_has_physics: bool
    physics_switched_on: bool
    using_legacy_physics: bool
    physics_fps_setting: Literal[30, 60, 120, -1] = Field(
        validation_alias="physicsFPSSetting"
    )
    api_physics_override_active: bool
    api_physics_override_plugin_name: str
    physics_groups: List[PhysicsGroup]


class GetCurrentModelPhysicsResponse(BaseResponse):
    message_type: Literal["GetCurrentModelPhysicsResponse", "APIError"]
    data: Union[GetCurrentModelPhysicsResponseData, ErrorResponse]


class Override(_ModelRequests):
    id: str = ""
    value: float = Field(ge=0, le=100)
    set_base_value: bool = False
    override_seconds: float = Field(ge=0.5, le=5)


class SetCurrentModelPhysicsRequestData(_ModelRequests):
    strength_overrides: List[Override] = []
    wind_overrides: List[Override] = []


class SetCurrentModelPhysicsRequest(BaseRequest):
    message_type: Literal["SetCurrentModelPhysicsRequest"] = (
        "SetCurrentModelPhysicsRequest"
    )
    data: SetCurrentModelPhysicsRequestData = SetCurrentModelPhysicsRequestData()


class SetCurrentModelPhysicsResponse(BaseResponse):
    message_type: Literal["SetCurrentModelPhysicsResponse", "APIError"]
    data: Union[EmptyData, ErrorResponse]


class NDIConfigRequestData(_ModelRequests):
    set_new_config: bool = False
    ndi_active: bool = False
    use_ndi_5: bool = Field(default=True, serialization_alias="useNDI5")
    use_custom_resolution: bool = False
    custom_width_ndi: int = Field(default=-1, serialization_alias="customWidthNDI")

    @field_validator("custom_width_ndi")
    @classmethod
    def validate_dimensions_ndi_width(cls, v: int) -> int:
        if v == -1:
            return v
        if v % 16 == 0 and 256 <= v <= 8192:
            return v
        raise ValueError("Has to be -1 or divisible by 16 and between 256 and 8192")

    custom_height_ndi: int = Field(default=-1, serialization_alias="customHeightNDI")

    @field_validator("custom_height_ndi")
    @classmethod
    def validate_dimensions_ndi_width(cls, v: int) -> int:
        if v == -1:
            return v
        if v % 8 == 0 and 256 <= v <= 8192:
            return v
        raise ValueError("Has to be -1 or divisible by 8 and between 256 and 8192")


class NDIConfigRequest(BaseRequest):
    message_type: Literal["NDIConfigRequest"] = "NDIConfigRequest"
    data: NDIConfigRequestData = NDIConfigRequestData()

    @field_validator("data")
    @classmethod
    def validate_dimensions(cls, v: NDIConfigRequestData) -> NDIConfigRequestData:
        if (v.custom_height_ndi == -1) == (v.custom_width_ndi == -1):
            return v
        raise ValueError("if height or width is -1 the other one has to be as well")


class NDIConfigResponseData(_ModelResponses):
    set_new_config: bool
    ndi_active: bool
    use_ndi_5: bool = Field(validation_alias="useNDI5")
    use_custom_resolution: bool
    custom_width_ndi: int = Field(validation_alias="customWidthNDI")
    custom_height_ndi: int = Field(validation_alias="customHeightNDI")


class NDIConfigResponse(BaseResponse):
    message_type: Literal["NDIConfigResponse", "APIError"]
    data: Union[NDIConfigResponseData, ErrorResponse]


class ItemListRequestData(_ModelRequests):
    include_available_spots: bool = True
    include_item_instances_in_scene: bool = True
    include_available_item_files: bool = True
    only_items_with_file_name: Optional[str] = None
    only_items_with_instance_id: Optional[str] = Field(
        default=None, serialization_alias="onlyItemsWithInstanceID"
    )


class ItemListRequest(BaseRequest):
    message_type: Literal["ItemListRequest"] = "ItemListRequest"
    data: ItemListRequestData = ItemListRequestData()


class SingleItemInstanceInScene(_ModelResponses):
    file_name: str
    instance_id: str = Field(validation_alias="instanceID")
    order: int
    type: str
    censored: bool
    flipped: bool
    locked: bool
    smoothing: float
    framerate: float
    frame_count: int
    current_frame: int
    pinned_to_model: bool
    pinned_model_id: str = Field(validation_alias="pinnedModelID")
    pinned_art_mesh_id: str = Field(validation_alias="pinnedArtMeshID")
    group_name: str
    scene_name: str
    from_workshop: bool


class SingleAvailableItemFile(_ModelResponses):
    file_name: str
    type: str
    loaded_count: int


class ItemListResponseData(_ModelResponses):
    items_in_scene_count: int
    total_items_allowed_count: int
    can_load_items_right_now: bool
    available_spots: List[int]
    item_instances_in_scene: List[SingleItemInstanceInScene]
    available_item_files: List[SingleAvailableItemFile]


class ItemListResponse(BaseResponse):
    message_type: Literal["ItemListResponse", "APIError"]
    data: Union[ItemListResponseData, ErrorResponse]


class ItemLoadRequestData(_ModelRequests):
    file_name: str
    position_x: int = Field(default=0, ge=-1000, le=1000)
    position_y: int = Field(default=0, ge=-1000, le=1000)
    size: float = Field(default=0.32, ge=0, le=1)
    rotation: float = Field(default=0, ge=-360, le=360)
    fade_time: float = Field(default=0, ge=0, le=2)
    order: int = 0
    fail_if_order_taken: bool = False
    smoothing: float = Field(default=0, ge=0, le=1)
    censored: bool = False
    flipped: bool = False
    locked: bool = False
    unload_when_plugin_disconnects: bool = True
    custom_data_base_64: Optional[str] = None
    custom_data_ask_user_first: bool = True
    custom_data_skip_asking_user_if_whitelisted: bool = True
    custom_data_ask_timer: float = 0


class ItemLoadRequest(BaseRequest):
    message_type: Literal["ItemLoadRequest"] = "ItemLoadRequest"
    data: ItemLoadRequestData


class ItemLoadResponseData(_ModelResponses):
    instance_id: str = Field(validation_alias="instanceID")
    file_name: str


class ItemLoadResponse(BaseResponse):
    message_type: Literal["ItemLoadResponse", "APIError"]
    data: Union[ItemLoadResponseData, ErrorResponse]


class ItemUnloadRequestData(_ModelRequests):
    unload_all_in_scene: bool = False
    unload_all_loaded_by_this_plugin: bool = False
    allow_unloading_items_loaded_by_user_or_other_plugins: bool = False
    instance_ids: List[str] = Field(default=[], serialization_alias="instanceIDs")
    file_names: List[str] = []


class ItemUnloadRequest(BaseRequest):
    message_type: Literal["ItemUnloadRequest"] = "ItemUnloadRequest"
    data: ItemUnloadRequestData = ItemUnloadRequestData()


class SingleUnloadedItem(_ModelResponses):
    instance_id: str = Field(validation_alias="instanceID")
    file_name: str


class ItemUnloadResponseData(_ModelResponses):
    unloaded_items: List[SingleUnloadedItem]


class ItemUnloadResponse(BaseResponse):
    message_type: Literal["ItemUnloadResponse", "APIError"]
    data: Union[ItemUnloadResponseData, ErrorResponse]


class ItemAnimationControlRequestData(_ModelRequests):
    item_instance_id: str = Field(serialization_alias="itemInstanceID")
    framerate: Optional[float] = Field(default=None, ge=0.1, le=120)
    """only set if item is gif, set to -1 to not change"""
    frame: Optional[int] = None
    """jump to this frame"""
    brightness: float = -1
    opacity: float = -1

    @field_validator("brightness", "opacity")
    @classmethod
    def validate_brightness(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return v
        if v == -1:
            return v
        if 0 <= v <= 100:
            return v
        raise ValueError("has to be none, -1 or between 0 and 100")

    set_auto_stop_frames: bool = False
    auto_stop_frames: List[int] = []
    set_animation_play_state: bool = False
    animation_play_state: bool = True


class ItemAnimationControlRequest(BaseRequest):
    message_type: Literal["ItemAnimationControlRequest"] = "ItemAnimationControlRequest"
    data: ItemAnimationControlRequestData


class ItemAnimationControlResponseData(_ModelResponses):
    frame: int
    animation_playing: bool


class ItemAnimationControlResponse(BaseResponse):
    message_type: Literal["ItemAnimationControlResponse", "APIError"]
    data: Union[ItemAnimationControlResponseData, ErrorResponse]


class SingleItemToMove(_ModelRequests):
    item_instance_id: str = Field(serialization_alias="itemInstanceID")
    time_in_seconds: float = Field(default=0, ge=0, le=30)
    fade_mode: Literal["linear", "easeIn", "easeOut", "easeBoth", "overshoot"] = (
        "linear"
    )
    position_x: int = Field(default=-1000)
    """-1000 or lower to ignore this field"""
    position_y: int = Field(default=-1000)
    """-1000 or lower to ignore this field"""
    size: float = Field(default=-1000)
    """-1000 or lower to ignore this field"""
    rotation: float = Field(default=-1000)
    """-1000 or lower to ignore this field"""
    rotation: int = Field(default=-1000)
    """-1000 or lower to ignore this field"""
    set_flip: bool = False
    fli: bool = False
    user_can_stop: bool = True


class ItemMoveRequestData(_ModelRequests):
    items_to_move: List[SingleItemToMove] = Field(default=[], max_length=64)


class ItemMoveRequest(BaseRequest):
    message_type: Literal["ItemMoveRequest"] = "ItemMoveRequest"
    data: ItemMoveRequestData


class SingleMovedItem(_ModelResponses):
    item_instance_id: str = Field(validation_alias="itemInstanceID")
    success: bool
    error_id: int = Field(validation_alias="errorID")


class ItemMoveResponseData(_ModelResponses):
    moved_items: List[SingleMovedItem]


class ItemMoveResponse(BaseResponse):
    message_type: Literal["ItemMoveResponse", "APIError"]
    data: Union[ItemMoveResponseData, ErrorResponse]


class ArtMeshSelectionRequestData(_ModelRequests):
    text_override: Optional[str] = Field(default=None, min_length=4, max_length=1024)
    help_override: Optional[str] = Field(default=None, min_length=4, max_length=1024)
    requested_art_mesh_count: int = -1
    """negative or 0 for arbitrary amount of meshes"""
    active_art_meshes: List[str] = []


class ArtMeshSelectionRequest(BaseRequest):
    message_type: Literal["ArtMeshSelectionRequest"] = "ArtMeshSelectionRequest"
    data: ArtMeshSelectionRequestData = ArtMeshSelectionRequestData()


class ArtMeshSelectionResponseData(_ModelResponses):
    success: bool
    active_art_meshes: List[str]
    inactive_art_meshes: List[str]


class ArtMeshSelectionResponse(BaseResponse):
    message_type: Literal["ArtMeshSelectionResponse", "APIError"]
    data: Union[ArtMeshSelectionResponseData, ErrorResponse]


class PinInfo(_ModelRequests):
    model_id: Optional[str] = Field(default=None, serialization_alias="modelID")
    art_mesh_id: Optional[str] = Field(default=None, serialization_alias="artMeshID")
    angle: float = Field(default=0, ge=0, le=360)
    size: float = Field(default=0.32, ge=-1, le=1)
    vertex_id_1: Optional[int] = Field(default=None, serialization_alias="vertexID1")
    vertex_id_2: Optional[int] = Field(default=None, serialization_alias="vertexID2")
    vertex_id_3: Optional[int] = Field(default=None, serialization_alias="vertexID3")
    vertex_weight_1: Optional[float] = Field(default=None, ge=0, le=1)
    vertex_weight_2: Optional[float] = Field(default=None, ge=0, le=1)
    vertex_weight_3: Optional[float] = Field(default=None, ge=0, le=1)


class ItemPinRequestData(_ModelRequests):
    pin: bool = True
    item_instance_id: str = Field(serialization_alias="itemInstanceID")
    angle_relative_to: Literal[
        "RelativeToWorld",
        "RelativeToCurrentItemRotation",
        "RelativeToModel",
        "RelativeToPinPosition",
    ] = "RelativeToWorld"
    size_relative_to: Literal["RelativeToWorld", "RelativeToCurrentItemSize"] = (
        "RelativeToWorld"
    )
    vertex_pin_type: Literal["Provided", "Center", "Random"] = "Center"
    pin_info: PinInfo = PinInfo()


class ItemPinRequest(BaseRequest):
    message_type: Literal["ItemPinRequest"] = "ItemPinRequest"
    data: ItemPinRequestData

    @field_validator("data")
    @classmethod
    def validate_itempinrequestdata(cls, v: ItemPinRequestData) -> ItemPinRequestData:
        if v.vertex_pin_type != "Provided":
            return v
        try:
            if not None in [
                v.pin_info.vertex_id_1,
                v.pin_info.vertex_id_2,
                v.pin_info.vertex_id_3,
            ]:
                if (
                    v.pin_info.vertex_weight_1
                    + v.pin_info.vertex_weight_2
                    + v.pin_info.vertex_weight_3
                    == 1
                ):
                    return v
        finally:
            raise ValueError(
                "If vertexPinType is provided, you have to provide 3 vertex ids and the weights have to add up to 1"
            )


class ItemPinResponseData(_ModelResponses):
    is_pinned: bool
    item_instance_id: str = Field(validation_alias="itemInstanceID")
    item_file_name: str


class ItemPinResponse(BaseResponse):
    message_type: Literal["ItemPinResponse", "APIError"]
    data: Union[ItemPinResponseData, ErrorResponse]


class PostProcessingListRequestData(_ModelRequests):
    fill_post_processing_presets_array: bool = False
    fill_post_processing_effects_array: bool = False
    effect_id_filter: List[str] = Field(
        default=[], serialization_alias="effectIDFilter"
    )


class PostProcessingListRequest(BaseRequest):
    message_type: Literal["PostProcessingListRequest"] = "PostProcessingListRequest"
    data: PostProcessingListRequestData = PostProcessingListRequestData()


class SingleConfigEntry(_ModelResponses):
    internal_id: str = Field(validation_alias="internalID")
    enum_id: str = Field(validation_alias="enumID")
    explanation: str
    type: Literal["Float", "Int", "Bool", "String", "Color", "SceneItem"]
    activation_config: bool
    float_value: float
    float_min: float
    float_max: float
    float_default: float
    int_value: int
    int_min: int
    int_max: int
    int_default: int
    color_value: str
    color_default: str
    color_has_alpha: bool
    bool_value: bool
    bool_default: bool
    string_value: str
    string_default: str
    scene_item_value: str
    scene_item_default: str


class SinglePostProcessingEffect(_ModelResponses):
    internal_id: str = Field(validation_alias="internalID")
    enum_id: str = Field(validation_alias="enumID")
    explanation: str
    effect_is_active: bool
    effect_is_restricted: bool
    config_entried: List[SingleConfigEntry]


class PostProcessingListResponseData(_ModelResponses):
    post_processing_supported: bool
    post_processing_active: bool
    can_send_post_processing_update_request_right_now: bool
    restricted_effects_allowed: bool
    preset_is_active: bool
    active_preset: str
    preset_count: int
    active_effect_count: int
    effect_count_before_filter: int
    config_count_before_filter: int
    effect_count_after_filter: int
    config_count_after_filter: int
    post_processing_effects: List[SinglePostProcessingEffect]
    post_processing_presets: List[str]


class PostProcessingListResponse(BaseResponse):
    message_type: Literal["PostProcessingListResponse", "APIError"]
    data: Union[PostProcessingListResponseData, ErrorResponse]


class SinglePostProcessingValue(_ModelRequests):
    config_id: str = Field(serialization_alias="configID")
    config_value: str


class PostProcessingUpdateRequestData(_ModelRequests):
    post_processing_on: bool = True
    set_post_processing_preset: bool = False
    set_post_processing_value: bool = False
    preset_to_set: Optional[str] = None
    post_processing_fade_time: float = Field(default=0, ge=0, le=2)
    set_all_other_values_to_default: bool = True
    using_restricted_effects: bool = False
    randomize_all: bool = False
    randomize_all_chaos_level: float = Field(default=0.4, ge=0, le=1)
    post_processing_values: List[SinglePostProcessingValue] = []


class PostProcessingUpdateRequest(BaseRequest):
    message_type: Literal["PostProcessingUpdateRequest"] = "PostProcessingUpdateRequest"
    data: PostProcessingUpdateRequestData = PostProcessingUpdateRequestData()


class PostProcessingUpdateResponseData(_ModelResponses):
    post_processing_active: bool
    preset_is_active: bool
    active_preset: str
    active_effect_count: int


class PostProcessingUpdateResponse(BaseResponse):
    message_type: Literal["PostProcessingUpdateResponse", "APIError"]
    data: Union[PostProcessingUpdateResponseData, ErrorResponse]

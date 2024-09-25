from unittest import IsolatedAsyncioTestCase
import unittest
import src.PyTubeStudio as pts
import src.VtsModels as VtsModels
import time

events = []


class Test(IsolatedAsyncioTestCase):

    def setUp(self):
        self.MODEL_ID = "6d2a3697bfdf445f92907509f4e34d3b"
        self.HOTKEY_ID = "1a5b73eb88494bf3bad781e75d7b3f38"
        self.EXPRESSION_ID = "expression_info.exp3.json"
        self.PARAM_NAME = "HandLeftFinger_1_Thumb"
        self.FILE_NAME = "ANIM_headpat"
        self.vts = pts.PyTubeStudio()

    async def asyncSetUp(self):
        await self.vts.connect()
        await self.vts.authenticate(VtsModels.AuthenticationTokenRequest())

    #async def test_authentication_token(self):
    #    request = models.AuthenticationTokenRequest()
    #    response = await self.vts.request(request)
    #    response = models.AuthenticationTokenResponse.model_validate_json(response)

    #async def test_authentication_valid_token(self):
    #    request = models.AuthenticationRequest(
    #       data=models.AuthenticationRequestData(
    #            authentication_token=self.vts.auth_token.token
    #        )
    #    )
    #    response = await self.vts.request(request)
    #    response = models.AuthenticationResponse.model_validate_json(response)

    #async def test_authentication_invalid_token(self):
    #    request = models.AuthenticationRequest(
    #        data=models.AuthenticationRequestData(authentication_token="a")
    #    )
    #    response = await self.vts.request(request)
    #    response = models.AuthenticationResponse.model_validate_json(response)

    async def test_statistics(self):
        request = VtsModels.StatisticsRequest()
        response = await self.vts.request(request)
        response = VtsModels.StatisticsResponse.model_validate_json(response)

    async def test_vts_folder_info(self):
        request = VtsModels.VTSFolderInfoRequest()
        response = await self.vts.request(request)
        response = VtsModels.VTSFolderInfoResponse.model_validate_json(response)

    async def test_current_model(self):
        request = VtsModels.CurrentModelRequest()
        response = await self.vts.request(request)
        response = VtsModels.CurrentModelResponse.model_validate_json(response)

    async def test_available_models(self):
        request = VtsModels.AvailableModelsRequest()
        response = await self.vts.request(request)
        response = VtsModels.AvailableModelsResponse.model_validate_json(response)

    async def test_model_loaded_invalid_model_id(self):
        request = VtsModels.ModelLoadRequest(data=VtsModels.ModelLoadRequestData(model_id=""))
        response = await self.vts.request(request)
        response = VtsModels.ModelLoadResponse.model_validate_json(response)

    async def test_model_loaded_valid_model_id(self):
        request = VtsModels.ModelLoadRequest(
            data=VtsModels.ModelLoadRequestData(model_id=self.MODEL_ID)
        )
        response = await self.vts.request(request)
        response = VtsModels.ModelLoadResponse.model_validate_json(response)
        time.sleep(2)
        # when the model is being loaded again, we have to wait for it to finish loading or other tests will fail

    async def test_move_model(self):
        request = VtsModels.MoveModelRequest(
            data=VtsModels.MoveModelRequestData(
                time_in_seconds=1,
                position_x=None,
                position_y=None,
                rotation=1,
                values_are_relative_to_model=False,
            )
        )
        response = await self.vts.request(request)
        response = VtsModels.MoveModelResponse.model_validate_json(response)
        try:
            assert response.message_type == "MoveModelResponse"
        except:
            raise Exception(response.data.message)

    async def test_hotkeys_in_current_model(self):
        request = VtsModels.HotkeysInCurrentModelRequest()
        response = await self.vts.request(request)
        response = VtsModels.HotkeysInCurrentModelResponse.model_validate_json(response)

    async def test_hotkey_trigger_invalid(self):
        request = VtsModels.HotkeyTriggerRequest(
            data=VtsModels.HotkeyTriggerRequestData(hotkey_id="")
        )
        response = await self.vts.request(request)
        response = VtsModels.HotkeyTriggerResponse.model_validate_json(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_hotkey_trigger_valid(self):
        request = VtsModels.HotkeyTriggerRequest(
            data=VtsModels.HotkeyTriggerRequestData(hotkey_id=self.HOTKEY_ID)
        )
        response = await self.vts.request(request)
        response = VtsModels.HotkeyTriggerResponse.model_validate_json(response)
        try:
            assert response.message_type == "HotkeyTriggerResponse"
        except:
            raise Exception(response.data.message)

    async def test_expression_state_invalid(self):
        request = VtsModels.ExpressionStateRequest(
            data=VtsModels.ExpressionStateRequestData(expression_file="a.exp3.json")
        )
        response = await self.vts.request(request)
        response = VtsModels.ExpressionStateResponse.model_validate_json(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_expression_state_valid(self):
        request = VtsModels.ExpressionStateRequest(
            data=VtsModels.ExpressionStateRequestData()
        )
        response = await self.vts.request(request)
        response = VtsModels.ExpressionStateResponse.model_validate_json(response)
        try:
            assert response.message_type == "ExpressionStateResponse"
        except:
            raise Exception(response.data.message)

    async def test_expression_activation_invalid(self):
        request = VtsModels.ExpressionActivationRequest(
            data=VtsModels.ExpressionActivationRequestData(
                expression_file="a.exp3.json", active=True
            )
        )
        response = await self.vts.request(request)
        response = VtsModels.ExpressionActivationResponse.model_validate_json(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_expression_activation_valid(self):
        request = VtsModels.ExpressionActivationRequest(
            data=VtsModels.ExpressionActivationRequestData(
                expression_file=self.EXPRESSION_ID, active=True
            )
        )
        response = await self.vts.request(request)
        response = VtsModels.ExpressionActivationResponse.model_validate_json(response)
        try:
            assert response.message_type == "ExpressionActivationResponse"
        except:
            raise Exception(response.data.message)

    async def test_art_mesh_list(self):
        request = VtsModels.ArtMeshListRequest()
        response = await self.vts.request(request)
        response = VtsModels.ArtMeshListResponse.model_validate_json(response)

    async def test_color_tint(self):
        request = VtsModels.ColorTintRequest(
            data=VtsModels.ColorTintRequestData(
                color_tint=VtsModels.ColorTint(
                    color_a=255, color_b=0, color_g=255, color_r=100
                ),
                art_mesh_matcher=VtsModels.ArtMeshMatcher(tint_all=True),
            )
        )
        response = await self.vts.request(request)
        response = VtsModels.ColorTintResponse.model_validate_json(response)
        try:
            assert response.message_type == "ColorTintResponse"
            assert response.data.matched_art_meshes > 0
        except:
            raise Exception(response.data.message)

    async def test_scene_color_overlay_info(self):
        request = VtsModels.SceneColorOverlayInfoRequest()
        response = await self.vts.request(request)
        response = VtsModels.SceneColorOverlayInfoResponse.model_validate_json(response)

    async def test_face_found(self):
        request = VtsModels.FaceFoundRequest()
        response = await self.vts.request(request)
        response = VtsModels.FaceFoundResponse.model_validate_json(response)

    async def test_input_parameter_list(self):
        request = VtsModels.InputParameterListRequest()
        response = await self.vts.request(request)
        response = VtsModels.InputParameterListResponse.model_validate_json(response)

    async def test_parameter_value_invalid(self):
        request = VtsModels.ParameterValueRequest(
            data=(VtsModels.ParameterValueRequestData(name="a"))
        )
        response = await self.vts.request(request)
        response = VtsModels.ParameterValueResponse.model_validate_json(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_parameter_value_valid(self):
        request = VtsModels.ParameterValueRequest(
            data=(VtsModels.ParameterValueRequestData(name=self.PARAM_NAME))
        )
        response = await self.vts.request(request)
        response = VtsModels.ParameterValueResponse.model_validate_json(response)
        try:
            assert response.message_type == "ParameterValueResponse"
        except:
            raise Exception(response.data.message)

    async def test_live2d_parameter_list(self):
        request = VtsModels.Live2DParameterListRequest()
        response = await self.vts.request(request)
        response = VtsModels.Live2DParameterListResponse.model_validate_json(response)

    async def test_parameter_creation(self):
        request = VtsModels.ParameterCreationRequest(
            data=VtsModels.ParameterCreationRequestData(
                parameter_name="test",
                explanation="nah",
                min=1,
                max=2,
                default_value=1.5,
            )
        )
        response = await self.vts.request(request)
        response = VtsModels.ParameterCreationResponse.model_validate_json(response)

    #async def test_parameter_deletion(self):
    #    request = models.ParameterDeletionRequest(
    #        data=models.ParameterDeletionRequestData(parameter_name="test")
    #    )
    #    response = await self.vts.request(request)
    #    response = models.ParameterDeletionResponse.model_validate_json(response)

    async def test_inject_parameter_data_invalid(self):
        request = VtsModels.InjectParameterDataRequest(
            data=VtsModels.InjectParameterDataRequestData(
                parameter_values=[VtsModels.ParameterValue(id="", value=30)]
            )
        )
        response = await self.vts.request(request)
        response = VtsModels.InjectParameterDataResponse.model_validate_json(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_inject_parameter_data_valid(self):
        request = VtsModels.InjectParameterDataRequest(
            data=VtsModels.InjectParameterDataRequestData(
                parameter_values=[VtsModels.ParameterValue(id=self.PARAM_NAME, value=30)]
            )
        )
        response = await self.vts.request(request)
        response = VtsModels.InjectParameterDataResponse.model_validate_json(response)
        try:
            assert response.message_type == "InjectParameterDataResponse"
        except:
            raise Exception(response.data.message)

    async def test_get_current_model_physics(self):
        request = VtsModels.GetCurrentModelPhysicsRequest()
        response = await self.vts.request(request)
        response = VtsModels.GetCurrentModelPhysicsResponse.model_validate_json(response)

    async def test_set_current_model_physics(self):
        request = VtsModels.SetCurrentModelPhysicsRequest()
        response = await self.vts.request(request)
        response = VtsModels.SetCurrentModelPhysicsResponse.model_validate_json(response)

    async def test_ndi_config_response(self):
        request = VtsModels.NDIConfigRequest()
        response = await self.vts.request(request)
        response = VtsModels.NDIConfigResponse.model_validate_json(response)

    async def test_item_list(self):
        request = VtsModels.ItemListRequest()
        response = await self.vts.request(request)
        response = VtsModels.ItemListResponse.model_validate_json(response)

    async def test_item_load(self):
        request = VtsModels.ItemLoadRequest(
            data=VtsModels.ItemLoadRequestData(file_name=self.FILE_NAME)
        )
        response = await self.vts.request(request)
        response = VtsModels.ItemLoadResponse.model_validate_json(response)

    async def test_item_unload(self):
        request = VtsModels.ItemUnloadRequest(
            data=VtsModels.ItemUnloadRequestData(unload_all_in_scene=True)
        )
        response = await self.vts.request(request)
        response = VtsModels.ItemUnloadResponse.model_validate_json(response)

    async def test_item_animation_control(self):
        request = VtsModels.ItemAnimationControlRequest(
            data=VtsModels.ItemAnimationControlRequestData(item_instance_id=self.FILE_NAME)
        )
        response = await self.vts.request(request)
        response = VtsModels.ItemAnimationControlResponse.model_validate_json(response)

    async def test_item_move(self):
        request = VtsModels.ItemMoveRequest(
            data=VtsModels.ItemMoveRequestData(
                items_to_move=[VtsModels.SingleItemToMove(item_instance_id="a")]
            )
        )
        response = await self.vts.request(request)
        response = VtsModels.ItemMoveResponse.model_validate_json(response)

    async def test_art_mesh_selection(self):
        request = VtsModels.ArtMeshSelectionRequest()
        response = await self.vts.request(request)
        response = VtsModels.ArtMeshSelectionResponse.model_validate_json(response)

    async def test_item_pin(self):
        request = VtsModels.ItemPinRequest(
            data=VtsModels.ItemPinRequestData(item_instance_id="a")
        )
        response = await self.vts.request(request)
        response = VtsModels.ItemPinResponse.model_validate_json(response)

    async def test_post_processing_list(self):
        request = VtsModels.PostProcessingListRequest()
        response = await self.vts.request(request)
        response = VtsModels.PostProcessingListResponse.model_validate_json(response)

    async def test_post_processing_update(self):
        request = VtsModels.PostProcessingUpdateRequest(
            data=VtsModels.PostProcessingUpdateRequestData(randomize_all=True)
        )
        response = await self.vts.request(request)
        response = VtsModels.PostProcessingUpdateResponse.model_validate_json(response)

    async def asyncTearDown(self):
        await self.vts.close()


if __name__ == "__main__":
    unittest.main()

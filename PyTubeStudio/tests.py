from unittest import IsolatedAsyncioTestCase
import unittest
import models
import jaarfivts
import time

events = []


class Test(IsolatedAsyncioTestCase):

    def setUp(self):
        self.MODEL_ID = "6d2a3697bfdf445f92907509f4e34d3b"
        self.HOTKEY_ID = "1a5b73eb88494bf3bad781e75d7b3f38"
        self.EXPRESSION_ID = "expression_info.exp3.json"
        self.PARAM_NAME = "HandLeftFinger_1_Thumb"
        self.FILE_NAME = "ANIM_headpat"
        self.vts = jaarfivts.JaarfiVts(ws_ip="127.0.0.1")

    async def asyncSetUp(self):
        await self.vts.connect()
        await self.vts.authenticate(models.AuthenticationTokenRequest())

    @unittest.skip(
        "annoying to allow each time you run a testrun because you wrote a new test"
    )
    async def test_authentication_token(self):
        request = models.AuthenticationTokenRequest()
        response = await self.vts.request(request)
        response = models.AuthenticationTokenResponse.model_validate(response)

    async def test_authentication_valid_token(self):
        request = models.AuthenticationRequest(
            data=models.AuthenticationRequestData(
                authentication_token=self.vts.auth_token.token
            )
        )
        response = await self.vts.request(request)
        response = models.AuthenticationResponse.model_validate(response)

    async def test_authentication_invalid_token(self):
        request = models.AuthenticationRequest(
            data=models.AuthenticationRequestData(authentication_token="a")
        )
        response = await self.vts.request(request)
        response = models.AuthenticationResponse.model_validate(response)

    async def test_statistics(self):
        request = models.StatisticsRequest()
        response = await self.vts.request(request)
        response = models.StatisticsResponse.model_validate(response)

    async def test_vts_folder_info(self):
        request = models.VTSFolderInfoRequest()
        response = await self.vts.request(request)
        response = models.VTSFolderInfoResponse.model_validate(response)

    async def test_current_model(self):
        request = models.CurrentModelRequest()
        response = await self.vts.request(request)
        response = models.CurrentModelResponse.model_validate(response)

    async def test_available_models(self):
        request = models.AvailableModelsRequest()
        response = await self.vts.request(request)
        response = models.AvailableModelsResponse.model_validate(response)

    async def test_model_loaded_invalid_model_id(self):
        request = models.ModelLoadRequest(data=models.ModelLoadRequestData(model_id=""))
        response = await self.vts.request(request)
        response = models.ModelLoadResponse.model_validate(response)

    @unittest.skip("annoying because we have to sleep in this test")
    async def test_model_loaded_valid_model_id(self):
        request = models.ModelLoadRequest(
            data=models.ModelLoadRequestData(model_id=self.MODEL_ID)
        )
        response = await self.vts.request(request)
        response = models.ModelLoadResponse.model_validate(response)
        time.sleep(
            2
        )  # when the model is being loaded again, we have to wait for it to finish loading or other tests will fail

    async def test_move_model(self):
        request = models.MoveModelRequest(
            data=models.MoveModelRequestData(
                time_in_seconds=1,
                position_x=None,
                position_y=None,
                rotation=1,
                values_are_relative_to_model=False,
            )
        )
        response = await self.vts.request(request)
        response = models.MoveModelResponse.model_validate(response)
        try:
            assert response.message_type == "MoveModelResponse"
        except:
            raise Exception(response.data.message)

    async def test_hotkeys_in_current_model(self):
        request = models.HotkeysInCurrentModelRequest()
        response = await self.vts.request(request)
        response = models.HotkeysInCurrentModelResponse.model_validate(response)

    async def test_hotkey_trigger_invalid(self):
        request = models.HotkeyTriggerRequest(
            data=models.HotkeyTriggerRequestData(hotkey_id="")
        )
        response = await self.vts.request(request)
        response = models.HotkeyTriggerResponse.model_validate(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_hotkey_trigger_valid(self):
        request = models.HotkeyTriggerRequest(
            data=models.HotkeyTriggerRequestData(hotkey_id=self.HOTKEY_ID)
        )
        response = await self.vts.request(request)
        response = models.HotkeyTriggerResponse.model_validate(response)
        try:
            assert response.message_type == "HotkeyTriggerResponse"
        except:
            raise Exception(response.data.message)

    async def test_expression_state_invalid(self):
        request = models.ExpressionStateRequest(
            data=models.ExpressionStateRequestData(expression_file="a.exp3.json")
        )
        response = await self.vts.request(request)
        response = models.ExpressionStateResponse.model_validate(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_expression_state_valid(self):
        request = models.ExpressionStateRequest(
            data=models.ExpressionStateRequestData()
        )
        response = await self.vts.request(request)
        response = models.ExpressionStateResponse.model_validate(response)
        try:
            assert response.message_type == "ExpressionStateResponse"
        except:
            raise Exception(response.data.message)

    async def test_expression_activation_invalid(self):
        request = models.ExpressionActivationRequest(
            data=models.ExpressionActivationRequestData(
                expression_file="a.exp3.json", active=True
            )
        )
        response = await self.vts.request(request)
        response = models.ExpressionActivationResponse.model_validate(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_expression_activation_valid(self):
        request = models.ExpressionActivationRequest(
            data=models.ExpressionActivationRequestData(
                expression_file=self.EXPRESSION_ID, active=True
            )
        )
        response = await self.vts.request(request)
        response = models.ExpressionActivationResponse.model_validate(response)
        try:
            assert response.message_type == "ExpressionActivationResponse"
        except:
            raise Exception(response.data.message)

    async def test_art_mesh_list(self):
        request = models.ArtMeshListRequest()
        response = await self.vts.request(request)
        response = models.ArtMeshListResponse.model_validate(response)

    async def test_color_tint(self):
        request = models.ColorTintRequest(
            data=models.ColorTintRequestData(
                color_tint=models.ColorTint(
                    color_a=255, color_b=0, color_g=255, color_r=100
                ),
                art_mesh_matcher=models.ArtMeshMatcher(tint_all=True),
            )
        )
        response = await self.vts.request(request)
        response = models.ColorTintResponse.model_validate(response)
        try:
            assert response.message_type == "ColorTintResponse"
            assert response.data.matched_art_meshes > 0
        except:
            raise Exception(response.data.message)

    async def test_scene_color_overlay_info(self):
        request = models.SceneColorOverlayInfoRequest()
        response = await self.vts.request(request)
        response = models.SceneColorOverlayInfoResponse.model_validate(response)

    async def test_face_found(self):
        request = models.FaceFoundRequest()
        response = await self.vts.request(request)
        response = models.FaceFoundResponse.model_validate(response)

    async def test_input_parameter_list(self):
        request = models.InputParameterListRequest()
        response = await self.vts.request(request)
        response = models.InputParameterListResponse.model_validate(response)

    async def test_parameter_value_invalid(self):
        request = models.ParameterValueRequest(
            data=(models.ParameterValueRequestData(name="a"))
        )
        response = await self.vts.request(request)
        response = models.ParameterValueResponse.model_validate(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_parameter_value_valid(self):
        request = models.ParameterValueRequest(
            data=(models.ParameterValueRequestData(name=self.PARAM_NAME))
        )
        response = await self.vts.request(request)
        response = models.ParameterValueResponse.model_validate(response)
        try:
            assert response.message_type == "ParameterValueResponse"
        except:
            raise Exception(response.data.message)

    async def test_live2d_parameter_list(self):
        request = models.Live2DParameterListRequest()
        response = await self.vts.request(request)
        response = models.Live2DParameterListResponse.model_validate(response)

    async def test_parameter_creation(self):
        request = models.ParameterCreationRequest(
            data=models.ParameterCreationRequestData(
                parameter_name="test",
                explanation="nah",
                min=1,
                max=2,
                default_value=1.5,
            )
        )
        response = await self.vts.request(request)
        response = models.ParameterCreationResponse.model_validate(response)

    async def test_parameter_deletion(self):
        request = models.ParameterDeletionRequest(
            data=models.ParameterDeletionRequestData(parameter_name="test")
        )
        response = await self.vts.request(request)
        response = models.ParameterDeletionResponse.model_validate(response)

    async def test_inject_parameter_data_invalid(self):
        request = models.InjectParameterDataRequest(
            data=models.InjectParameterDataRequestData(
                parameter_values=[models.ParameterValue(id="", value=30)]
            )
        )
        response = await self.vts.request(request)
        response = models.InjectParameterDataResponse.model_validate(response)
        try:
            assert response.message_type == "APIError"
        except:
            raise Exception("Expected Error and received positive feedback")

    async def test_inject_parameter_data_valid(self):
        request = models.InjectParameterDataRequest(
            data=models.InjectParameterDataRequestData(
                parameter_values=[models.ParameterValue(id=self.PARAM_NAME, value=30)]
            )
        )
        response = await self.vts.request(request)
        response = models.InjectParameterDataResponse.model_validate(response)
        try:
            assert response.message_type == "InjectParameterDataResponse"
        except:
            raise Exception(response.data.message)

    async def test_get_current_model_physics(self):
        request = models.GetCurrentModelPhysicsRequest()
        response = await self.vts.request(request)
        response = models.GetCurrentModelPhysicsResponse.model_validate(response)

    async def test_set_current_model_physics(self):
        request = models.SetCurrentModelPhysicsRequest()
        response = await self.vts.request(request)
        response = models.SetCurrentModelPhysicsResponse.model_validate(response)

    async def test_ndi_config_response(self):
        request = models.NDIConfigRequest()
        response = await self.vts.request(request)
        response = models.NDIConfigResponse.model_validate(response)

    async def test_item_list(self):
        request = models.ItemListRequest()
        response = await self.vts.request(request)
        response = models.ItemListResponse.model_validate(response)

    async def test_item_load(self):
        request = models.ItemLoadRequest(
            data=models.ItemLoadRequestData(file_name=self.FILE_NAME)
        )
        response = await self.vts.request(request)
        response = models.ItemLoadResponse.model_validate(response)

    async def test_item_unload(self):
        request = models.ItemUnloadRequest(
            data=models.ItemUnloadRequestData(unload_all_in_scene=True)
        )
        response = await self.vts.request(request)
        response = models.ItemUnloadResponse.model_validate(response)

    async def test_item_animation_control(self):
        request = models.ItemAnimationControlRequest(
            data=models.ItemAnimationControlRequestData(item_instance_id=self.FILE_NAME)
        )
        response = await self.vts.request(request)
        response = models.ItemAnimationControlResponse.model_validate(response)

    async def test_item_move(self):
        request = models.ItemMoveRequest(
            data=models.ItemMoveRequestData(
                items_to_move=[models.SingleItemToMove(item_instance_id="a")]
            )
        )
        response = await self.vts.request(request)
        response = models.ItemMoveResponse.model_validate(response)

    async def test_art_mesh_selection(self):
        request = models.ArtMeshSelectionRequest()
        response = await self.vts.request(request)
        response = models.ArtMeshSelectionResponse.model_validate(response)

    async def test_item_pin(self):
        request = models.ItemPinRequest(
            data=models.ItemPinRequestData(item_instance_id="a")
        )
        response = await self.vts.request(request)
        response = models.ItemPinResponse.model_validate(response)

    async def test_post_processing_list(self):
        request = models.PostProcessingListRequest()
        response = await self.vts.request(request)
        response = models.PostProcessingListResponse.model_validate(response)


    async def test_post_processing_update(self):
        request = models.PostProcessingUpdateRequest(data=models.PostProcessingUpdateRequestData(randomize_all=True))
        response = await self.vts.request(request)
        response = models.PostProcessingUpdateResponse.model_validate(response)

    async def asyncTearDown(self):
        await self.vts.close()


if __name__ == "__main__":
    unittest.main()

import time
import tomli
import obswebsocket
from obswebsocket import requests
import pathlib

path_config = pathlib.Path('./config.toml')
with open(path_config, "rb") as f:
    toml_dict = tomli.load(f)
pwd_obs = toml_dict.get('OBS_WEBSOCKET')['pwd_obs']
IPv4_obs = toml_dict.get('OBS_WEBSOCKET')['ipv4_obs']
# IPv4_obs = "localhost"

"""
Disclaimer : This file works with OBS-WEBSOCKET 5.X.X
Go here to see why : https://github.com/obsproject/obs-websocket/discussions/1119

You are forced to  e x p l i c i t l y  write down every source of OBS you will modify

To make things things easier for you, every functions in this project are not connected to each other
So
There is always a try catch with the obs part in case things go bad :eyes:
"""

_source1_name = "JOUEUR_GAUCHE"
_source2_name = "JOUEUR_DROITE"
_source3_name = "ROUND_TOURNOI"
_source4_name = "SCORE_GAUCHE"
_source5_name = "SCORE_DROITE"
_source6_name = "NOM_CONF_1"
_source7_name = "NOM_CONF_2"
_source8_name = "NOM_CONF_3"
_source9_name = "NOM_CONF"
_scene1_name = "TABLE RONDE - TEMPLATE"


def swap_text_sources(ws, source1_name, source2_name):
    # Get the current text contents of the two sources
    source1_props = ws.call(obswebsocket.requests.GetInputSettings(inputName=source1_name))
    # print(source1_props.datain['text'])
    source2_props = ws.call(obswebsocket.requests.GetInputSettings(inputName=source2_name))
    # print(source2_props.datain['text'])
    source1_text = source1_props.datain['inputSettings']['text']
    source2_text = source2_props.datain['inputSettings']['text']
    print("nouveau text 1 " + source1_text)
    print("nouveau text 2 " + source2_text)
    # Set the text contents of the sources to each other's text
    ws.call(obswebsocket.requests.SetInputSettings(inputName=source1_name, inputSettings={"text": source2_text}))
    ws.call(obswebsocket.requests.SetInputSettings(inputName=source2_name, inputSettings={"text": source1_text}))


def rename_players(source1_name, source2_name, source1_text, source2_text):
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()

    ws.call(obswebsocket.requests.SetInputSettings(inputName=source1_name, inputSettings={"text": source2_text}))
    ws.call(obswebsocket.requests.SetInputSettings(inputName=source2_name, inputSettings={"text": source1_text}))
    ws.disconnect()


'''
This function is used to change the text of 3 selected text field, so for the matches it's for 2 players and the name
of the match AND for the table ronde it's for changing 3 text that have the same text (it's for the echo effect on OBS)
'''


def rename_players_and_match(ws, source1_name, source2_name, source3_name, source1_text, source2_text, source3_text):
    ws.call(obswebsocket.requests.SetInputSettings(inputName=source1_name, inputSettings={"text": source1_text}))
    ws.call(obswebsocket.requests.SetInputSettings(inputName=source2_name, inputSettings={"text": source2_text}))
    ws.call(obswebsocket.requests.SetInputSettings(inputName=source3_name, inputSettings={"text": source3_text}))


def obs_do_swap_of_players():
    # Set the contents of a text file in OBS Studio
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    try:
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)
        # swap players NAMES
        swap_text_sources(ws, _source1_name, _source2_name)
        # swap players SCORES
        swap_text_sources(ws, _source4_name, _source5_name)

        # ws.call(obswebsocket.requests.GetInputSettings(source="textTestAPI", text="Hello, world!"))

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def reset_scores(ws, _source4_name, _source5_name):
    ws.call(obswebsocket.requests.SetInputSettings(inputName=_source4_name, inputSettings={"text": "0"}))
    ws.call(obswebsocket.requests.SetInputSettings(inputName=_source5_name, inputSettings={"text": "0"}))
    return True


def obs_confirm_next_game(source1_text, source2_text, source3_text):
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    try:
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)

        rename_players_and_match(ws, _source1_name, _source2_name, _source3_name, source1_text, source2_text,
                                 source3_text)
        reset_scores(ws, _source4_name, _source5_name)
        # ws.call(obswebsocket.requests.GetInputSettings(source="textTestAPI", text="Hello, world!"))

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def obs_confirm_next_guest(guest_text):
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    print("Guest_text")
    print(guest_text)
    try:
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)
        rename_players_and_match(ws, _source6_name, _source7_name, _source8_name, guest_text, guest_text,
                                 guest_text)

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def add_1_player(ws, source_name):
    source_props = ws.call(obswebsocket.requests.GetInputSettings(inputName=source_name))

    source_text = str(int(source_props.datain['inputSettings']['text']) + 1)  # changed str to int to str
    # print("Plus 1" + source_text)
    ws.call(obswebsocket.requests.SetInputSettings(inputName=source_name, inputSettings={"text": source_text}))
    return True


def minus_1_player(ws, source_name):
    source_props = ws.call(obswebsocket.requests.GetInputSettings(inputName=source_name))
    source_text = str(int(source_props.datain['inputSettings']['text']) - 1)
    # print("Plus 1" + source_text)
    ws.call(obswebsocket.requests.SetInputSettings(inputName=source_name, inputSettings={"text": source_text}))
    return True


def obs_add_1_player_1():
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    try:
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)

        add_1_player(ws, _source4_name)

        # ws.call(obswebsocket.requests.GetInputSettings(source="textTestAPI", text="Hello, world!"))

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def obs_add_1_player_2():
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    try:
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)

        add_1_player(ws, _source5_name)

        # ws.call(obswebsocket.requests.GetInputSettings(source="textTestAPI", text="Hello, world!"))

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def obs_minus_1_player_1():
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    try:
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)

        minus_1_player(ws, _source4_name)

        # ws.call(obswebsocket.requests.GetInputSettings(source="textTestAPI", text="Hello, world!"))

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def obs_minus_1_player_2():
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    try:
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)

        minus_1_player(ws, _source5_name)

        # ws.call(obswebsocket.requests.GetInputSettings(source="textTestAPI", text="Hello, world!"))

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def obs_get_all_scenes():
    global scenes_obs
    scene_names = []
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    try:
        scenes_obs = ws.call(requests.GetSceneList())
        print(scenes_obs)
        for s in scenes_obs.getScenes():
            scene_names.append(s['sceneName'])
        # here we reverse the list because OBS when doing GetSceneList does a FIFO so the first
        # scene will be the last on your list
        scene_names = reversed(scene_names)
    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()
    return scene_names


def obs_switch2scene(scene):
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    try:
        ws.call(requests.SetCurrentProgramScene(sceneName=scene))
    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def get_item_id(ws, source_name):
    source_id_props = ws.call(obswebsocket.requests.GetSceneItemId(sceneName=_scene1_name, sourceName=source_name))
    source_id = source_id_props.datain['sceneItemId']
    print("source_id")
    return source_id


def get_item_enable_state(ws, scene_name, source_id):
    source_state_props = ws.call(obswebsocket.requests.GetSceneItemEnabled(sceneName=scene_name, sceneItemId=source_id))
    source_state = source_state_props.datain["sceneItemEnabled"]
    print("source_state")
    print(source_state)
    return source_state


def set_item_enable_state(ws, scene_name, source_id, status_desired):
    GetSceneItemEnabled_test = ws.call(obswebsocket.requests.SetSceneItemEnabled(sceneName=scene_name,
                                                                                 sceneItemId=source_id,
                                                                                 sceneItemEnabled=status_desired))
    print("GetSceneItemEnabled_test")
    print(GetSceneItemEnabled_test)
    return True


'''
This function hides a source in OBS, (it could be a group OR a single source), if it's hidden it will unhide and vice
versa
'''


def obs_hide_unhide_item():
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    print("here")
    try:
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)
        item_id = get_item_id(ws, _source9_name)
        item_status = get_item_enable_state(ws, _scene1_name, item_id)
        if item_status:
            # It means the boolean is 1 so True
            set_item_enable_state(ws, _scene1_name, item_id, False)
        else:
            set_item_enable_state(ws, _scene1_name, item_id, True)

        # ws.call(obswebsocket.requests.GetInputSettings(source="textTestAPI", text="Hello, world!"))

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()


def obs_synthe_in_out(guest_text):
    ws = obswebsocket.obsws(IPv4_obs, 4455, pwd_obs)
    ws.connect()
    print("here")
    try:
        rename_players_and_match(ws, _source6_name, _source7_name, _source8_name, guest_text, guest_text,
                                 guest_text)
        # scenes = ws.call(requests.GetSceneList())
        # print(scenes)
        item_id = get_item_id(ws, _source9_name)
        item_status = get_item_enable_state(ws, _scene1_name, item_id)

        set_item_enable_state(ws, _scene1_name, item_id, True)
        time.sleep(10)
        set_item_enable_state(ws, _scene1_name, item_id, False)

        # ws.call(obswebsocket.requests.GetInputSettings(source="textTestAPI", text="Hello, world!"))

    except KeyboardInterrupt:
        pass
    # Disconnect from the WebSocket server
    ws.disconnect()

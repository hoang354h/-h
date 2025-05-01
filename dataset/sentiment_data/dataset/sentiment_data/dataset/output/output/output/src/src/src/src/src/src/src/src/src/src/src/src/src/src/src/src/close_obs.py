import obspython as obs

def close_obs():
    obs.obs_frontend_recording_stop()
    obs.obs_frontend_streaming_stop()
    print("Closed OBS!")

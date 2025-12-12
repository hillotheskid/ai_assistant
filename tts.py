import requests



def tts(text: str, output_file: str = "out.wav"):
    speaker_id = 14  # 冥鳴ひまり - ノーマル
    base_url = "http://localhost:50021"

    query_response = requests.post(
        f"{base_url}/audio_query",
        params={"text": text, "speaker": speaker_id}
    )

    if query_response.status_code != 200:
        raise Exception(f"Failed to generate audio_query: {query_response.text}")

    synthesis_response = requests.post(
        f"{base_url}/synthesis",
        params={"speaker": speaker_id},
        headers={"Content-Type": "application/json"},
        data=query_response.content
    )

    if synthesis_response.status_code != 200:
        raise Exception(f"Failed to synthesize audio: {synthesis_response.text}")

    with open(output_file, "wb") as f:
        f.write(synthesis_response.content)

    return output_file 


import json


class Config:
    def __init__(self):
        self.json_encoder = json.JSONEncoder
        self.json_decoder = json.JSONDecoder

    def set_json_encoder(self, encoder):
        self.json_encoder = encoder

    def set_json_decoder(self, decoder):
        self.json_decoder = decoder


config = Config()

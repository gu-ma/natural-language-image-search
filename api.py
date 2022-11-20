from pathlib import Path
import numpy as np
import pandas as pd
import clip
import torch

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


def encode_text(txt):
    with torch.no_grad():

        # Encode and normalize the description using CLIP
        text_encoded = model.encode_text(clip.tokenize(txt).to(device))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)

        # Retrieve the description vector and the photo vectors
        text_features = text_encoded.cpu().numpy()

        return text_features


class Index(Resource):
    def get(self):
        results = [str(p) for p in photos_files]
        return jsonify(results)


class EncodeText(Resource):
    def get(self):

        txt = request.args.get("text")

        if txt:
            text_features = encode_text(txt)
            results = text_features[0].tolist()

        else:
            results = "Missing arguments"

        return jsonify(results)


class GetClosest(Resource):
    def get(self):

        txt = request.args.get("text")

        if txt:
            text_features = encode_text(txt)

            # Compute the similarity between the descrption and each photo using the Cosine similarity
            similarities = (text_features @ photo_features.T).squeeze(0).tolist()

            # Sort the photos by their similarity score
            best_photos = sorted(
                zip(similarities, range(photo_features.shape[0])),
                key=lambda x: x[0],
                reverse=True,
            )
            # for p in best_photos[:10]:
            #     print(type(p), [str(p[0]), str(p[1])])
            results = best_photos[:10]

        else:
            results = "Missing arguments"

        return jsonify(results)


api.add_resource(Index, "/index")
api.add_resource(EncodeText, "/encode_text")
api.add_resource(GetClosest, "/get_closest")


if __name__ == "__main__":

    # Set the paths
    photos_path = Path("featurescoop_salvatore") / "imgs"
    features_path = Path("featurescoop_salvatore") / "features"

    # List all JPGs in the folder
    photos_files = list(photos_path.glob("*.jpg"))
    photos_files.sort()

    # Load the features and the corresponding IDs
    photo_features = np.load(features_path / "features.npy")
    photo_ids = pd.read_csv(features_path / "photo_ids.csv")
    photo_ids = list(photo_ids["photo_id"])

    # Load the open CLIP model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("checkpoints/ViT-B-32.pt", device=device)

    app.config["JSON_SORT_KEYS"] = False
    app.run(host="0.0.0.0", port=5001)

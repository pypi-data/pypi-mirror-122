# Music-Classifier
python3 library with pretrained classifier.
## Installation
pip installation: pip install musicnet
## Usage template
```
# python3
from from musicnet.MusicClassifier import get_music_classifier
net = get_music_classifier()
net.predict_proba_display(X_path="music_folder") 
```
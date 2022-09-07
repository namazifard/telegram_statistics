import json
from pathlib import Path
from turtle import width
from typing import Union

import arabic_reshaper
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    """Generates chat statistics from a telegram chat json file
    """
    def __init__(self, chat_json: Union[str, Path]):
        """
        :param chat_json: path to telegram export json file
        """

        # load chat data
        with open(chat_json) as f:
            self.chat_data = json.load(f)
    
        self.normalizer = Normalizer()

        # load stopwords
        stop_words = open(DATA_DIR / 'stopwords.txt').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normalizer.normalize, stop_words))

    def generate_word_cloud(
        self,
        output_dir: Union[str, Path],
        width: int = 1800,
        height: int = 1800
    ):
        """Generates a word cloud from a chat data
        :param output_dir: path to output directory for word cloud image
        """
        text_content = ''

        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = list(filter(lambda item: item not in self.stop_words, tokens))
                text_content += f" {' '.join(tokens)}"

        # normalize, reshape for final word cloud
        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        text_content = get_display(text_content)

        # generate word cloud
        wordcloud = WordCloud(
            width=1800, height=1800,
            background_color='white',
            font_path=str(DATA_DIR / 'fonts/BHoma.ttf'),
        ).generate(text_content)

        wordcloud.to_file(str(Path(output_dir) / 'wordcloud.png'))
    

if __name__ == "__main__":
    chat_stats = ChatStatistics(chat_json=DATA_DIR / 'difen.json')
    chat_stats.generate_word_cloud(output_dir=DATA_DIR)

print('Done!')

import html2text
import pytz
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import torch
from scipy.special import expit


def toots_processing(toots):
    toots_processed = []
    for toot in toots:
        toot_id = toot['id']

        toot_created_at = toot['created_at']
        toot_created_at_reformat = datetime2string(toot_created_at)

        toot_content_html = toot['content']
        toot_content_text = content_processing(toot_content_html)

        toot_url = toot['url']

        toot_language = toot['language']

        toot_processed = {
            'id': toot_id,
            'created_at': toot_created_at_reformat,
            'content': toot_content_text,
            'url': toot_url,
            'language': toot_language
        }
        toots_processed.append(toot_processed)
    return toots_processed


def toot_processing(raw_toot):
    toot_id = raw_toot['id']

    toot_created_at = raw_toot['created_at']
    toot_created_at_reformat = datetime2string(toot_created_at)

    toot_content_html = raw_toot['content']
    toot_content_text = content_processing(toot_content_html)

    toot_sentiment_score = toots_sentiment_analysis(toot_content_text)
    toot_topics = toot_topic_classification(toot_content_text)

    toot_url = raw_toot['url']

    toot_language = raw_toot['language']

    toot_processed = {
        'id': toot_id,
        'created_at': toot_created_at_reformat,
        'content': toot_content_text,
        'sentiment_score': toot_sentiment_score,
        "topics": toot_topics,
        'url': toot_url,
        'language': toot_language
    }
    return toot_processed


def toots_sentiment_analysis(toot_content):
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(toot_content)
    sentiment_score = ss["compound"]
    return sentiment_score


def datetime2string(toot_datetime):
    """
    Convert datetime object to string
    :param toot_datetime:
    :return:
    """
    sydney_timezone = pytz.timezone('Australia/Sydney')
    sydney_datetime = toot_datetime.astimezone(sydney_timezone)
    toot_datetime_string = sydney_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")
    return toot_datetime_string


def content_processing(toot_content):
    """
    Convert html to text
    :param toot_content:
    :return:
    """
    h = html2text.HTML2Text()
    h.ignore_links = True
    toot_content_text = h.handle(toot_content)
    toot_content_text_without_newlines = toot_content_text.replace("\n", "")
    return toot_content_text_without_newlines


def toot_topic_classification(toot):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = f"cardiffnlp/tweet-topic-21-multi"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)

    class_mapping = model.config.id2label
    topics = []
    tokens = tokenizer(toot, return_tensors='pt', max_length=512, truncation=True).to(device)
    output = model(**tokens)
    output = {key: value.to("cpu") for key, value in output.items()}
    scores = output["logits"][0].detach().numpy()
    scores = expit(scores)
    predictions = (scores >= 0.5) * 1

    for i in range(len(predictions)):
        if predictions[i]:
            topics.append(class_mapping[i])

    return topics

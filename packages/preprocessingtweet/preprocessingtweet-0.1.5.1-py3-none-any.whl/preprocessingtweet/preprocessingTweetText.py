"""
Pre-process a tweet text and return a cleaned version of it alongside the mentions, the hashtags the URLs and the RT status (defined if it catches a 'RT" at the beginning of a tweet'
"""
import re

import emot
from gensim.utils import deaccent
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

# Catch the mentions
mention_re = re.compile(r"@([A-Za-z0-9_]+)")

# Catch the hashtags
hashtag_re = re.compile(r"^#\S+|\s#\S+")

# Catch any URL
url_re = re.compile(
    "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)

# Catch the RT
rt_re = re.compile(r"^RT", re.IGNORECASE)

# Tokeniser
to_split_re = re.compile(r"\w+")


def return_token(txt: str, tokenizer=None):
    """
    Use a tokenizer to return text in a list format
    :params:
        txt str(): text to tokenised
        tokeniser tokenizer(): Which tokeniser is used. Default RegexpTokenizer
    :return:
        list() of tokens
    """
    if isinstance(txt, list):
        txt = " ".join(txt)
    if tokenizer is None:
        tokenizer = RegexpTokenizer(to_split_re)
    return tokenizer.tokenize(txt)


def stem_text(txt: list, lang: str):
    """
    Return a stemmed version of the input list of words

    :params:
        txt list(): of str to stem
        lang: str(): language of the text to clean
    """
    stemmer = SnowballStemmer(lang)
    try:
        if isinstance(txt, str):
            return [stemmer.stem(w) for w in txt.split(" ") if len(w) > 0]
        elif isinstance(txt, list):
            return [stemmer.stem(w) for w in txt if len(w) > 0]
    except TypeError:  # In case of np.NaN
        return txt


def remove_accent(sentence):
    return deaccent(sentence)


def remove_stop(txt, lang):
    """ """
    stop_words = set(stopwords.words(lang))
    stop_words.update([".", ",", '"', "'", ":", ";",
                      "(", ")", "[", "]", "{", "}"])
    # TODO Remove all first person plural from the set
    # stop_words.update(["MENTION".lower(), "RT".lower(), "URL".lower()])
    if isinstance(txt, str):
        txt = txt.split(" ")
    try:
        return [
            w
            for w in txt
            if str(w).lower().rstrip() not in stop_words and len(str(w).rstrip()) > 0
        ]
    except TypeError:
        return None


def convert_emo(text, type_symbol="emoticon"):
    """ """

    def replace_emo(txt, indexes, replacements):
        for (index, replacement) in zip(indexes, replacements):
            txt[index] = replacement
        return txt

    replacement = None
    converter_emo = emot.core.emot()
    if type_symbol == "emoticon":
        converted_emo = converter_emo.emoticons(text)
    elif type_symbol == "emoji":
        converted_emo = converter_emo.emoji(text)
    else:
        raise Exception("Need a type of symbol, either emoticon or emoji")
    if converted_emo["flag"] is True:
        text = [x for x in text]
        idx_emo = [
            location[0] for location in converted_emo["location"]
        ]  # Get the first el as it is a single car
        replacement = converted_emo["mean"]
        replacement = [
            "__" +
            x.upper()
            .replace(", ", "_")
            .replace(" or ", "_")
            .replace(" ", "_")
            .replace(":", "") +
            "__"
            for x in replacement
        ]
        text = replace_emo(
            text,
            idx_emo,
            replacement,
        )
        text = "".join(text)
    return text, replacement


def remove_mentions_from_txt(txt, remove_mention, mention_re):
    """ """
    if remove_mention is True:
        mention_replace = ""
    else:
        mention_replace = "__MENTION__"
    txt, mentions = remove_compiled_regex(txt, mention_re, mention_replace)
    return txt, mentions


def remove_urls_from_txt(txt, remove_url, url_re):
    """ """
    if remove_url is True:
        url_replace = ""
    else:
        url_replace = "__URL__"
    txt, urls = remove_compiled_regex(txt, url_re, url_replace)
    return txt, urls


def remove_hashtags_from_txt(txt, remove_hashtag, hashtag_re):
    """ """
    if remove_hashtag is True:
        txt, hashtags = remove_compiled_regex(txt, hashtag_re, "__HASHTAG__")
    else:
        hashtags = hashtag_re.findall(txt)
        # txt = txt.replace("#", "")
    return txt, hashtags


def remove_rt_from_txt(txt, remove_rt, rt_re):
    """ """
    if remove_rt is True:
        rt_replace = ""
    else:
        rt_replace = "RT"
    txt, rt_status = remove_compiled_regex(txt, rt_re, rt_replace)
    # Transform into boolean to return True or False if catch RT
    rt_status = bool(rt_status)

    return txt, rt_status


def remove_compiled_regex(txt: str, compiled_regex: re.compile, substitute: str = ""):
    """
    Search for the compiled regex in the txt and either replace it with the substitute or remove it
    """
    entities = compiled_regex.findall(txt)
    txt = compiled_regex.sub(substitute, txt)
    return txt, entities


def remove_entities(txt: str,
                    remove_hashtag: bool,
                    remove_url: bool,
                    remove_mention: bool,
                    remove_rt: bool):
    """
    Removes entities from an input text, such as mentions, URLs, hashtags, and retweet symbols.

    Args:
        txt (str): The input text to process.
        remove_hashtag (bool): Whether to remove hashtags from the input text.
        remove_url (bool): Whether to remove URLs from the input text.
        remove_mention (bool): Whether to remove mentions from the input text.
        remove_rt (bool): Whether to remove "RT" (retweet) from the input text.

    Returns:
        tuple: A tuple containing the processed text and any removed entities. The first element of the tuple
            is the processed text as a string, while the remaining elements are lists containing any removed
            mentions, URLs, hashtags, and the retweet status as a boolean value (True if the input text is a retweet,
            False otherwise).
    """
    txt, mentions_lists = remove_mentions_from_txt(
        txt, remove_mention, mention_re)

    # Remove URL
    txt, urls_lists = remove_urls_from_txt(txt, remove_url, url_re)

    # Remove Hashtags
    # We keep the hashtags as they can be normal words
    txt, hashtags_list = remove_hashtags_from_txt(
        txt, remove_hashtag, hashtag_re)

    # Remove RT symbol
    txt, rt_bool = remove_rt_from_txt(txt, remove_rt, rt_re)

    return txt, mentions_lists, urls_lists, hashtags_list, rt_bool


def preprocess_text(
    sentence: str,
    lowercase: bool = False,
    remove_accent: bool = False,
    remove_punctuation: bool = False,
    remove_hashtag: bool = False,
    remove_url: bool = False,
    remove_mention: bool = False,
    remove_rt: bool = True,
    replace_emoticon: bool = True,
    replace_emoji: bool = True,
):
    """
    Preprocesses a text by performing a series of transformations, such as removing URLs, mentions, hashtags,
    punctuation, and converting emojis and emoticons into text. The output is a dictionary containing the processed
    text and any removed entities, such as URLs, mentions, or hashtags.

    Args:
        sentence (str): The input text to preprocess.
        lowercase (bool, optional): Whether to convert the input text to lowercase. Defaults to False.
        remove_accent (bool, optional): Whether to remove accents from characters. Defaults to False.
        remove_punctuation (bool, optional): Whether to remove punctuation from the input text. Defaults to False.
        remove_hashtag (bool, optional): Whether to remove hashtags from the input text. Defaults to False.
        remove_url (bool, optional): Whether to remove URLs from the input text. Defaults to False.
        remove_mention (bool, optional): Whether to remove mentions from the input text. Defaults to False.
        remove_rt (bool, optional): Whether to remove "RT" (retweet) from the input text. Defaults to True.
        replace_emoticon (bool, optional): Whether to convert emoticons into text. Defaults to True.
        replace_emoji (bool, optional): Whether to convert emojis into text. Defaults to True.

    Returns:
        dict: A dictionary containing the processed text and any removed entities, such as URLs, mentions, or hashtags.
            The keys in the dictionary are: 'tweet' for the processed text, 'mentions' for any removed mentions,
            'urls' for any removed URLs, 'hashtags' for any removed hashtags, 'rt_status' for the retweet status
            (True if the input text is a retweet, False otherwise), 'emoticons' for any converted emoticons,
            and 'emojis' for any converted emojis.
    """
    mentions = None
    urls = None
    hashtags = None
    rt_status = None
    emoticons = None
    emojis = None
    try:
        # lowering all words
        if lowercase:
            sentence = sentence.lower()

        # remove entities and get the list of the removed object if need future parsing
        (sentence, mentions, urls, hashtags, rt_status,) = remove_entities(
            sentence, remove_mention, remove_url, remove_hashtag, remove_rt
        )
        # Single character removal
        # sentence = re.sub(r"\s+[a-zA-Z]\s+", " ", sentence)

        # Replace the accents with a normalised version
        if remove_accent:
            sentence = remove_accent(sentence)

        # Replace emoticon if true
        if replace_emoticon:
            sentence, emoticons = convert_emo(sentence, type_symbol="emoticon")

        # Replace emojis if True
        if replace_emoji:
            sentence, emojis = convert_emo(sentence, type_symbol="emoji")

        # Remove punctuations and numbers but keeping underscore
        if remove_punctuation:
            sentence = re.sub("[^a-zA-Z_]", " ", sentence)

        # Removing multiple spaces
        sentence = " ".join(sentence.split())
    except Exception as e:
        print(e)
        print("Sentence: {} - Type {}".format(sentence, type(sentence)))
        raise

    return {
        "tweet": sentence,
        "mentions": mentions,
        "urls": urls,
        "hashtags": hashtags,
        "rt_status": rt_status,
        "emoticons": emoticons,
        "emojis": emojis,
    }


def preprocessing_list_text(list_to_process):
    raise NotImplementedError()


def main():

    test_tweet = "__MENTION__ __MENTION__ enserio cuando habeis dicho que los froot loops estan malos me ha dolido...  ❤ @mentions of an #hastags :(,  :), :< @Toto, #hastags"
    print("Original Tweet")
    print(test_tweet)
    process_tweet = preprocess_text(test_tweet)
    print("Preprocess tweet")
    print(process_tweet)

    print("Token tweet")
    token_tweet = return_token(process_tweet["tweet"])
    print(token_tweet)

    print("Stem tweet")
    stem_tweet = stem_text(process_tweet["tweet"], lang="spanish")
    print(stem_tweet)


if __name__ == "__main__":
    main()

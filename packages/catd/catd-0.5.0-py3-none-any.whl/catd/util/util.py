import datetime
import logging
import os
import pickle
import re
import sqlite3
import sys
import urllib.request
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from gensim import matutils
from matplotlib.font_manager import FontProperties

logging.getLogger().setLevel(logging.INFO)


def set_up_current_dir_as_working_dir(download_test_set=True):
    """
    Create necessary directory and download test set
    :param download_test_set:
    :return:
    """
    Path(os.path.join('data', 'original_data')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('data', 'selected_words')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('data', 'stop_words')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('output', 'objects')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('output', 'cut_docs')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('output', 'description')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join('output', 'extracted_words')).mkdir(parents=True, exist_ok=True)
    if download_test_set:
        data_set_url = 'https://github.com/dqwert/dataset/raw/master/test_weibo_COVID19.db'
        logging.info('downloading dataset from', data_set_url)
        urllib.request.urlretrieve(data_set_url, os.path.join('data', 'original_data', 'test_weibo_COVID19.db'))
        logging.info('download complete.')


def save_obj(obj, name):
    with open(os.path.join(os.getcwd(), 'output', 'objects', name + '.pkl'), 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(os.path.join(os.getcwd(), 'output', 'objects', name + '.pkl'), 'rb+') as f:
        return pickle.load(f)


def display_progress(prompt, curr_progress, total):
    if curr_progress % 100 == 0:
        progress_percent = curr_progress / total
        sys.stdout.write('\r')
        sys.stdout.write('%s [%s%s]%3.1f%s' % (
            prompt, '█' * int(progress_percent * 50), ' ' * int(50 - int(progress_percent * 50)),
            progress_percent * 100, '%'))
    elif curr_progress == total:
        sys.stdout.write('\r')
        sys.stdout.write('%s [%s]100%s\n' % (prompt, '█' * 50, '%'))
    sys.stdout.flush()


def collect_mutual_words_to_set_from_dir(dir_of_txt_files):
    """
    generate stop word set from a given directory, by iterating all the txt files
    :param dir_of_txt_files: each txt file should contain word sperated by '\n'
    :return: a complete set of word
    """
    word_set = set()
    is_initialized = False
    for filename in os.listdir(dir_of_txt_files):
        curr_word_set = set()
        if filename.endswith(".txt"):
            file = os.path.join(dir_of_txt_files, filename)
            words = [line.rstrip('\n') for line in open(file, encoding='utf-8')]
            for word in words:
                curr_word_set.add(word)
            if is_initialized is True and len(curr_word_set) != 0:
                word_set = word_set.intersection(curr_word_set)
            else:
                word_set = curr_word_set
                is_initialized = True
    return word_set


def collect_all_words_to_set_from_dir(dir_of_txt_files):
    """
    generate stop word set from a given directory, by iterating all the txt files
    :param dir_of_txt_files: each txt file should contain word sperated by '\n'
    :return: a complete set of word
    """
    word_set = set()
    for filename in os.listdir(dir_of_txt_files):
        if filename.endswith(".txt"):
            file = os.path.join(dir_of_txt_files, filename)
            words = [line.rstrip('\n') for line in open(file, encoding='utf-8')]
            for word in words:
                word_set.add(word)
    return word_set


def count_word_in_doc(list_of_words):
    word_counter_for_separate_doc = {}
    for word in list_of_words:
        if word not in word_counter_for_separate_doc.keys():
            word_counter_for_separate_doc[word] = 1
        else:
            word_counter_for_separate_doc[word] += 1
    return word_counter_for_separate_doc


def get_topic_with_words(gensim_lda_model, num_topics=-1, num_words=None, formatted=False):
    """
    From Gensim: Get a representation for selected topics.

    Returns
    -------
    list of {str, tuple of (str, float)}
        a list of topics, each represented either as a string (when `formatted` == True) or word-probability
        pairs.

    """
    if num_topics < 0 or num_topics >= gensim_lda_model.num_topics:
        num_topics = gensim_lda_model.num_topics
        chosen_topics = range(num_topics)
    else:
        num_topics = min(num_topics, gensim_lda_model.num_topics)

        # add a little random jitter, to randomize results around the same alpha
        sort_alpha = gensim_lda_model.alpha + 0.0001 * gensim_lda_model.random_state.rand(len(gensim_lda_model.alpha))
        # random_state.rand returns float64, but converting back to dtype won't speed up anything

        sorted_topics = list(matutils.argsort(sort_alpha))
        chosen_topics = sorted_topics[:num_topics // 2] + sorted_topics[-num_topics // 2:]

    shown = []

    topic = gensim_lda_model.state.get_lambda()
    for i in chosen_topics:
        topic_ = topic[i]
        topic_ = topic_ / topic_.sum()  # normalize to probability distribution
        bestn = matutils.argsort(topic_, num_words, reverse=True)
        topic_ = [(gensim_lda_model.id2word[id], topic_[id]) for id in bestn]
        if formatted:
            topic_ = ' + '.join('%.3f*"%s"' % (v, k) for k, v in topic_)
        shown.append((i, topic_))

    return shown


def read_txt_input(dataset_filename):
    corpus = []
    with open(os.path.join('data', 'original_data', dataset_filename), encoding='utf-8') as f:
        for line in f:
            corpus.append(line)
    return corpus


def get_sql_database_input(database_filename):
    remove_hashtag = re.compile(r'#[\w-]+#')
    con = sqlite3.connect(os.path.join('data', 'original_data', database_filename))
    cursor = con.cursor()
    cursor.execute("SELECT post_content, post_time FROM posts")
    rows = cursor.fetchall()
    corpus = [(remove_hashtag.sub(' ', str(post_content)), post_time) for post_content, post_time in rows]
    return corpus


def vis_post_num_time_stats(database_filename):
    con = sqlite3.connect(os.path.join('data', 'original_data', database_filename))
    cursor = con.cursor()
    cursor.execute("SELECT post_time, COUNT(1) AS post_num FROM posts GROUP BY post_time")
    rows = cursor.fetchall()

    x = [datetime.datetime.strptime(row[0], '%Y%m%d').date() for row in rows]
    y = [row[1] for row in rows]

    fig, ax = plt.subplots()

    # configure x_axis for date
    chinese_font = FontProperties(fname=os.path.join('data', 'STHeiti_Medium.ttc'))
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())

    plt.xlabel('日期', fontproperties=chinese_font)
    plt.ylabel('收集微博数（条）', fontproperties=chinese_font)

    ax.grid()

    # Plot
    ax.plot(x, y)
    plt.show()


def color_set(num):
    color_set = {-1: (207 / 256, 207 / 256, 207 / 256),
                 0: (31 / 256, 119 / 256, 180 / 256),
                 1: (174 / 256, 199 / 256, 232 / 256),
                 2: (255 / 256, 127 / 256, 14 / 256),
                 3: (255 / 256, 187 / 256, 120 / 256),
                 4: (44 / 256, 160 / 256, 44 / 256),
                 5: (152 / 256, 223 / 256, 138 / 256),
                 6: (214 / 256, 39 / 256, 40 / 256),
                 7: (255 / 256, 152 / 256, 150 / 256),
                 8: (148 / 256, 103 / 256, 189 / 256),
                 9: (197 / 256, 176 / 256, 213 / 256),
                 10: (140 / 256, 86 / 256, 75 / 256),
                 11: (196 / 256, 156 / 256, 148 / 256),
                 12: (227 / 256, 119 / 256, 194 / 256),
                 13: (247 / 256, 182 / 256, 210 / 256),
                 14: (127 / 256, 127 / 256, 127 / 256),
                 15: (199 / 256, 199 / 256, 199 / 256),
                 16: (188 / 256, 189 / 256, 34 / 256),
                 17: (219 / 256, 219 / 256, 141 / 256),
                 18: (23 / 256, 190 / 256, 207 / 256),
                 19: (158 / 256, 218 / 256, 229 / 256),
                 }
    return color_set[num]

# -*- coding: utf-8 -*-
from common import set_log, set_common, input_text, output_text
from logging import getLogger, config

from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

log_conf = set_log()
config.dictConfig(log_conf)
logger = getLogger(__name__)

common_conf = set_common()


def summary_text():
    # テキストを読み込む
    text = input_text(common_conf['filename'])
    # 自動要約のオブジェクトを生成
    auto_abstractor = AutoAbstractor()
    # トークナイザー（単語分割）にMeCabを指定
    auto_abstractor.tokenizable_doc = MeCabTokenizer()
    # 文書の区切り文字を指定
    auto_abstractor.delimiter_list = ["。", "\n"]
    # ドキュメントの抽象化、フィルタリングを行うオブジェクトを生成
    abstractable_doc = TopNRankAbstractor()
    # 文書の要約を実行
    result_dict = auto_abstractor.summarize(text, abstractable_doc)

    print(result_dict)
    output_text(common_conf['filename'], result_dict)


if __name__ == '__main__':
    logger.info('START')
    summary_text()
    logger.info('END')

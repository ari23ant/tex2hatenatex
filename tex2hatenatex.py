#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tex→はてなTex変換

Browser Addon markdown view
MathJaxで書いた数式Tex形式をはてなTex形式に変換する
- 第1引数｜.mdファイルのファイルパス

memo: replace_symbol_displayとreplace_symbol_inlineは共通化できるが、
      解読困難な正規表現をわかりやすくするため、あえて分けて管理している。
      同様の理由で、正規表現パターンを引数化していない。

"""
__author__  = 'ari23(Twitter: @ari23ant)'
__version__ = '0.0.4'
__date__    = '2020/10/16'
__status__  = 'Development'

import os
import re
import sys
import time
from IPython import get_ipython

NORMAL_MODE = True  # デバッグしたいときはFalseにする


class Tex2HatenaTex:

    def __init__(self, fpath=''):
        self.msg = 'Tex to HatenaTex'
        # ------- 入力 ------- #
        # 変換したいファイルパス
        self.fpath = fpath

        # ------- 正規表現 ------- #
        ####################################
        # $マーク以外→$マークの順で変換する
        ####################################
        # 改行コード
        # Mac->\r, Unix->\n, Windows->\r\n, 自動->os.linesep
        self.linesep = r'\n'

        # --- 角括弧[] --- #
        # - ディスプレイ数式 - #
        #  [→\[, ]→\] \を1つ足す
        # Tex記法 置換元
        self.kaku_l = '\['  # [の意味 r'\['でもよい
        self.kaku_r = '\]'  # ]の意味 r'\]'でもよい
        # HatenaTex記法 置換先
        self.kaku_l_ht_display = '\\['  # \[の意味 r'\['でもよい
        self.kaku_r_ht_display = '\\]'  # \]の意味 r'\]'でもよい

        # - インライン数式 - #
        # [→\\[, ]→\\] \を2つ足す
        # HatenaTex記法 置換先
        self.kaku_l_ht_inline = '\\\\['  # \\[の意味 r'\\['でもよい
        self.kaku_r_ht_inline = '\\\\]'  # \\]の意味 r'\\]'でもよい

        # --- アンダースコア_ --- #
        # - ディスプレイ数式 - #
        # 対応不要
        # - インライン数式 - #
        # _→\_ \を1つ足す
        # Tex記法 置換元
        self.underscore = '_'  # r'_'でもよい
        # HatenaTex記法 置換先
        self.underscore_ht_inline = '\\_'  # \_の意味 r'\_'でもよい

        # --- $マーク --- #
        # - ディスプレイ数式 - #
        # Tex記法 置換元
        pattern_line_1 = r'\$\$[\n|\r\n|\r]'
        pattern_line_2 = r'([\s\S]+?)'
        pattern_line_3 = r'\$\$[\n|\r\n|\r]'
        self.pattern_display = pattern_line_1 + pattern_line_2 + pattern_line_3
        # HatenaTex記法 置換先
        repl_line_1 = r"<div align='center' class='scroll'>" + self.linesep  # 'のために"でくくった
        repl_line_2 = r'[tex: \displaystyle' + self.linesep
        repl_line_3 = r'\1'
        repl_line_4 = r']' + self.linesep
        repl_line_5 = r'</div>' + self.linesep
        self.repl_display = repl_line_1 + repl_line_2 + repl_line_3 + repl_line_4 + repl_line_5

        # - インライン数式 - #
        # Tex記法 置換元
        self.pattern_inline = r'\$(.+?)\$'  # 非欲張り型
        # HatenaTex記法 置換先
        self.repl_inline = r'[tex: \1 ]'

        # ------- 出力 ------- #
        # 出力先のファイル名
        self.fname_out = 'hatenatex.md'


    def Process(self):
        print(self.msg)

        # ------- ファイル読み込み ------- #
        # 有無確認
        if not os.path.isfile(self.fpath):
            print('file NOT FOUND: ' + self.fpath)
            return False

        # ファイル名とディレクトリパス用意
        fname = os.path.basename(self.fpath)
        dpath = os.path.dirname(self.fpath)

        # 読み込み
        with open(self.fpath, mode='r', encoding='utf-8') as f:
            self.s = f.read()

        # ------- 置換 ------- #
        # --- 角括弧[] --- #
        # ディスプレイ数式 [→\[, ]→\] \が1つ
        self.s = self.replace_symbol_display(self.kaku_l, self.kaku_l_ht_display, self.s)
        self.s = self.replace_symbol_display(self.kaku_r, self.kaku_r_ht_display, self.s)

        # インライン数式 [→\\[, ]→\\] \が2つ
        self.s = self.replace_symbol_inline(self.kaku_l, self.kaku_l_ht_inline, self.s)
        self.s = self.replace_symbol_inline(self.kaku_r, self.kaku_r_ht_inline, self.s)

        # --- アンダースコア_ --- #
        # インライン数式 _→\_ \が1つ
        self.s = self.replace_symbol_inline(self.underscore, self.underscore_ht_inline, self.s)

        # --- $マーク --- #
        # ディスプレイ数式
        self.s = self.replace_dollar(self.pattern_display, self.repl_display, self.s)
        # インライン数式
        self.s = self.replace_dollar(self.pattern_inline, self.repl_inline, self.s)

        # ------- ファイル出力 ------- #
        fpath_out = os.path.join(dpath, self.fname_out)
        with open(fpath_out, mode='w', encoding='utf-8') as f:
            f.write(self.s)

        return True


    def replace_symbol_display(self, word1, word2, body, num_max=100):
        """
        数式内に複数ある同じパターンをfor文で置換する
        同じパターンの最大個数はnum_maxで設定
        """
        # いったん以下のワードに置き換える
        tmpword = 'tmpworddisplay'
        pattern = r'\$\$([^\$]+?)'+ word1 + r'([^\$]*?)\$\$[\n|\r\n|\r][\n|\r\n|\r]'
        repl = r'$$\1' + tmpword + r'\2$$' + self.linesep + self.linesep
        # [^\$]を[\s\S]にすると、数式内でないものもヒットしてしまう20201015
        ## pattern = r'\$\$([\s\S]+?)'+ word1 +r'([\s\S]*?)\$\$[\n|\r\n|\r][\n|\r\n|\r]'
        ## repl =  r'$$' + r'\1' + tmpword + r'\2$$' + self.linesep + self.linesep

        # 正規表現で置換
        tuple_subn = (body, None)
        cnt = 0
        for num in range(num_max):
            tuple_subn = re.subn(pattern, repl, tuple_subn[0])
            cnt += tuple_subn[1]
            if tuple_subn[1] == 0:
                # 置換し終わったらbreak
                print(pattern + ' --> ' + str(cnt))
                break

        # いっぺんに置き換え 計算量は増えるが、汎用性考慮してこの方法を選択した
        if NORMAL_MODE:
            s = tuple_subn[0].replace(tmpword, word2)
        else:
            s = tuple_subn[0]  # debug用 tmpwordで確認できる

        return s


    def replace_symbol_inline(self, word1, word2, body, num_max=100):
        """
        インライン数式内に複数ある同じパターンをfor文で置換する
        同じパターンの最大個数はnum_maxで設定
        """
        # いったん以下のワードに置き換える
        tmpword = 'tmpwordinline'
        pattern = r'\$(.+?)' + word1 + r'(.*?)\$'
        repl = r'$\1' + tmpword + r'\2$'

        # 正規表現で置換
        tuple_subn = (body, None)
        cnt = 0
        for num in range(num_max):
            tuple_subn = re.subn(pattern, repl, tuple_subn[0])
            cnt += tuple_subn[1]
            if tuple_subn[1] == 0:
                # 置換し終わったらbreak
                print(pattern + ' --> ' + str(cnt))
                break

        # いっぺんに置き換え 計算量は増えるが、汎用性考慮してこの方法を選択した
        if NORMAL_MODE:
            s = tuple_subn[0].replace(tmpword, word2)
        else:
            s = tuple_subn[0]  # debug用 tmpwordで確認できる

        return s


    def replace_dollar(self, pattern, repl, body):
        """
        数式の$マークを置換する
        """
        tuple_subn = re.subn(pattern, repl, body)
        print(pattern + ' --> ' + str(tuple_subn[1]))

        return tuple_subn[0]


if __name__ == '__main__':
    # IPython使用時のおまじない
    if get_ipython().__class__.__name__ == 'TerminalInteractiveShell':
        # IPython Resetコマンド
        get_ipython().magic('reset -sf')
        print('IPython reset command')

    # ---------- Program Start ---------- #
    start_time = time.perf_counter()
    print('---------- Start ----------')

    # --- Get Argument --- #
    args = sys.argv  # list
    # --- Main Process --- #
    if len(args) == 1:
        proc = Tex2HatenaTex()
    else:  # argsの大きさが0になることはない
        proc = Tex2HatenaTex(args[1])
    proc.Process()

    # ---------- Program End ---------- #
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print('Execution Time: ' + str(execution_time) + 's')
    print('----------  End  ----------')

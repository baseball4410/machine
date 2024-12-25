# ライブラリの読み取り　
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pybaseball as pyb

# 日本語フォントの設定
font_path = 'C:/Windows/Fonts/msgothic.ttc' 
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# 関数の作成
def draft_analysis(year, round_num):
    # データを取得
    draft_data = pyb.amateur_draft(year, round_num)
    
    # ポジションの英語から日本語への変換辞書
    pos_translation = {
        'OF': '外野手',
        'LHP': '左投手',
        'RHP': '右投手',
        'SS': 'ショート',
        'C': 'キャッチャー',
        '1B': 'ファースト',
        '3B': 'サード',
        'P': '投手(左右関係なく)',
    }
    
    # ポジションを日本語に変換
    draft_data['Pos'] = draft_data['Pos'].map(pos_translation)
    
    # ポジションの分布を計算
    position_distribution = draft_data['Pos'].value_counts()
    
    # 最もWARが高い選手を見つける（累計）
    highest_war_player = draft_data.loc[draft_data['WAR'].idxmax()]
    
    # 結果を表示
    st.write(f"年度: {year}, 何巡目: {round_num}")
    st.write("\nポジションの分布:")
    st.write(position_distribution)
    st.write("\n最もWARが高い選手(累計):")
    st.write(f"名前: {highest_war_player['Name']}, WAR: {highest_war_player['WAR']}")
    
    # WARの説明を追加
    st.write("\nWAR（Wins Above Replacement）とは、選手の総合的な貢献度を示す指標であり、"
             "その選手がいなかった場合に比べてチームが何勝多くできるかを表します。"
             "WARが高いほど、その選手の貢献度が高いことを意味します。"
             "投手・野手共通で使えます。")
    
    # ポジションの分布をグラフ化
    plt.figure(figsize=(10, 6))
    sns.barplot(x=position_distribution.index, y=position_distribution.values, palette='viridis')
    plt.title(f'{year}年ドラフト {round_num}順目のポジション分布')
    plt.xlabel('ポジション')
    plt.ylabel('選手数')
    st.pyplot(plt)

# Streamlitアプリケーションの設定
st.title('ドラフト分析ツール')
year = st.number_input('年度を入力してください:', min_value=1965, max_value=2023, value=1965)
round_num = st.number_input('何巡目かを入力してください:', min_value=1, max_value=50, value=1)

if st.button('Search!'):
    draft_analysis(year, round_num)

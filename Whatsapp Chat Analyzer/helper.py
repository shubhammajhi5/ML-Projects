from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # 1. fetching no of messages
    num_messages = df.shape[0]

    # 2. fetching no of words
    words = []
    for message in df['messages']:
        words.extend(message.split())
    num_words = len(words)

    # 3. fetching no of media messages
    num_media_messages = df[df['messages'] == '<Media omitted>'].shape[0]

    # 4. fetching no of links shared
    extract = URLExtract()

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    num_links_shared = len(links)

    return num_messages, num_words, num_media_messages, num_links_shared


def most_busy_users(df):
    x = df['users'].value_counts()

    new_df = round((df['users'].value_counts(normalize=True)) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'})

    return x, new_df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=' '))

    return df_wc


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'chat_notification']
    temp = temp[temp['messages'] != '<Media omitted>']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'num_occurrence'])

    return most_common_words_df


def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []

    for message in df['messages']:
        for word in message:
            if emoji.is_emoji(word):
                emojis.extend(word)

    most_common_emojis_df = pd.DataFrame(Counter(emojis).most_common(20), columns=['emoji', 'num_occurrence'])

    return most_common_emojis_df


def monthly_timeline_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    monthly_timeline = df.groupby(['year', 'month']).count()['messages'].reset_index()

    month_year = []
    for i in range(monthly_timeline.shape[0]):
        month_year.append(monthly_timeline['month'][i] + '-' + str(monthly_timeline['year'][i]))

    monthly_timeline['month_year'] = month_year

    return monthly_timeline


def daily_timeline_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('date').count()['messages'].reset_index()

    return daily_timeline


def weekly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    busy_week = df['day_name'].value_counts()

    return busy_week


def monthly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    busy_month = df['month'].value_counts()

    return busy_month


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    heatmap_data = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return heatmap_data







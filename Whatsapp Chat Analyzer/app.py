import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a File')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    # fetch unique users

    users_list = df['users'].unique().tolist()
    users_list.remove('chat_notification')
    users_list.sort()
    users_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('Show Analysis wrt', users_list)

    if st.sidebar.button('Show Analysis'):

        # stats area

        st.title('Top Statistics')
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(num_words)

        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)

        with col4:
            st.header('Links Shared')
            st.title(num_links)


        # monthly timeline

        st.title('Monthly Timeline')

        monthly_timeline = helper.monthly_timeline_analysis(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['month_year'], monthly_timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # daily timeline

        st.title('Daily Timeline')

        daily_timeline = helper.daily_timeline_analysis(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date'], daily_timeline['messages'], color='violet')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # activity map

        st.title('User Activity Map')

        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Month')
            busy_month = helper.monthly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Day')
            busy_day = helper.weekly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='indigo')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # weekly activity heatmap

        st.title('Weekly Activity Heatmap')

        heatmap_data = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap_data)
        st.pyplot(fig)


        # finding the busiest users in the group (only for group level analysis)

        if selected_user == 'Overall':
            st.title('Most Busy Users')

            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        # wordcloud

        st.title('Wordcloud')

        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')
        st.pyplot(fig)


        # most common words

        st.title('Most Common Words')

        most_common_words_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_words_df['word'], most_common_words_df['num_occurrence'])
        st.pyplot(fig)


        # emojis analysis

        st.title('Most Common Emojis')

        most_common_emojis_df = helper.emoji_analysis(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.pie(most_common_emojis_df['num_occurrence'].head(), labels=most_common_emojis_df['emoji'].head(), autopct='%0.2f%%')
            st.pyplot(fig)

        with col2:
            st.dataframe(most_common_emojis_df)
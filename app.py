import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    
    # Remove group_notification from DataFrame
    df = df[df['user'] != 'group_notification']    
    
    # fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    
    
    # to create the selectbox for the users
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    
    # to create the button to show the analysis
    if st.sidebar.button("Show Analysis"):
        
        # Stats Area
        num_messages,words,num_media_messages,links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(links)
            
            
        # monthly-timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        
        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        
        #daily activity
        st.title("Actvity Map")
        col1,col2=st.columns(2)
        
        with col1:
            st.header("Most Busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            name=busy_day.index
            count=busy_day.values
            ax.bar(name,count,color='green')
            for i in range(len(name)):
                    plt.text(i, count[i], str(count[i]), ha='center', va='bottom')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.header("Most Busy month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            name=busy_month.index
            count=busy_month.values
            ax.bar(name,count,color='orange')
            for i in range(len(name)):
                    plt.text(i, count[i], str(count[i]), ha='center', va='bottom')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        
        
            
        # Finding the busiest users in the group(Group Level)
        
        if selected_user=='Overall':
            st.title("Most Busy Users")
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            
            col1,col2=st.columns(2)
            
            with col1:
                name=x.index
                count=x.values
                ax.bar(name,count,color='red')
                plt.xticks(rotation='vertical')
                # Add count labels above bars
                for i in range(len(name)):
                    plt.text(i, count[i], str(count[i]), ha='center', va='bottom')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
                
                
        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
            
        #most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        plt.xticks(rotation='vertical')
        ax.barh(most_common_df[0],most_common_df[1])
        st.title("Most Common Words")
        st.pyplot(fig)
        # st.dataframe(most_common_df)
        
        ## emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        
        col1,col2=st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct="%0.2f")
            st.pyplot(fig)
            
    
    
    
    
    
    
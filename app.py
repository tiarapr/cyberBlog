from ctypes.wintypes import LPINT
from turtle import pd
from unittest import result
import streamlit as st

# EDA Pkgs
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Connect db
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Functions
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS cyberBlog(title TEXT, article TEXT, author TEXT, postdate DATE)')
def add_data(title, article, author, postdate):
    c.execute('INSERT INTO cyberBlog(title, article, author, postdate) VALUES (?,?,?,?)', (title, article, author, postdate))
    conn.commit()
def view_all_notes():
    c.execute('SELECT * FROM cyberBlog')
    data = c.fetchall()
    return data
def view_all_articles():
    c.execute('SELECT title, author, postdate FROM cyberBlog')
    data = c.fetchall()
    return data
def view_all_titles():
    c.execute('SELECT DISTINCT title FROM cyberBlog')
    data = c.fetchall()
    return data
def get_blog_by_title(title):
    c.execute('SELECT * FROM cyberBlog WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data
def delete_data(title):
    c.execute('DELETE FROM cyberBlog WHERE title="{}"'.format(title))
    conn.commit()
def update_article(update_blog_title, update_blog_article, update_blog_author, update_blog_post_date, title, article, author, postdate):
    c.execute("UPDATE cyberBlog SET title=?, article=?, author=?, postdate=? WHERE title=? and article=? and author=? and postdate=? ", (update_blog_title, update_blog_article, update_blog_author, update_blog_post_date, title, article, author, postdate))
    conn.commit()
    data = c.fetchall()
    return data

# Layout Templates Home
home_temp = """
<div style="margin-top:10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); border-radius: 10px;">
    <div style="padding:20px;">
        <article>
            <h4 style="margin-bottom:20px">{}</h4>
            <p>By : {}</p>
            <p>Post Date : {}</p>
        </article>
    </div>
</div>
"""

# Layout Templates View Post
view_post_temp = """
<div style="padding:10px, margin:10px;">
    <br>
    <h2 style='text-align: center; margin: 20px 0'>{}</h2>
    <p>{}</p>
    <br>
    <p>{}</p>
    <p>{}</p>
</div>
"""

def main():
    # Blog Name
    st.markdown("<h1 style='color: red; margin-bottom:20px'>Cyber Blog</h1>", unsafe_allow_html=True)
    
    # Images
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("images/data.png")

    with col2:
        st.image("images/hacked.png")

    with col3:
        st.image("images/protect.png")

    # Menu
    menu = ["Home", "Read Articles", "Add Articles", "Update Articles", "Manage Blog"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.markdown("<h4 style='margin-top:20px'>List Articles</h4>", unsafe_allow_html=True)

        # Show data articles
        result = view_all_articles()
        
        for i in result:
            b_title = i[0]
            b_author = i[1]
            b_post_date = i[2]
            st.markdown(home_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)

    elif choice == "Read Articles":
        all_titles = [i[0] for i in view_all_titles()]
        postList = st.sidebar.selectbox("Read Articles by title", all_titles)

        post_result = get_blog_by_title(postList)
        for i in post_result:
            b_title = i[0]
            b_article = i[1]
            b_author = i[2]
            b_post_date = i[3]
            st.markdown(view_post_temp.format(b_title,b_article,b_author,b_post_date), unsafe_allow_html=True)

    elif choice == "Add Articles":
        st.markdown("<h3 style='margin-top:20px'>Add Articles</h3>", unsafe_allow_html=True)

        create_table()
        blog_title = st.text_input("Title", max_chars=50)
        blog_article = st.text_area("Article", height=200, max_chars=10000)
        blog_author = st.text_input("Author", max_chars=50)
        blog_post_date = st.date_input("Date")

        if st.button("Add Article"):
            add_data(blog_title, blog_article, blog_author, blog_post_date)
            st.success("Post: {} saved".format(blog_title))
    
    elif choice == "Update Articles":
        st.markdown("<h3 style='margin-top:20px'>Update Articles</h3>", unsafe_allow_html=True)

        titles = [i[0] for i in view_all_titles()]
        update_blog_by_title = st.sidebar.selectbox("Title", titles)
        selected_result = get_blog_by_title(update_blog_by_title)
        
        if selected_result:
            title = selected_result[0][0]
            article = selected_result[0][1]
            author = selected_result[0][2]
            postdate = selected_result[0][3]

            update_blog_title = st.text_input("Title", title, max_chars=50)
            update_blog_article = st.text_area("Article", article, height=200, max_chars=10000)
            update_blog_author = st.text_input("Author", author, max_chars=50)
            update_blog_post_date = st.date_input(postdate)

            if st.button("Update Article"):
                update_article(update_blog_title, update_blog_article, update_blog_author, update_blog_post_date, title, article, author, postdate)
                st.success("Post: {} updated To: {}".format(title, update_blog_title))

    elif choice == "Manage Blog":
        st.markdown("<h3 style='margin-top:20px'>Manage Articles</h3>", unsafe_allow_html=True)

        result = view_all_notes()

        with st.expander("View All Data"):
            clean_db = pd.DataFrame(result, columns=["Title", "Articles", "Author", "Post Date"])
            st.dataframe(clean_db)
            
        with st.expander("Delete by title"):
            all_titles = [i[0] for i in view_all_titles()]
            delete_blog_by_title = st.selectbox("Title", all_titles)

            if st.button("Delete"):
                delete_data(delete_blog_by_title)
                st.warning("Deleted: '{}'".format(delete_blog_by_title))

if __name__=='__main__':
    main()
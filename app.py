
import streamlit as st
import sqlite3

st.markdown(
    """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-MBXPFR25QW"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-MBXPFR25QW');
    </script>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="The Caregiver Circle",
)

st.title("Our Discussion Board")

st.write("A place for people to share, connect, and have conversation.")

## connect to a database
conn = sqlite3.connect("discussion_board.db")
cursor = conn.cursor()

## Create a table to store discussions
cursor.execute("""
CREATE TABLE IF NOT EXISTS discussions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    post TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

## Create comments section
cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    post TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# new Discussion section
st.subheader("Start A Discussion")

title = st.text_input("Discussion Title")
post = st.text_area("What is on your mind?")

if st.button("Publish"):
    if title.strip() and post.strip():

        cursor.execute(
            "INSERT INTO discussions (title, post) VALUES (?, ?)",
            (title.strip(), post.strip()))


        conn.commit()
        st.success("Discussion published!")
        st.rerun()

    else:
        st.warning("Please enter a title and description")

# Recent discussion
st.divider()
st.subheader("Recent Discussions")

cursor.execute("""
SELECT title, post, created_at
FROM discussions
ORDER BY id DESC
""")

discussions = cursor.fetchall()

if discussions:
    for discussion_id, title, post, created_at in discussions:

        with st.container(border=TRUE):

            st.markdown(f"### {title}")
            st.write(post)
            st.caption(f"Posted: {created_at}")

            st.markdown("**Comments**")

            cursor.execute("""
            SELECT comment, created_at
            FROM comments
            WHERE discussion_id = ? 
            ORDER BY id ASC
            """, (discussion_id,))

            comments = cursor.fetchall()

            if comments: 
                for comment, comment_date in comments:
                    st.write(comment)
                    st.caption(f"Commented: {comment_date}")

            else: 
                st.write("No Comments Yet.")

        ## Add a new comment 

        with st.form(key=f"comment_from_{discussion_id}"):

            new_comment - st.text_area(
                "Write a comment",
                key=f"comment_input_{discussion_id}"
            )

        submitted = st.form_submit_button("Add Comment")

        if submitted: 
            if new_comment.strip():

                    cursor.execute("""
                    INSERT INTO comments (discussion_id, comment)
                    VALUES (?, ?)
                    """, (discussion_id, new_comment.strip()))

                    conn.commit()
                    st.rerun()
    else: 
        st.warning("No discussions yet. Be the first to post!")

conn.close()

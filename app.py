import streamlit as st
from datetime import datetime
import os
import re

# Directory for blog posts
BLOG_DIR = "blog_posts"

# Function to save or update blog post
def save_blog_post(title, content, date, time, category, tags, filename=None, append=False):
    if not filename:
        filename = f"{title.replace(' ', '_')}.txt"  # Filename is now only the title, no date
    os.makedirs(BLOG_DIR, exist_ok=True)
    filepath = os.path.join(BLOG_DIR, filename)

    mode = "a" if append else "w"
    with open(filepath, mode) as file:
        if append:
            # Ensure the new content starts on a new line after date and time
            file.write(f"\n\n[Date: {date} {time}]\n{content}\n")
        else:
            file.write(f"Title: {title}\n")
            file.write(f"Category: {category}\n")
            file.write(f"Tags: {tags}\n")
            file.write(f"Content:\n{content}\n")
    return filepath

# Function to load a blog post
def load_blog_post(filepath):
    with open(filepath, "r") as file:
        return file.read()

# Function to list and search blog posts
def list_saved_posts(search_query=None):
    if not os.path.exists(BLOG_DIR):
        return []
    files = sorted([f for f in os.listdir(BLOG_DIR) if f.endswith(".txt")])
    if search_query:
        # Use re.IGNORECASE to make search case-insensitive
        files = [f for f in files if re.search(search_query, f, re.IGNORECASE)]
    return files

# Streamlit blog UI
st.set_page_config(page_title="Blogging App", layout="wide")
st.title("Streamlit Blogging App")

# --- Sidebar ---
sidebar_option = st.sidebar.radio("Choose an Option", ["Search Blog Posts", "View All Saved Posts", "Create New Blog Post"])

# --- Search Section ---
if sidebar_option == "Search Blog Posts":
    search_query = st.text_input("Search Blog Posts", key="search", label_visibility="collapsed")

    if search_query:  # If search query exists, show results and options
        # List matching blog posts
        filtered_posts = list_saved_posts(search_query)

        if filtered_posts:
            selected_post = st.selectbox("Select a Post", ["Create New Post"] + filtered_posts)

            if selected_post != "Create New Post":
                filepath = os.path.join(BLOG_DIR, selected_post)
                post_content = load_blog_post(filepath)

                # Sidebar Action: View or Add Content
                action = st.sidebar.radio("Choose an Action", ["View Complete Blog", "Add Today's Content"])

                # Option 1: View Complete Blog
                if action == "View Complete Blog":
                    st.subheader(f"Complete Blog: {selected_post}")
                    st.text(post_content)
                    # Download button for the selected post
                    with open(filepath, "rb") as file:
                        st.download_button(
                            label="Download Blog Post",
                            data=file,
                            file_name=selected_post,
                            mime="text/plain"
                        )

                # Option 2: Add Today's Content
                elif action == "Add Today's Content":
                    new_content = st.text_area("Enter today's content:")
                    if st.button("Save Today's Content"):
                        if new_content:
                            today_date = datetime.now().strftime("%Y-%m-%d")
                            current_time = datetime.now().strftime("%H:%M:%S")
                            # For adding content, you don't need category and tags as they are already present
                            save_blog_post(None, new_content, today_date, current_time, "", "", filename=selected_post, append=True)
                            st.success("Today's content added successfully.")
                        else:
                            st.error("Content cannot be empty.")
        else:
            st.sidebar.warning("No posts match your search query.")
    
elif sidebar_option == "View All Saved Posts":
    # List all saved blog posts
    saved_posts = list_saved_posts()

    if saved_posts:
        selected_post = st.selectbox("Select a Post to View", saved_posts)

        if selected_post:
            filepath = os.path.join(BLOG_DIR, selected_post)
            post_content = load_blog_post(filepath)
            st.subheader(f"Complete Blog: {selected_post}")
            st.text(post_content)
            
            # Download button for the selected post
            with open(filepath, "rb") as file:
                st.download_button(
                    label="Download Blog Post",
                    data=file,
                    file_name=selected_post,
                    mime="text/plain"
                )

            # Add today's content button (only here)
            action = st.radio("What would you like to do?", ["View Complete Blog", "Add Today's Content"])

            if action == "Add Today's Content":
                new_content = st.text_area("Enter today's content:")
                if st.button("Save Today's Content"):
                    if new_content:
                        today_date = datetime.now().strftime("%Y-%m-%d")
                        current_time = datetime.now().strftime("%H:%M:%S")
                        # Append today's content to the blog post
                        save_blog_post(None, new_content, today_date, current_time, "", "", filename=selected_post, append=True)
                        st.success("Today's content added successfully.")
                    else:
                        st.error("Content cannot be empty.")

    else:
        st.sidebar.warning("No saved blog posts available.")

# --- Create New Blog Post ---
elif sidebar_option == "Create New Blog Post":
    st.sidebar.subheader("Create New Blog Post")
    title = st.text_input("Title")
    date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    category = st.selectbox("Category", ["Technology", "Lifestyle", "Education", "Other"])
    tags = st.text_input("Tags (comma-separated)")
    content = st.text_area("Content")

    if st.button("Save New Blog Post"):
        if title and category and tags and content:
            save_blog_post(title, content, date, current_time, category, tags)
            st.success(f"Blog post '{title}' saved successfully.")
        else:
            st.error("Please provide a title, category, tags, and content.")

# --- Update Existing Blog Post ---
else:
    # Add only content to existing blog posts
    st.sidebar.subheader("Update Existing Blog Post")
    selected_post_for_update = st.selectbox("Select a Post to Update", list_saved_posts())

    if selected_post_for_update:
        filepath = os.path.join(BLOG_DIR, selected_post_for_update)
        post_content = load_blog_post(filepath)

        new_content = st.text_area("Enter today's content:", value="")
        if st.button("Save Updated Content"):
            if new_content:
                today_date = datetime.now().strftime("%Y-%m-%d")
                current_time = datetime.now().strftime("%H:%M:%S")
                save_blog_post(None, new_content, today_date, current_time, "", "", filename=selected_post_for_update, append=True)
                st.success("Content updated successfully.")
            else:
                st.error("Content cannot be empty.")

# Instructions for Users
st.markdown("""
### How to Use:
1. **Search for a Blog Post**: Use the search box to find an existing blog post. The search is case-insensitive.
2. **View All Saved Posts**: View all saved blog posts from the sidebar and select one to read or download.
3. **View or Edit Existing Post**: After searching or selecting from saved posts, you can view the full content or add new content for today.
4. **Create New Blog Post**: Select "Create New Post" to start a new blog entry. Fill in the Title, Category, Tags, and Content for the new blog.
5. **Download Option**: You can download any blog post after viewing it.
6. **Update Content**: You can update the content of an existing blog post without changing the title, category, or tags.
""")

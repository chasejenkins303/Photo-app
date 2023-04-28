import React from 'react';
import LikeButton from './LikeButton';
import { getHeaders } from './utils';
import { useState } from 'react';
import BookmarkButton from './BookmarkButton'
import AddComment from './AddComment';

export default function Post({post, token}) { 

    const [actualPost, setActualPost] = useState(post)

    async function requeryPost(post){
        const response = await fetch(`/api/posts/${actualPost.id}`, {
        method: "GET",
        headers: getHeaders(token)
    });
    const data = await response.json();
    console.log(data);
    setActualPost(data);
    //to make screen redraw, after requery, need state variable
    }

    return (
        <header className="photo-feed" id="post_">
                <div className="post-bar-top">
                    <p>{post.user.username}</p>
                    <button>
                        <i id="top" className="fas fa-ellipsis-h"></i>
                    </button>
                </div>
                <img aria-label='post' className="post" src={post.image_url}/>
                <div className="post-bar-bottom">
                    <section className="bottom-icons">
                            <LikeButton post={actualPost} token={token} requeryPost={requeryPost}></LikeButton>
                        <button>
                            <i className="far fa-comment"></i>
                        </button>
                        <button>
                            <i className="far fa-paper-plane"></i>
                        </button>
                    </section>
                        {/* ${isBookmarked(post)} */}
                        <BookmarkButton post={actualPost} token={token} requeryPost={requeryPost}></BookmarkButton>
                </div>
                <div className="comment-section">
                    <p className="like-count">{actualPost.likes.length} likes</p>
                    <p className = "caption">
                        <strong>{actualPost.user.username}</strong>
                        {actualPost.caption}
                    </p>
                    <p className = "days-ago">
                        {actualPost.display_time}
                    </p>
                    {/* ${showCommentAndButton(post)} */}


                    <p className="comments">
                        <button className = "com-button"> 
                        {/* //onclick="showModal(${post.id})"> */}
                            View all {actualPost.comments.length} comments
                        </button><br/>
                        <span className="username-poster">
                            {actualPost.comments.length > 0 ? actualPost.comments[actualPost.comments.length-1].user.username : ''}
                        </span>
                        <span className="com">
                            {actualPost.comments.length > 0 ? actualPost.comments[actualPost.comments.length-1].text : ''}
                        </span>
                        {/* <span className = "days-ago">
                        {post.comments.length > 0 ? post.comments[post.comments.length-1].display_time : ''}
                        </span> */}

                    </p>
                    <p className = "days-ago">
                        {actualPost.comments.length > 0 ? actualPost.comments[actualPost.comments.length-1].display_time : ''}
                    </p>

                    <hr className="com-line"/>
                    <AddComment post={actualPost} token={token} requeryPost={requeryPost}></AddComment>
                    {/* <section className = "add-comm" id="post_com_${post.id}">
                        <input type="text" id="add-c" className="com_${post.id}" placeholder="Add a comment..."/>

                        <button className="post-com-button" onclick="addComment(${post.id})">Post</button>
                    </section> */}
                </div>
            </header>
    )   
}
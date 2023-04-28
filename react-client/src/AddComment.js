import { getHeaders } from "./utils";

export default function AddComment({post, token, requeryPost}){

    async function addComment(){
            const text = document.querySelector(`.com_${post.id}`).value
            document.querySelector(`.com_${post.id}`).value = ''
            document.querySelector(`.com_${post.id}`).focus()
            console.log('CommentText',text)
            const endpoint = `/api/comments`;
            const postData = {
                "post_id": post.id,
                "text": text
            };
        
            // Create the bookmark:
            const response = await fetch(endpoint, {
                method: "POST",
                headers: getHeaders(token),
                body: JSON.stringify(postData)
            })
            const data = await response.json();
            console.log(data);
            requeryPost();
        
    }

    return(
        <section className = "add-comm" id="post_com_">
                <input type="form" id="add-c" className={`com_${post.id}`} onSubmit={addComment} placeholder="Add a comment..."/>

                <button className="post-com-button" onClick={addComment} onSubmit={addComment}>Post</button>
        </section>
    )

}
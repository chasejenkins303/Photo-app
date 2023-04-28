import { getHeaders } from "./utils";


export default function LikeButton({post, token, requeryPost}){
   
    const likeId=post.current_user_like_id;
    const postId= post.id;

    async function likeUnlike(){


        console.log(likeId, postId)
        if(likeId){
            console.log('unlike')
            const response = await fetch(`/api/posts/likes/${likeId}`, {
                method: "DELETE",
                headers: getHeaders(token)
            });
            const data = await response.json();
            console.log(data);
            requeryPost()
        }
        
        else{
            console.log('like')
            const postData={
                "post_id": postId
            }
         const response = await fetch("/api/posts/likes/", {
                method: "POST",
                headers: getHeaders(token),
                body: JSON.stringify(postData)
         });
        const data = await response.json();
        console.log(data);
        requeryPost();
    }


    }
   
    return(
        <button onClick={likeUnlike} role='switch' aria-checked={likeId ? 'true' : 'false'}>{likeId ? <i id="liked" className="fas fa-heart"></i> : <i id="notLiked" className="far fa-heart"></i>}</button>
    )
}
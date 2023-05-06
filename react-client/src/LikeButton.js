import { getHeaders } from "./utils";


export default function LikeButton({profile, post, token, requeryPost}){
   
    if(!profile){
        return ''
    }

    //console.log('profile like', profile.id)
    //const likeId=post.current_user_like_id;
    const likeId = post.likes.find((o)=>o.user_id === profile.id)
    //const likeId = likeInit.id
    const postId= post.id;

    async function likeUnlike(){


        //console.log('likeId, postID', likeId.id, postId)
        if(likeId){
            console.log('unlike')
            const response = await fetch(`/api/posts/likes/${likeId.id}`, {
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
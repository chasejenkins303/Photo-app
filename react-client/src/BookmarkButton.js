import { useEffect, useState } from "react";
import { getHeaders } from "./utils";


export default function BookmarkButton({profile, post, token, requeryPost}){
   
    let bookmarkId2
    const [bookmarkId, setBookmarkId] = useState(bookmarkId2)
    useEffect(() =>
    async function check(){
        const response = await fetch("/api/bookmarks/", {
        method: "GET",
        headers: getHeaders(token),
        });
        const data = await response.json();
        //console.log('bookmark list for testing',data);
        setBookmarkId(data.find(p => p.post.id === post.id))
       console.log('return value of check', bookmarkId)
        //return bookmarkId
    },[post])
    //check()
    //const bookmarkId=check();
    const postId= post.id;

    async function bookUnbook(){
        //check()

       // console.log('bookmark and post id', bookmarkId, postId)
        if(bookmarkId){
            console.log('unbookmark')
            const response = await fetch(`/api/bookmarks/${bookmarkId.id}`, {
                method: "DELETE",
                headers: getHeaders(token)
            });
            const data = await response.json();
            //console.log(data);
            requeryPost()
        }
        
        else{
            console.log('bookmark')
            const postData={
                "post_id": postId
            }
         const response = await fetch("/api/bookmarks/", {
                method: "POST",
                headers: getHeaders(token),
                body: JSON.stringify(postData)
         });
        const data = await response.json();
        //console.log(data);
        requeryPost();
    }
    console.log('end of function check for bookmark', bookmarkId)

    }

    //console.log('final check', bookmarkId)
   
    return(
        <button className="bookmark" onClick={bookUnbook} role='switch' aria-checked={bookmarkId ? 'true' : 'false'}>{bookmarkId ? <i id="bookmarked" className="fas fa-bookmark"></i> : <i id="notBookmarked" className="far fa-bookmark"></i>}</button>
    )
}
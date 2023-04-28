import React from 'react';
import { getHeaders } from './utils';
import { useState } from 'react';

export default function Suggestion({suggestion, token}) { 
    const [actualSug, setActualSug] = useState(suggestion)
    const [following, setFollowing] = useState(0)
    // let following = 0;
   // console.log('original following num', following)
    // const unfollowId = actualSug.id

    // const followData = {
    //     "user_id": actualSug.id
    // };

    async function followUnfollow(){
       console.log('following num',following)

       const followData = {
        "user_id": suggestion.id
        };
        console.log('follow data:', followData)
        if(following===0){
        const response = await fetch(`/api/following`, {
            method: "POST",
            headers: getHeaders(token),
            body: JSON.stringify(followData)
            }
        );
        const data = await response.json();
        console.log("Suggestion", data);
        setActualSug(data);
        setFollowing(1)
        }else{
            const response = await fetch(`api/following/${actualSug.id}`, {
                method: "DELETE",
                headers: getHeaders(token),
            })
            const data = await response.json();
            console.log(data);
            setActualSug(data);
            setFollowing(0)
        }
    //to make screen redraw, after requery, need state variable
    }



    if(!suggestion){
        console.log('not working')
        return ''
    }

    return (
        <div id="panel-1">
                <img aria-label='profile picture' className="prof" src={suggestion.image_url}/>
                <section id="user1">{suggestion.username}</section>
                <p>Suggested for you</p>
                <button role='switch' aria-checked={following===0 ? 'false' : 'true'} className="follow-button" id="follow_button_" onClick={followUnfollow}>{following===0 ? 'follow' : 'unfollow'}</button>
        </div> 
    )   
}
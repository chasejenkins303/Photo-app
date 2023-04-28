//The job of Profile is to show the name and image of 
//the person who is logged into the system

//TODO: assume the user is passed into this component as a prop

import React from "react";

export default function Profile({profile}){
    
    console.log("prof", profile)
    //return some jsx
    if(!profile){
        return ''
    }
   

    return (
        <div className="Suggestions">
            <img className='prof' src={profile.thumb_url}/>
            <section>{profile.username}</section>

        </div>

    )
}
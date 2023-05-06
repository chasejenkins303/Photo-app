import React, { useState } from "react";
import { getHeaders } from "./utils";
import { useEffect } from "react";

export default function Stories({profile, token}){
    
    const [actualStory, setActualStory] = useState([])

    useEffect(() => {
        async function fetchStories() {
            const response = await fetch('/api/stories', {
                headers: getHeaders(token)
            });
            const data = await response.json();
            setActualStory(data)
            console.log('Storiessss', data)
            console.log('story token', token)
        }
        fetchStories();
    }, [token]);

    
    // const storyToHtml=(story)=>{
    //     return `
    //         <section>
    //             <img src="${story.user.thumb_url}" />
    //             <button>${story.user.username}</button>
    //         </section>
    //     `
    // }

    if(!profile){
        return ''
    }

    return (
        <header id="stories-panel">

{
            actualStory.map(story => {
                return (
                    <section key={story.id}>
                        <img src={story.user.thumb_url} alt=''/>
                        <button>{story.user.username}</button>
                    </section>
                )
            })
        }
            {/* <section>
                <img src={actualStory.thumb_url}/>
                <button>{actualStory.username}</button>
            </section> */}
        </header>

    )
}
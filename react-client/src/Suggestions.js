import React from "react";
import { useState, useEffect } from "react";
import {getHeaders} from './utils';
import Suggestion from "./Suggestion";

export default function Suggestions({profile, token}){
    
    const [suggestions, setSuggestions]=useState([])
    console.log(profile)
    //return some jsx

    useEffect(() => {
        async function showSuggestions() {
            const response = await fetch('/api/suggestions/', {
                headers: getHeaders(token)
            });
            const data = await response.json();
            console.log('Suggestions: ', data);
            setSuggestions(data)
        }
        showSuggestions();
    
    }, [token]);
    
    // const suggestionToHtml = (sug) =>{
    //     console.log('sug.id', sug.id)
    //     return `
    //     <div id="panel-1">
    //         <img class="prof" src="${sug.image_url}">
    //         <section id="user1">${sug.username}</section>
    //         <p>Suggested for you</p>
    //         <button aria-checked="false" class="follow-button" id="follow_button_${sug.id}" onclick="followAccount(${sug.id})">follow</button>
    //      </div>`
    // }

    if(suggestions.length === 0){
        console.log('not getting suggestion')
        return <section className="sug-panel"></section>
    }
    return (
        <section className="sug-panel">
            {/* <div id="panel-1">
                <img className="prof" src={suggestions.image_url}/>
                <section id="user1">{suggestions.username}</section>
                <p>Suggested for you</p>
                <button aria-checked="false" class="follow-button" id="follow_button_${sug.id}" onClick="followAccount({sug.id})">follow</button>
            </div> */}
            {
            suggestions.map(sug => {
                return (
                    <Suggestion key={sug.id} suggestion={sug} token={token}/>
                )
            })
        }

        </section>

    )
}
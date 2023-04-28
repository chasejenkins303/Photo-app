import React from 'react';
// import { useState, useEffect } from "react";
// import {getHeaders} from './utils';

export default function NavLinks({profile}) { 
    // const [profile, setProfile] = useState(null);
    // useEffect(() => {
    //     async function fetchProfile() {
    //         const response = await fetch('/api/profile', {
    //             headers: getHeaders(token)
    //         });
    //         const data = await response.json();
    //         setProfile(data)
    //     }
    //     fetchProfile();
    // }, [token]);


    if (!profile) {
        return '';
    }
    return (



<header id="topnav">
        <h1 className='logo'>
            Photo App
        </h1>
    <section className='corner'>
        <button id='api'>
            API docs
        </button>
        <h1 className='username'>
            {profile.username}
        </h1>
        <button id='sign-in'>
            Sign Out
        </button>
    </section>
</header>
        
    );
    
}

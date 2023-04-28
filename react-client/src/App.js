import React from 'react';
import NavLinks from './NavLinks';
import Profile from './Profile';
import { useState, useEffect } from "react";
import {getHeaders} from './utils';
import Suggestions from './Suggestions';
import Posts from './Posts';
import Stories from './Stories';

export default function App ({token}) { 
    console.log('access token:', token);

    const [profile, setProfile] = useState(null);
    useEffect(() => {
        async function fetchProfile() {
            const response = await fetch('/api/profile', {
                headers: getHeaders(token)
            });
            const data = await response.json();
            setProfile(data)
        }
        fetchProfile();
    }, [token]);
    
    return (
        <div>
            
            {/* Navbar */}
            <nav id='topnav'>
                <h1>Photo App</h1>
                <NavLinks token={token} profile={profile} />
            </nav>
           

            <main>


            <aside>
                <Profile profile={profile}/>
                <Suggestions profile={profile} token={token}/>
            </aside>

            <section className="news-feed">
                {/* Stories */}
                <Stories profile={profile} token={token}/>

                <hr/>
                {/* Posts */}
                <Posts token={token}/>
                
            </section>

            

            <section className='main-feed'>
                <Posts token={token}/>
            </section>
            </main>

        </div>
    );
    
}
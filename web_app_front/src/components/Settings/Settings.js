import './Settings.sass';
import React, { useEffect, useState } from 'react';
import getProfileInfo from "../../getProfileInfo";
import Atree from "../../static/Atree.svg";
import httpClient from "../../httpClient";


const Settings = () => {
    const [profile_data, setProfileData] = useState("");

    const signOut = async () => {
        await httpClient.post("/logout");
        window.location.href = "/profile";
    };

    useEffect(async () => {
        const response = await getProfileInfo();
        if (response === null) {
            window.location.href = "/profile";
        }
        setProfileData(response.data);
    }, []);
    return (
        <div className="Settings">
            <div className="settings-wrapper">
                <div className="text-block">
                    <h1>{profile_data.email}</h1>
                    <p>Api key: {profile_data.api_key}</p>
                    <p>Secret: {profile_data.secret}</p>
                    <button type="button" onClick={() => signOut()}>sign out</button>
                </div>
                <div className="TreeDeco">
                    <img id='Atree' height={180} src={Atree}/>
                </div>
            </div>
        </div>
    )
}

export default Settings;
